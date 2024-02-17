from django.shortcuts import HttpResponse

# Create your views here.


def index(request):
    if request.method == "GET":
        return HttpResponse(("Index page."))


def login(request):
    if request.method == "GET":
        return HttpResponse("Login app index.")
