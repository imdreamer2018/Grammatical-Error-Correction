import os
from flask import Flask, request, render_template, redirect
from src.checker import GrammarCorrection

UPLOAD_FOLDER = 'data/predict_for_file/'
app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'panda sandal buggy broken rock'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def serve():
    return render_template("index.html")


@app.route('/file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            print('no filename')
            return redirect(request.url)

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'input.txt'))
        with open(os.path.join(app.config['UPLOAD_FOLDER'], 'input.txt'), 'r') as f:
            text = f.readlines()
        grammar_correction = GrammarCorrection()
        grammar_correction.correct_sentence_by_file()
        with open(os.path.join(app.config['UPLOAD_FOLDER'], 'output.txt'), 'r') as f:
            corrected = f.readlines()
        return render_template('index.html', correct="".join(corrected), wrong="".join(text))

    return render_template('index.html')


@app.route('/text', methods=['GET', 'POST'])
def upload_text():
    if request.method == 'POST' and 'textupload' in request.form:
        text = request.form['textupload']
        grammar_correction = GrammarCorrection()
        corrected = grammar_correction.correct_sentence(text)

        return render_template('index.html', correct=corrected, wrong=text)

    return render_template('index.html')


@app.route('/api/texts', methods=['POST'])
def grammar_correction_text():
    content = request.json
    text = content['text']
    grammar_correction = GrammarCorrection()
    return grammar_correction.correct_sentence(text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='21047', debug=True)
