from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from .models import LongToShort, linkAnalytics
import jsonpickle
import requests
import json


# Create your views here.
def hello_world(request):
    return HttpResponse("Helllo how are you!!")

def task(request):
    context={"year":"2023","attendees":["Adi","Rishabh","Nikesh","sarthak"]}

    return render(request,"task.html",context)

def home_page(request):
    # print("Sahi hai bc")
    context = {"submitted":False,
               "error": False}
    
    if request.method=="POST":
        # print(request.POST)
        data = request.POST 
        long_url = data['longurl']
        custom_name = data['custom_name']
        # print(long_url, custom_name)
        
        try:
            
            context["long_url"] = long_url
            context["custom_name"] = request.build_absolute_uri() +"url/"+custom_name
            context["submitted"] = True

            obj = LongToShort(long_url = long_url, custom_name = custom_name)
            context["clicks"] = obj.visit_count
            obj.save()
            context["date"] = obj.created_date
            context['obj'] = obj
            print(context)
            print(long_url, custom_name)
        except:
            context["error"] = True
            # return HttpResponse("Invalid Alias")
    else:
        print("USer didnkt submit yet")
       
    return render(request,"index.html", context)


def redirect_url(request, customname):
    row = LongToShort.objects.filter(custom_name = customname)
    if len(row) == 0:
        return HttpResponse("This Alias doesn't exist")
    obj = row[0] 
    long_url = obj.long_url
    obj.visit_count += 1
    obj.save()
    custom_name = customname 
    country_name = getCountry(request)
    link = linkAnalytics(custom_name = customname, country = country_name)
    link.save()
    print(link)
    return redirect(long_url)


def analytics(request):
    rows = LongToShort.objects.all()
    context = {
        'rows' : rows,
    }
    
    return render(request, 'analyatics.html', context)


def graphs(request):
    rows = LongToShort.objects.all()
    context = {
        "rows" :rows,
    }
    
    return render(request, 'graphs.html', context)

def error_url(request):
    return HttpResponse("<h1>Wrong URL</h1>")


def link_analytics(request, customname):
    print("Inside linkAnalytics", customname)
    rows = linkAnalytics.objects.filter(custom_name = customname)
    print(rows)
    # if len(rows) == 0:
    #     return HttpResponse("This Alias doesn't exist")
    countries = dict()
    for row in rows:
        countries[row.country] = countries.get(row.country, 0) + 1 
        
    print(countries)
    
    # context = countries

    return render(request, 'singleLinkAnalysis.html', {'context':countries})

def getCountry(request):
    print("geolactions")
    ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)
    res = requests.get('http://ip-api.com/json/'+ip_data["ip"])
    location_data_one = res.text 
    location_data = json.loads(location_data_one)
    print(location_data)
    return location_data['country']
    
