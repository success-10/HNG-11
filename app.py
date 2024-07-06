from flask import Flask, request, jsonify
import requests
from config import OPENWEATHER_API_KEY, IPINFO_TOKEN


app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Guest')
    
    geo_request = requests.get(f'https://ipinfo.io?token={IPINFO_TOKEN}')
    geo_data = geo_request.json()
    location = geo_data.get("city")
    client_ip = geo_data.get("ip")

    # Use OpenWeather to get temperature
    weather_request = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric')
    weather_data = weather_request.json()
    temperature = weather_data.get('main', {}).get('temp', 'Unknown')
    
    
    response = {
        "client_ip": client_ip,
        "location": location,
        "greeting": f"Hello, {visitor_name}! The temperature is {temperature} degrees Celsius in {location}"
    }
    return jsonify(response)