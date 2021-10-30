from rest_framework import serializers


class WeatherSerializer(serializers.Serializer):
    city = serializers.CharField()
    country = serializers.CharField()
    main = serializers.CharField()
    wind = serializers.FloatField()
    pressure = serializers.FloatField()
    humidity = serializers.FloatField()
    dt = serializers.CharField()
