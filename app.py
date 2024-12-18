from flask import Flask, jsonify, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Weatherstack API configuration
WEATHERSTACK_API_KEY = os.getenv('WEATHERSTACK_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather/<city>', methods=['GET'])
def get_weather(city):
    try:
        # Get the 7-day weather forecast
        response = requests.get(
            f'http://api.weatherstack.com/forecast',
            params={'access_key': WEATHERSTACK_API_KEY, 'query': city, 'forecast_days': 7}
        )
        response.raise_for_status()  # Raise an error for bad responses
        weather_data = response.json()

        # Check if the response contains an error
        if 'error' in weather_data:
            return jsonify({'error': weather_data['error']['info']}), 400

        return jsonify(weather_data['forecast'])
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/current/<city>', methods=['GET'])
def get_current_weather(city):
    try:
        # Get the current weather
        response = requests.get(
            f'http://api.weatherstack.com/current',
            params={'access_key': WEATHERSTACK_API_KEY, 'query': city}
        )
        response.raise_for_status()  # Raise an error for bad responses
        current_weather_data = response.json()

        # Check if the response contains an error
        if 'error' in current_weather_data:
            return jsonify({'error': current_weather_data['error']['info']}), 400

        return jsonify(current_weather_data['current'])
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)