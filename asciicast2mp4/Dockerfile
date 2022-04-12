FROM beer5215/asciicast2mp4

RUN apt update && \
    apt install -y python-pip python-virtualenv

ADD . /a2mp4server/
WORKDIR /a2mp4server/
RUN virtualenv venv && \
	. venv/bin/activate && \
	pip install flask

ENTRYPOINT ["./venv/bin/flask", "run"]
