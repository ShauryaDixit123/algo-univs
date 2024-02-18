from django.http import HttpResponse
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .compile import compile_by_lang
from .models import User, Problem, ProblemTestCase, ProblemSolutionUser

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
def create_test_case(request):
    data = json.loads(request.POST.get('data'))
    pid = data['pid']
    inp = data['inp']
    out = data['out']
    pblm = Problem.objects.get(id=pid)
    test = ProblemTestCase(pid=pblm, inp=inp, out=out)
    test.save()
    return JsonResponse({'status': 'success'})

@csrf_exempt
def submit_and_run_solution(request):
    data = json.loads(request.POST.get('data'))
    uid = data['uid']
    pid = data['pid']
    sol = data['sol']
    pblm = Problem.objects.get(id=pid)
    user = User.objects.get(id=uid)
    user_sol = ProblemSolutionUser(uid=user, pid=pblm, sol=sol)

    user_sol.save()
    tstByPid = ProblemTestCase.objects.filter(pid=pid)
    return JsonResponse({'status': 'success'})


@csrf_exempt
def compile_code(request):
    print("requueueu")
    data = json.loads(request.POST.get('data'))
    code = data['code']
    lang = data['lang']
    test_cases = data.get('test_cases')
    print(code, lang, test_cases)
    output = compile_by_lang(lang, code, test_cases)
    return JsonResponse(output,safe=False)