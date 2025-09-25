#Python modules
from typing import Any
from datetime import datetime
import pytz

#Django modules
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

# WELCOME
def welcome(request):
    return render(request, 'welcome.html')

#Users page
def users(request):
    users_list = [
        {"full_name": "Alice Johnson", "age":25},
        {"full_name": "Alex Morgan", "age":21},
        {"full_name": "Justin Smith", "age":29},
    ]
    return render(request, 'users.html', {"users": users_list})

# City time page
def city_time(request):
    cities = {
        "Almaty": "Asia/Almaty",
        "Calgary": "America/Edmonton",
        "Moscow": "Europe/Moscow",
        "UTC": "UTC"
    }
    selected_city= request.GET.get("city")
    current_time = None

    if selected_city and selected_city in cities:
        tz = pytz.timezone(cities[selected_city])
        current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    return render (request, "city_time.html",{
        "cities": cities.keys(),
        "selected_city":selected_city,
        "current_time": current_time,
    })

#Counter
counter_value = 0

def counter(request):
    global counter_value
    if request.method == "POST":
        if "increment" in request.POST:
            counter_value +=1
        elif "reset" in request.POST:
            counter_value = 0
        return redirect("counter")
    
    return render(request, "counter.html", {"counter": counter_value})