from django.http import HttpResponse
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import F, Value, CharField, JSONField
from django.db.models.functions import Cast
from .compile import compile_by_lang
from .models import User, Problem, ProblemTestCase, ProblemSolutionUser, ProblemType

def index(request):
    return HttpResponse("hey!")


def details(request, enquiry_id):
    return HttpResponse("You are here for %s" % enquiry_id)


def status(request, enquiry_id):
    return HttpResponse("Status of your enquiry")

@csrf_exempt
def create_user(request):
    print(request.POST.get('data'),"asssasas")
    data = json.loads(request.POST.get('data'))
    name = data['name']
    user = User(name=name)
    user.save()
    return JsonResponse({'id': user.id})

@csrf_exempt
def create_problem(request):
    rating = 0
    data = json.loads(request.POST.get('data'))
    name = data['name']
    rating = data['rating']
    problem = data['problem']
    pb_type = data['type']
    pblm = Problem(name=name,rating=rating, problem=problem)
    pblm.save()
    for i in range(len(pb_type)):
        pt =  ProblemType(pid=pblm, type= pb_type[i])
        pt.save()

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
def compile_code_by_pid(request):
    data = json.loads(request.POST.get('data'))
    uid = data['uid']
    pid = data['pid']
    sol = data['sol']
    lang = data['lang']
    pblm = Problem.objects.get(id=pid)
    user = User.objects.get(id=uid)
    user_sol = ProblemSolutionUser(uid=user, pid=pblm, sol=sol)

    user_sol.save()
    tstByPid = ProblemTestCase.objects.filter(pid=pid)
    print(list(tstByPid),"zxcxzc")
    output= compile_by_lang(lang=lang, code=sol, test_cases=list(tstByPid.values()))
    return JsonResponse(output,safe=False)

@csrf_exempt
def compile_code_raw(request):
    print("requueueu")
    data = json.loads(request.POST.get('data'))
    code = data['code']
    lang = data['lang']
    test_cases = data.get('test_cases')
    print(code, lang, test_cases)
    output = compile_by_lang(lang, code, test_cases)
    return JsonResponse(output,safe=False)

def problems_list(request):
    problems = Problem.objects.all().values()
    for i in problems:
        i["type"] = list(ProblemType.objects.filter(pid=i['id']).values())
    return JsonResponse(list(problems), safe=False)


def test_cases_by_pid(pid):
    test_cases = ProblemTestCase.objects.filter(pid=pid).values()
    return list(test_cases)

def get_problem_by_id(request, pid):
    problem = Problem.objects.filter(id=pid).values()[0]
    print(problem,"asdsad")
    problem["type"] = list(ProblemType.objects.filter(pid=problem["id"]).values())
    problem["test_cases"] = test_cases_by_pid(pid)
    return JsonResponse(problem, safe=False)


def get_test_cases_by_pid(request, pid):
    return JsonResponse(test_cases_by_pid(pid), safe=False)