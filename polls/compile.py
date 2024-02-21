import subprocess
from django.http import JsonResponse
import re

pattern = r',(?![^\[]*\])'
def compile_by_lang(lang:str,code:str, test_cases:list[dict[str,str]]):
    filename = 'temp.' + lang
    stdout, stderr = '', ''
    with open(filename, 'w') as file:
        file.write(code)

    output = {}
    if lang == 'py':
                # process = subprocess.Popen(['python', filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                # stdout, stderr = process.communicate(input_data, timeout=5)
        output = run_user_function(code, 'main', test_cases)
        return output
    for idx, test_case in enumerate(test_cases):
        print(idx,test_case,"sadsads")
        input_data = test_case['inp']
        expected_output = test_case['out']

        try:
            if lang == 'java':
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



def run_user_function(user_code, function_name, test_cases):
    user_namespace = {}
    res = []
    exec(user_code, user_namespace)
    user_function = user_namespace.get(function_name)
    if not callable(user_function):
        print(f"Function '{function_name}' not found in user code.")
        return
    for test_case in test_cases:
        args = []
        input_data = re.split(pattern, test_case["inp"])
        for arg in input_data:
            if arg.isdigit():
                args.append(int(arg))
            else:
                args.append(arg)
        arr_index = None
        for i, arg in enumerate(args):
            if isinstance(arg, list):  # Check if the argument is a list (array)
                arr_index = i
                break
        if arr_index is not None:  # If an array is present, concatenate it into a single string argument
            arr = args[arr_index]
            args[arr_index] = ",".join(map(str, arr))
        try:
            actual_output = user_function(*args)  # Pass x and the arguments as separate arguments to the user function
            expected_output = test_case['out']  # Assuming you have expected output in your test case dictionary
            if actual_output == expected_output or str(actual_output) == expected_output:
                print(f"Test case passed: Input: {input_data}, Output: {actual_output}")
                res.append({"status": "Pass", "output": actual_output})
            else:
                print(f"Test case failed: Input: {input_data}, Expected Output: {expected_output}, Actual Output: {actual_output}")
                res.append({"status": "Fail", "output": actual_output})

        except Exception as e:
            print(f"Error occurred while running test case: {input_data}, Error: {e}")

    return res