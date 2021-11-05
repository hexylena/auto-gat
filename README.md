# Fully Automated Luxury GAT Screen Capture

**Premise**: We can record all of GAT automatically. Every terminal interaction, everything. Fully automated, so we can just relax on the beach while it records our workshop for us.

## Terminal Recordings

See current recordings here: https://asciinema.org/~hexylena (there are some known issues.)

[![asciicast](https://asciinema.org/a/402574.svg)](https://asciinema.org/a/402574)

## Galaxy Recordings

```
sudo apt-get install libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libgtk-3-0 libpango-1.0-0 libcairo2 libgdk-pixbuf2.0-0 libasound2 libatspi2.0-0 libxshmfence1 libx11-xcb1 fonts-noto-color-emoji fonts-dejavu ffmpeg pv
```

For this we've come up with a pretty generic recording tool. It takes in a json file describing the steps, and returns a video and a json file with timestamps the actions occurred at to enable proper audio syncing.

```
node player.js play-0.json video-0.mp4
```

Where `play-0.json` looks like this:

```
[
  {"action": "goto", "target": "http://localhost:4002/training-material/topics/admin/tutorials/cvmfs/tutorial.html"},
  {"action": "scrollTo", "target": "#top-navbar", "sleep": 8.904},
  {"action": "scrollTo", "target": "#cvmfs-quote", "sleep": 52.248},
  {"action": "scrollTo", "target": "#agenda", "sleep": 12.672},
  {"action": "scrollTo", "target": "#ansible-cvmfs-and-galaxy", "sleep": 23.28},
  {"action": "scrollTo", "target": "#installing-and-configuring", "sleep": 15.336}
]
```

And you'll get a nice video output with the following sync log:

```
[{"msg": {"action": "scroll", "target": "#top-navbar"}, "time": 4393},
 {"msg": {"action": "scroll", "target": "#cvmfs-quote"}, "time": 13308},
 {"msg": {"action": "scroll", "target": "#agenda"}, "time": 65605},
 {"msg": {"action": "scroll", "target": "#ansible-cvmfs-and-galaxy"}, "time": 78292},
 {"msg": {"action": "scroll", "target": "#installing-and-configuring"}, "time": 101596}]
```

Which you can then sync with your audio with ffmpeg.
