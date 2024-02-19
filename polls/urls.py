from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:enquiry_id>', views.details, name="details"),
    path('<int:enquiry_id>', views.status, name="status"),
    path('compile', views.compile_code_raw, name="compile_code"),
    path('create_user', views.create_user, name="create_user"),
    path('create_problem', views.create_problem, name="create_problem"),
    path('create_test_case', views.create_test_case, name="create_test_case"),
    path("problem_list/", views.problems_list, name="problem_list"),
    path("problem/<int:pid>", views.get_problem_by_id, name="problem"),
    path("compile_code_by_pid", views.compile_code_by_pid, name="compile_code_by_pid"),
    path("user_sol", views.user_solution_history_by_pid, name="user_sol"),
    path("rate_problem", views.create_rating, name="rate_problem"),
    path("user_attempts/<int:uid>", views.get_prblms_attempted_by_user, name="problem_attempted_by_user"),
    # api's above , frontEnd below! Here will be using just one html!
    
    path('react-web/', view=TemplateView.as_view(template_name='polls/static_react.html')),

]

# {
#         "code" : "print(1+7)",
#         "language" : "py",
#         "test_cases" : [{
#             "input" : "1",
#             "output" : "2"
#         }]
# }

# {
# "name" : "add 2 number",
#  "lang" : "python",
# "problem" : "print(1+1)",
# "rating":0
# }