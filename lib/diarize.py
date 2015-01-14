import os
from time import time
from pydub import AudioSegment



class SegmentFinder:
    def __init__(self, wav_file_name):
        self.wav_file_name = wav_file_name
        self.seg_file_name = str(int(time())) + 'seg.seg'

    def create_segfile(self):
        os.system('/usr/bin/java -Xmx2024m -jar ./LIUM_SpkDiarization-4.2.jar --fInputMask=./' + \
                              self.wav_file_name + ' --sOutputMask=./' + \
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
    def __init__(self, wav_file_name):
        self.wav_file = AudioSegment.from_wav(wav_file_name)
        seg_finder = SegmentFinder('ppl2.wav')
        seg_finder.create_segfile()
        self.event_data = seg_finder.get_event_data()

    def split(self):
        clips = {}
        for event in self.event_data:
            start = event["start_time"]
            end = start + event["duration"]
            if event["speaker"] in clips.keys():
                clips[event["speaker"]] = clips[event["speaker"]] + self.wav_file[start:end]
            else:
                clips[event["speaker"]] = self.wav_file[start:end]

        for name in clips:
            print "exporting clip " + name
            clips[name].export(name + ".wav", format="wav")

# example usage
# s = Diarize('ppl2.wav')
# s.split()
