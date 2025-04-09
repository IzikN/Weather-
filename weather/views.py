import requests
from django.shortcuts import render
import datetime

API_KEY = '6c4bb55a4a09f501d60f6181222ea2ca'  # OpenWeather API key

def weather(request):
    context = {'error': None, 'weather': None, 'selected_unit': 'metric'}
    
    if request.method == 'POST':
        city = request.POST.get('city')
        unit = request.POST.get('unit')
        context['selected_unit'] = unit  # Keep the selected unit for re-display

        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units={unit}&appid={API_KEY}"
            response = requests.get(url)
            data = response.json()

            # Debug: print the raw response
            print("API Response:", data)  

            if data['cod'] != 200:
                context['error'] = data.get('message', 'City not found. Please try again.')
            else:
                weather_data = {
                    'city': city.title(),
                    'temperature': round(data['main']['temp'], 1),
                    'unit_symbol': '°C' if unit == 'metric' else '°F',
                    'description': data['weather'][0]['description'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'wind_speed': data['wind']['speed'],
                    'icon': data['weather'][0]['icon'],
                    'updated_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                }
                context['weather'] = weather_data
                context['background'] = get_weather_background(data['weather'][0]['main'])

    return render(request, 'index.html', context)

def get_weather_background(weather_condition):
    weather_images = {
        'Clear': 'clear.jpg',
        'Clouds': 'cloudy.jpg',
        'Rain': 'rain.jpg',
        'Thunderstorm': 'storm.jpg',
        'Snow': 'snow.jpg',
        'Drizzle': 'drizzle.jpg',
        'Mist': 'mist.jpg',
        'Fog': 'fog.jpg',
    }
    return weather_images.get(weather_condition, 'default.jpg')
