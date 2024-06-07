from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from app.tasks import getData
# from celery.result import AsyncResult

import uuid

tasks = []

def index(request):
    context = {}

    context["job_id_1"] = ""
    context["job_id_2"] = ""
    context["job_id_3"] = ""

    if request.method == "POST":
        options = request.POST.getlist('coin')
        job_id = uuid.uuid4()
        for option in options:
            if option == "duko":
                context["job_id_1"] = job_id
                output = getData.delay(option).get()
                tasks.append({"coin": option, "output": output})
            elif option == "notcoin":
                context["job_id_2"] = job_id
                output = getData.delay(option).get()
                tasks.append({"coin": option, "output": output})
            elif option == "gorilla-token":
                context["job_id_3"] = job_id
                output = getData.delay(option).get()
                tasks.append({"coin": option, "output": output})
    
    return render(request, "index.html", context)

def get_status(request, id):
    print(tasks)
    return JsonResponse({"job_id": id, "tasks": tasks})
