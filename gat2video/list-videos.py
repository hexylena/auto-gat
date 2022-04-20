#!/usr/bin/env python
import glob

for video in sorted(glob.glob('video-[0-9].mp4') + glob.glob('video-[0-9][0-9].mp4'), key=lambda x: int(x.split('-')[1][0:-4])):
    print(f"file '{video}'")
