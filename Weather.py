from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)
API_KEY = "YOUR WEATHER API"  # Replace with your OpenWeatherMap API key

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>🌐 SHIN X Weather App</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background: black;
            color: #00ff00;
            margin: 0;
            padding: 0;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }
        .container {
            background: rgba(0, 0, 0, 0.8);
            padding: 2rem;
            border-radius: 10px;
            max-width: 500px;
            width: 95%;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
            animation: fadeIn 1s ease-in-out;
        }
        h2 {
            text-align: center;
            margin-bottom: 1rem;
            animation: blink 1s infinite;
        }
        input, button {
            width: 100%;
            padding: 12px;
            margin-top: 10px;
            border: 2px solid #00ff00;
            border-radius: 5px;
            background: black;
            color: #00ff00;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus, button:hover {
            border-color: #ffcc00;
            outline: none;
        }
        button {
            cursor: pointer;
            background: black;
            transition: background 0.3s;
        }
        button:hover {
            background: #00ff00;
            color: black;
        }
        .map {
            margin-top: 1rem;
        }
        iframe {
            width: 100%;
            height: 200px;
            border: none;
            border-radius: 5px;
        }
        .result { 
            margin-top: 1.5rem; 
            text-align: center; 
        }
        .error { 
            color: #ff0000; 
            font-weight: bold; 
            text-align: center; 
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }
    </style>
    <script>
        function getLocation() {
            navigator.geolocation.getCurrentPosition(function(pos) {
                let lat = pos.coords.latitude;
                let lon = pos.coords.longitude;
                document.getElementById('location_input').value = lat + ',' + lon;
                document.getElementById('weatherForm').submit();
            }, function(err) {
                alert("Location access denied or not available.");
            });
        }
    </script>
</head>
<body>
    <div class="container">
        <h2>🌐 SHIN X Weather App</h2>
        <form method="POST" id="weatherForm">
            <input type="text" name="city" id="location_input" placeholder="Enter city, village or lat,lon" required>
            <button type="submit">Check Weather</button>
            <button type="button" onclick="getLocation()">📍 Use My Location</button>
        </form>

        {% if weather %}
        <div class="result">
            <h3>📍 Weather in {{ weather.city }}:</h3>
            <p>🌡️ Temperature: {{ weather.temperature }} °C</p>
            <p>💧 Humidity: {{ weather.humidity }}%</p>
            <p>⚡ Pressure: {{ weather.pressure }} hPa</p>
            <p>☁️ Description: {{ weather.description }}</p>
        </div>

        <div class="map">
            <h4>🗺️ Location Map:</h4>
            <iframe src="https://maps.google.com/maps?q={{ lat }},{{ lon }}&z=12&output=embed"></iframe>
        </div>
        {% elif error %}
        <div class="result error">❌ {{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
"""



def fetch_weather(city_or_coords):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # Check if input is coordinates
    if "," in city_or_coords and all(x.strip().replace(".", "").replace("-", "").isdigit() for x in city_or_coords.split(",")):
        lat, lon = map(str.strip, city_or_coords.split(","))
        url = f"{base_url}lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    else:
        city = city_or_coords.strip()
        url = f"{base_url}q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") == 200:
            coord = data["coord"]
            weather = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "description": data["weather"][0]["description"].capitalize()
            }
            return weather, None, coord["lat"], coord["lon"]
        else:
            return None, data.get("message", "Unknown error"), None, None
    except Exception as e:
        return None, str(e), None, None

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    lat = lon = None

    if request.method == "POST":
        user_input = request.form.get("city", "")
        if user_input:
            weather, error, lat, lon = fetch_weather(user_input)

    return render_template_string(HTML_TEMPLATE, weather=weather, error=error, lat=lat, lon=lon)

if __name__ == "__main__":
    app.run(debug=True, port=5050)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
