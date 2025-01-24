import requests
from flask import Flask, render_template, request, redirect, flash
import os
urlt = "https://api-b2b.backenster.com/b1/api/v3/translate"
urlc = "https://api-b2b.backenster.com/b1/api/v3/getLanguages?platform=api&code=en_GB"

app = Flask(__name__)



headersc = {
        "accept": "application/json",
        "Authorization": os.environ.get('FLASK_KEY')
    }

headerst = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "a_FVCr2bXlBaJEvrgvNrp7wlgHlJCd8C8rvt2sZqaxd2DScw8acqifRUfDTYTB0OIdUodg2ffaXscbzso8"
    }



def translator(word,to,fromm):
    global urlt
    global headerst

    payload = {
        "platform": "api",
        "to": to,
        "from": fromm,
        "data": word
    }

    response = requests.post(urlt, json=payload, headers=headerst)

    gett = response.json()

    word = gett.get("result")
    lan = gett.get("from")
    return word, lan

def getCountryCode(text):
    global urlc
    global headersc
    global languages
    response = requests.get(urlc, headers=headersc)

    universe = response.json()
    earth = universe.get("result")
    for country in earth:
        language = country['englishName']
        alphaCode = country['code_alpha_1']
        if language.lower() == text.lower() or alphaCode.lower() == text.lower() :
            code = country['full_code']
            return code, language, alphaCode

def detect(text):
    url = "https://api-gl.lingvanex.com/language/translate/v2/detect"

    payload = {"q": text}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": os.environ.get('FLASK_KEY')
    }

    response = requests.post(url, json=payload, headers=headers)

    dictt = response.json()
    detections = dictt['data']
    deeper = detections['detections']
    evenDeeper = deeper[0]
    evenEvenDeeper = evenDeeper[0]
    language = evenEvenDeeper['language']
    return language






@app.route('/')
def home():
    return render_template("index.html")

@app.route('/translate',methods = ['POST'])
def translate():
    choice1 = request.form.get("choice1")
    choice2 = request.form.get("choice2")
    text = request.form.get("text")

    if not choice2 or not text:
        flash('Please fill in all required fields.')
        return redirect('/')

    if choice1 == "Detect Language":
        language = detect(text)
        countryCode1, english1, code1 = getCountryCode(language)
        choice1 = english1
    else:
        countryCode1, english1, code1 = getCountryCode(choice1)


    language = detect(text)
    if language != code1:
        countryCode1, english1, code1 = getCountryCode(language)
        choice1 = english1
    countryCode2, english2, code2 = getCountryCode(choice2)

    new, lan = translator(text,countryCode2,countryCode1)



    return render_template("index.html", text = text, translated = new, choice1 = choice1, choice2 = choice2)










if __name__ == "__main__":
    app.run(debug=False)