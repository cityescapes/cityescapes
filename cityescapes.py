from flask import Flask, jsonify, render_template, request
import requests
import pyunsplash

app = Flask("cityescapes")
port = int(os.environ.get("PORT", 5000))

pu = pyunsplash.PyUnsplash(api_key=os.environ.get("api_key", None))
W_API_KEY = os.environ.get("API_KEY", None)

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

app.run(host='0.0.0.0', port=port, debug=True)
