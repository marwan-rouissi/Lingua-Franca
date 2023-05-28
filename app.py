from flask import Flask, render_template, request
import googletrans
from googletrans import Translator

# create a Flask instance
app = Flask(__name__)
# create a Translator instance
translator = Translator()
# save all googletrans API languages in a variable
languages = googletrans.LANGUAGES
# save last dest language used
lastT = []

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',
                           languages_list = languages,
                           curLanguageSource = "select a language",
                           curLanguageTarget = "select a language")

# @app.route("/image.jpg")
# def image():
#     return render_template("image.jpg")

@app.route('/', methods=['POST'])
def index_post():
    textToTranslate = request.form['text']
    sourceLanguage = request.form['FromLanguage']
    targetLanguage = request.form['ToLanguage']
    lastTarget = targetLanguage

    try:
        if sourceLanguage == 'autodetect':
            sourceLanguage = translator.detect(textToTranslate).lang

        else:
            sourceLanguage = request.form['FromLanguage']
            targetLanguage = request.form['ToLanguage']
        

        translatedText = translator.translate(textToTranslate, targetLanguage, sourceLanguage)
        lastT.append(targetLanguage)
        print(lastT)
        print(lastT[-1])
        return render_template('index.html',
                            transText = translatedText.text,
                            textToTrans = textToTranslate,
                            languages_list = languages,
                            curLanguageSource = languages[sourceLanguage],
                            curLanguageTarget = languages[targetLanguage],
                            curSrcLanguage = sourceLanguage,
                            )
    except ValueError:
        if targetLanguage == "":
            return 
        else:
            targetLanguage = lastT[-1]
            print(lastTarget)

        translatedText = translator.translate(textToTranslate, targetLanguage, sourceLanguage)
        return render_template('index.html',
                            transText = translatedText.text,
                            textToTrans = textToTranslate,
                            languages_list = languages,
                            curLanguageSource = languages[sourceLanguage],
                            curLanguageTarget = languages[targetLanguage],
                            curSrcLanguage = sourceLanguage,
                            )