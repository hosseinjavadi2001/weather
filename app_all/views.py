from itertools import count

from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import redis
import json
import time

from app_all.models import Weather
from app_all.serializers import WeatherSerializer

redis_host = 'localhost'
redis_port = '6379'
redis_pass = ''


@api_view(['GET'])
def weather_api(request, *args, **kwargs):
    if str(kwargs['city']) == "None":
        return Response({"None": 'none'})

    city = str(kwargs['city']).lower()
    rd = redis.Redis(host=redis_host, port=redis_port, password=redis_pass)
    if rd.exists(city) == 0:
        response_data = Weather.objects.filter(city__icontains=city).first()
        if response_data is None:
            data_w = requests.get(
                f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=9dd1ba5586b926aa6d998e5ebcc8418c'
            ).json()
            print(data_w['cod'])
            if str(data_w['cod']) != '200':
                print(data_w['cod'])
                return Response({
                    "message": data_w['message']
                })
            country = data_w['sys']['country']
            main = data_w['weather'][0]['main']
            wind = data_w['wind']['speed']
            pressure = data_w['main']['pressure']
            humidity = data_w['main']['humidity']
            dt = data_w['dt']
            Weather.objects.create(
                city=city,
                country=country,
                main=main,
                wind=wind,
                pressure=pressure,
                humidity=humidity,
                dt=time.ctime(int(dt))
            )
            rd.hset(city, "country", country)
            rd.hset(city, "main", main)
            rd.hset(city, "wind", wind)
            rd.hset(city, "pressure", pressure)
            rd.hset(city, "humidity", humidity)
            rd.hset(city, "dt", time.ctime(int(dt)))
            response_data = {
                "country": country,
                "main": main,
                "wind": wind,
                "pressure": pressure,
                "humidity": humidity,
                "dt": time.ctime(int(dt))
            }
            return Response(response_data)
        else:
            rd.hset(city, "country", response_data.country)
            rd.hset(city, "main", response_data.main)
            rd.hset(city, "wind", response_data.wind)
            rd.hset(city, "pressure", response_data.pressure)
            rd.hset(city, "humidity", response_data.humidity)
            rd.hset(city, "dt", response_data.dt)
            response_data = {
                "country": rd.hget(city, "country"),
                "main": rd.hget(city, "main"),
                "wind": rd.hget(city, 'wind'),
                "pressure": rd.hget(city, "pressure"),
                "humidity": rd.hget(city, "humidity"),
                "dt": rd.hget(city, "dt")
            }
            return Response(response_data)
    else:
        response_data = {
            "country": rd.hget(city, "country"),
            "main": rd.hget(city, "main"),
            "wind": rd.hget(city, 'wind'),
            "pressure": rd.hget(city, "pressure"),
            "humidity": rd.hget(city, "humidity"),
            "dt": rd.hget(city, "dt")
        }
        return Response(response_data)
