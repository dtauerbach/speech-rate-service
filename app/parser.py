from flask import Flask, request, render_template, redirect, url_for
from flaskext.uploads import UploadSet
app = Flask(__name__)

audios = UploadSet('audios')

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'audio' in request.files:
        filename = audios.save(request.files['audio'])
        rec = Audio(filename=filename, user=g.user.id)
        rec.store()
        flash("Audio saved.")
        return redirect(url_for('show', id=rec.id))
    return render_template('upload.html')

@app.route('/audio/<id>')
def show(id):
    audio = Audio.load(id)
    if audio is None:
        abort(404)
    url = audios.url(audio.filename)
    return render_template('show.html', url=url, audio=audio)

if __name__ == '__main__':
    app.debug = True
    app.run()
