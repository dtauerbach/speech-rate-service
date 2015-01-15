import os, os.path
from time import time
from pydub import AudioSegment

BASE_DIRECTORY = '/tmp'

class SegmentFinder:
    def __init__(self, wav_file_name, random_token):
        self.wav_file_name = wav_file_name
        os.mkdir(os.path.join(BASE_DIRECTORY, random_token))
        self.seg_file_name = os.path.join(BASE_DIRECTORY, random_token, 'seg.seg')

    def create_segfile(self):
        os.system('/usr/bin/java -Xmx2024m -jar ./app/lib/LIUM_SpkDiarization-4.2.jar --fInputMask=./' + \
                              self.wav_file_name + ' --sOutputMask=' + \
                              self.seg_file_name + ' --doCEClustering  showName')

    def _parse_segfile_line(self, line):
        print line
        split_line = line.split(" ")
        return {"start_time": int(split_line[2]) * 10,
                "duration": int(split_line[3]) * 10,
                "speaker": split_line[7][:-1]}

    def get_event_data(self):
        seg_file = open(self.seg_file_name, 'r')
        return [self._parse_segfile_line(line) for line in seg_file if line[0] != ";"]

class Diarize:
    def __init__(self, wav_file_name, random_token):
        self.wav_file = AudioSegment.from_wav(wav_file_name)
        self.random_token = random_token
        seg_finder = SegmentFinder(wav_file_name, random_token)
        seg_finder.create_segfile()
        self.event_data = seg_finder.get_event_data()

    def split(self):
        clips = {}
        for event in self.event_data:
            start = event["start_time"]
            end = start + event["duration"]
            duration = event["duration"]
            if event["speaker"] in clips.keys():
                clips[event["speaker"]] = [clips[event["speaker"]][0] + self.wav_file[start:end], clips[event["speaker"]][1] + duration]
            else:
                clips[event["speaker"]] = [self.wav_file[start:end], duration]

        for name in clips:
            print "exporting clip " + name
            segment_file_name = os.path.join(BASE_DIRECTORY, self.random_token, name + '.wav')
            clips[name][0].export(segment_file_name, format="wav")
        return clips
