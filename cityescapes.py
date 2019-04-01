from flask import Flask, jsonify, render_template, request
import requests
import pyunsplash
import os

app = Flask("cityescapes")
port = int(os.environ.get("PORT", 5000))

pu = pyunsplash.PyUnsplash(api_key=os.environ.get("IMAGE_API_KEY", None))
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", None)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/image")
def getImages(searchTerm):
    search = pu.search(type_="photos", query=searchTerm, per_page=20)
    links = []
    for photo in search.entries:
        photoURL = photo.body.get("urls").get("regular")
        links.append(photoURL)
    return links

def getWeather(searchTerm):
    endpoint = "http://api.openweathermap.org/data/2.5/weather"
    payload = {"q": searchTerm, "units": "metric", "appid": WEATHER_API_KEY}
    response = requests.get(endpoint, params=payload)
    data = response.json()

    if response.status_code == 404:
        return None

    temperature = data["main"]["temp"]
    condition = data["weather"][0]["main"]
    return{"temperature": temperature, "condition": condition}

@app.route("/result", methods=["POST"])
def result():
    search = request.form["user_search"]
    weather = getWeather(search)
    images = getImages(search)
    return render_template("result.html",images=images,search=search,weather=weather)

app.run(host='0.0.0.0', port=port, debug=True)
