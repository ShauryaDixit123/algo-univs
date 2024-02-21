from django.http import HttpResponse
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import F, Value, CharField, JSONField
from django.db.models.functions import Cast
from .compile import compile_by_lang
from .models import User, Problem, ProblemTestCase, ProblemSolutionUser, ProblemType,ProblemSolutionTestCase
import textwrap


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
    problem = data['problem']
    pb_type = data['type']
    test_cases = data['test_cases']
    pblm = Problem(name=name,rating=rating, problem=problem)
    pblm.save()
    for i in range(len(pb_type)):
        pt =  ProblemType(pid=pblm, type= pb_type[i])
        pt.save()
    for i in range(len(test_cases)):
        tc = ProblemTestCase(pid=pblm, inp=test_cases[i]["inp"], out=test_cases[i]["out"])
        tc.save()
    return JsonResponse({'pid': pblm.id})

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
    all_psed = True
    uid = data['uid']
    pid = data['pid']
    sol = data['sol']
    lang = data['lang']
    pblm = Problem.objects.get(id=pid)
    user = User.objects.get(id=uid)
    sol = textwrap.dedent(sol)
    user_sol = ProblemSolutionUser.objects.filter(uid=user, pid=pblm)
    if len(user_sol) > 0:
        user_sol.update(sol=sol)
    else:
        user_sol = ProblemSolutionUser(uid=user, pid=pblm, sol=sol)
        user_sol.save()
        user_sol = ProblemSolutionUser.objects.filter(uid=user, pid=pblm)
    tstByPid = ProblemTestCase.objects.filter(pid=pid)
    result = compile_by_lang(lang=lang, code=sol, test_cases=list(tstByPid.values()))
    print(result,"asdsads")
    del_test_case_result(user_sol[0].id)
    if lang == "py":
        for i in range(len(list(tstByPid.values()))):
            psed = result[i]["status"] == "Pass"
            if not psed:
                all_psed = False
            tid = get_test_case_by_id(list(tstByPid.values())[i]["id"])
            pblm_sol_tst = ProblemSolutionTestCase(attempted=True, passed=psed, sid=user_sol[0], tid=tid[0])
            pblm_sol_tst.save()
        test_case_his = ProblemSolutionTestCase.objects.filter(sid=user_sol.values()[0]["id"]).values()
        return JsonResponse({"result" : list(test_case_his), "passed" : all_psed},safe=False)
    result = [value for key, value in result.items()]
    for i in range(len(list(tstByPid.values()))):
        psed = result[i]["status"] == "Pass"
        if not psed:
            all_psed = False
        tid = get_test_case_by_id(list(tstByPid.values())[i]["id"])
        pblm_sol_tst = ProblemSolutionTestCase(attempted=True, passed=psed, sid=user_sol[0], tid=tid[0])
        pblm_sol_tst.save()
    test_case_his = ProblemSolutionTestCase.objects.filter(sid=user_sol.values()[0]["id"]).values()
    return JsonResponse({"result" : list(test_case_his), "passed" : all_psed},safe=False)

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

@csrf_exempt
def user_solution_history_by_pid(request):
    data = json.loads(request.POST.get('data'))
    pid = data['pid']
    uid = data['uid']
    pb_sol = ProblemSolutionUser.objects.filter(pid=pid,uid=uid).values()
    if len(pb_sol) == 0:
        return JsonResponse({'error': 'No solution found'})
    pb_sol = pb_sol[0]
    test_case_his = ProblemSolutionTestCase.objects.filter(sid=pb_sol["id"]).values()
    pb_sol["tst_hstry"] = list(test_case_his)
    return JsonResponse(pb_sol, safe=False)

def get_test_case_by_id(tid):
    return ProblemTestCase.objects.filter(id=int(tid))
    
def del_test_case_result(sid):
    return ProblemSolutionTestCase.objects.filter(sid=sid).delete()

@csrf_exempt
def create_rating(request):
    data = json.loads(request.POST.get('data'))
    rating = float(data['rating'])
    uid =  data['uid']
    pid = data['pid']
    pblmSu = ProblemSolutionUser.objects.get(uid=uid, pid=pid)
    pblmSu.rating = rating
    pblm = Problem.objects.get(id=pid)
    if pblm.rating == 0:
        pblm.rating = rating
    else:
        pblm.rating  = (pblm.rating + rating)/2
    pblmSu.save()
    pblm.save()
    return JsonResponse({'status': 'success'})

def get_prblms_attempted_by_user(request, uid):
    pb_sol = ProblemSolutionUser.objects.filter(uid=uid).values()
    for i in pb_sol:
        print(i,"dsdas")
        pblm = Problem.objects.get(id=i["pid_id"]) 
        i["name"] = pblm.name
        i["rating"] = pblm.rating
        i["des"] = pblm.des

    return JsonResponse(list(pb_sol), safe=False)