from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:enquiry_id>', views.details, name="details"),
    path('<int:user_id>', views.list, name="quote_list"),
    path('<int:enquiry_id>', views.status, name="status"),

    # api's above , frontEnd below! Here will be using just one html!
    
    path('react-web/', view=TemplateView.as_view(template_name='polls/static_react.html')),
]
