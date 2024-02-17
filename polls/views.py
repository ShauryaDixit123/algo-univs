from django.http import HttpResponse
# Create your views here.


def index(request):
    return HttpResponse("hey!")


def details(request, enquiry_id):
    return HttpResponse("You are here for %s" % enquiry_id)


def list(request, user_id):
    return HttpResponse("Here is the list of all enquiry by user:- %s" % user_id)


def status(request, enquiry_id):
    return HttpResponse("Status of your enquiry")
