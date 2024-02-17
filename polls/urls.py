from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:enquiry_id>', views.details, name="details"),
    path('<int:user_id>', views.list, name="quote_list"),
    path('<int:enquiry_id>', views.status, name="status"),
    path('compile', views.compile_code, name="compile_code"),
    path('create_user', views.create_user, name="create_user"),
    path('create_problem', views.create_problem, name="create_problem"),
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