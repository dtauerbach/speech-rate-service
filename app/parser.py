import random
from time import time
from flask import Flask, flash, request, render_template, redirect, url_for
from flaskext.uploads import UploadSet, configure_uploads
import lib.diarize as diarize
app = Flask(__name__)
app.secret_key = 'this is a fake secret key boyyeeeeee'

app.config['UPLOADED_AUDIOS_DEST'] = 'wavs/'
audiofiles = UploadSet('audios', ('wav',))
configure_uploads(app, (audiofiles,))

class Audio(object):
    def __init__(self, filename):
        self.filename = filename
        self.id = int(random.random() * 100000000)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'audio' in request.files:
        timestamp = str(int(time()))
        filename = audiofiles.save(request.files['audio'])
        d = diarize.Diarize('wavs/%s' % filename, timestamp)
        d.split()
        return redirect(url_for('show', id=rec.id))
    return render_template('upload.html')

@app.route('/audio/<id>')
def show(id):
    # audio = Audio.load(id)
    # if audio is None:
    #     abort(404)
    # url = audiofiles.url(audio.filename)
    return render_template('show.html', id=id)


if __name__ == '__main__':
    app.debug = True
    app.run()
