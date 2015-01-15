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

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'audio' in request.files:
        timestamp = str(int(time()))
        filename = audiofiles.save(request.files['audio'])
        d = diarize.Diarize('wavs/%s' % filename, timestamp)
        clips = d.split()
        length_dict = {k: int(v[1]/1000.) for k,v in clips.items()}
        return render_template('show.html', id=timestamp, clip_stats=length_dict)
    return render_template('upload.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
