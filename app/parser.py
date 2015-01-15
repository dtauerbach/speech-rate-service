import random, numpy
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
        total_secs = sum(length_dict.values())
        # filter out things less than 5% of total and come up with percentage breakdown
        length_dict = dict((k, (v,v/float(total_secs))) for k, v in length_dict.items() if v/float(total_secs) > 0.05)
        num_participants = len(length_dict)
        fair_distribution = numpy.array([1/float(num_participants) for i in xrange(num_participants)])
        current_distribution = numpy.array([v[1] for v in length_dict.values()])
        l2_distance = numpy.linalg.norm(current_distribution - fair_distribution)

        return render_template('show.html', id=timestamp, clip_stats=length_dict, balance_score=l2_distance)
    return render_template('upload.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
