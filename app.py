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

# render the created template (index.html)
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',
                           languages_list = languages,
                           curLanguageSource = "select a language",
                           curLanguageTarget = "select a language")

@app.route('/', methods=['POST'])
def index_post():
    textToTranslate = request.form['text']
    sourceLanguage = request.form['FromLanguage']
    targetLanguage = request.form['ToLanguage']

    try:
        if sourceLanguage == 'autodetect':
            sourceLanguage = translator.detect(textToTranslate).lang

        else:
            sourceLanguage = request.form['FromLanguage']
            targetLanguage = request.form['ToLanguage']
        
        # render template and apply modification on the targeted fields
        translatedText = translator.translate(textToTranslate, targetLanguage, sourceLanguage)
        lastT.append(targetLanguage)
    
        return render_template('index.html',
                            transText = translatedText.text,
                            textToTrans = textToTranslate,
                            languages_list = languages,
                            curLanguageSource = languages[sourceLanguage],
                            curLanguageTarget = languages[targetLanguage],
                            curSrcLanguage = sourceLanguage,
                            )
    except ValueError:
        # if no language is selected on the first traduction render the basic template
        if targetLanguage == "" and lastT == []:
            return render_template('index.html',
                           languages_list = languages,
                           curLanguageSource = "select a language",
                           curLanguageTarget = "select a language")
        # else, targeted language is the last one selected
        else:
            targetLanguage = lastT[-1]

        translatedText = translator.translate(textToTranslate, targetLanguage, sourceLanguage)
        return render_template('index.html',
                            transText = translatedText.text,
                            textToTrans = textToTranslate,
                            languages_list = languages,
                            curLanguageSource = languages[sourceLanguage],
                            curLanguageTarget = languages[targetLanguage],
                            curSrcLanguage = sourceLanguage,
                            )