from django.http import HttpResponse
# Create your views here.
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, Problem

def index(request):
    return HttpResponse("hey!")


def details(request, enquiry_id):
    return HttpResponse("You are here for %s" % enquiry_id)


def list(request, user_id):
    return HttpResponse("Here is the list of all enquiry by user:- %s" % user_id)


def status(request, enquiry_id):
    return HttpResponse("Status of your enquiry")

@csrf_exempt
def create_user(request):
    data = json.loads(request.POST.get('data'))
    name = data['name']
    user = User(name=name)
    user.save()
    return JsonResponse({'id': user.id})

@csrf_exempt
def create_problem(request):
    rating = 0
    data = json.loads(request.POST.get('data'))
    lang = data['lang']
    rating = data['rating']
    problem = data['problem']
    problem = Problem(lang=lang, rating=rating, problem=problem)
    problem.save()
    return JsonResponse({'pid': problem.id})

@csrf_exempt
def compile_code(request):
    data = json.loads(request.POST.get('data'))
    code = data['code']
    language = data['language']
    test_cases = data.get('test_cases')
    print(code, language, test_cases)
    filename = 'temp.' + language
    with open(filename, 'w') as file:
        file.write(code)

    output = {}
    for idx, test_case in enumerate(test_cases):
        input_data = test_case['input']
        expected_output = test_case['output']

        try:
            if language == 'py':
                process = subprocess.Popen(['python', filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            elif language == 'java':
                process = subprocess.Popen(['java', filename[:-3]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            elif language == 'c':
                process = subprocess.Popen(['gcc', '-o', 'temp', filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                process.wait()
                process = subprocess.Popen(['./temp'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            else:
                return JsonResponse({'error': 'Language not supported'})

            stdout, stderr = process.communicate(input_data, timeout=5)
            if stderr:
                output[idx] = {'output': stderr.strip(), 'status': 'Compilation Error'}
            else:
                if stdout.strip() == expected_output.strip():
                    output[idx] = {'output': stdout.strip(), 'status': 'Pass'}
                else:
                    output[idx] = {'output': stdout.strip(), 'status': 'Fail'}
        except subprocess.TimeoutExpired:
            output[idx] = {'output': '', 'status': 'Timeout'}

    return JsonResponse(output)