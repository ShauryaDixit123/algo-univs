import subprocess
from django.http import JsonResponse

def compile_by_lang(lang:str,code:str, test_cases:list[dict[str,str]]):
    filename = 'temp.' + lang
    stdout, stderr = '', ''
    with open(filename, 'w') as file:
        file.write(code)

    output = {}
    for idx, test_case in enumerate(test_cases):
        print(idx,test_case,"sadsads")
        input_data = test_case['inp']
        expected_output = test_case['out']

        try:
            if lang == 'py':
                process = subprocess.Popen(['python', filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate(input_data, timeout=5)

            elif lang == 'java':
                process = subprocess.Popen(['javac', filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                process.wait()
                process = subprocess.Popen(['java', 'temp'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate(input_data, timeout=5)
            elif lang == 'c':
                process = subprocess.Popen(['gcc', '-o', 'temp', filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                process.wait()
                process = subprocess.Popen(['./temp'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate(input_data, timeout=5)
            else:
                return JsonResponse({'error': 'Language not supported'})

            if stderr:
                output[idx] = {'output': stderr.strip(), 'status': 'Compilation Error'}
            else:
                if stdout.strip() == expected_output.strip():
                    output[idx] = {'output': stdout.strip(), 'status': 'Pass'}
                else:
                    output[idx] = {'output': stdout.strip(), 'status': 'Fail'}
        except subprocess.TimeoutExpired:
            output[idx] = {'output': '', 'status': 'Timeout'}
    print(output)
    return output