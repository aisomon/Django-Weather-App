import requests
from django.shortcuts import render,get_object_or_404,redirect
from .models import City
from .form import CityForm
# Create your views here.

def home(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=3530e69b4b972b8bd0291c655f01da80"
    errmsg = ''
    msgclass = ''
    msg = ''
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            city_count = City.objects.filter(name=new_city).count()
            if city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    errmsg = "Invalid city name!"  
            else:
                errmsg = "Already the city is added below."
        if errmsg:
            msg = errmsg
            msgclass = "is-danger"
        else:
            msg ="The city is added successfully in database."
            msgclass = "is-success"
    form = CityForm()
    weather = []
    city = City.objects.all()
    for c in city:
        r = requests.get(url.format(c)).json()
        city_weather={
            'city':c,
            'temparature':r['main']['temp'],
            'description':r['weather'][0]['description'],
            'icon':r['weather'][0]['icon'],
        }
        weather.append(city_weather)
    context = {
        "weather":weather,
        "form":form,
        "msg":msg,
        "msgclass":msgclass,
    }
    return render(request,"index.html",context)


def city_delete(request,city_name):
    c = get_object_or_404(City, name=city_name)
    c.delete()
    return redirect('home')