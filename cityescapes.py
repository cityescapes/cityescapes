from flask import Flask, jsonify, render_template, request
import requests
import pyunsplash

pu = pyunsplash.PyUnsplash(api_key='34e948ce5f96be47a8a3bf8ffc94ee01dfc630bb83173bf8e1746733a4ace054')

API_KEY = "e3e43d3fd3b29fa08c734d0146a9d0a0"

app = Flask("cityescapes")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/image")
def getImages(searchTerm):
    search = pu.search(type_="photos", query=searchTerm)
    links = []
    for photo in search.entries:
        photoURL = photo.body.get("urls").get("regular")
        links.append(photoURL)
    return links

def getWeather(searchTerm):
    endpoint = "http://api.openweathermap.org/data/2.5/weather"
    payload = {"q": searchTerm, "units": "metric", "appid": API_KEY}
    response = requests.get(endpoint, params=payload)
    data = response.json()
    temperature = data["main"]["temp"]
    condition = data["weather"][0]["main"]
    return{"temperature": temperature, "condition": condition}

@app.route("/result", methods=["POST"])
def result():
    search = request.form["user_search"]
    weather = getWeather(search)
    images = getImages(search)
    print weather
    return render_template("index.html",images=images,search=search,weather=weather)

app.run(debug=True)
