
RUN apt install -y build-essential
# Playwright ships a custom thing to install deps
RUN npx -y playwright install-deps chromium

WORKDIR /home/ubuntu/
RUN chown ubuntu:ubuntu -R /home/ubuntu
USER ubuntu
RUN git clone https://github.com/hexylena/git-gat /home/ubuntu/galaxy/
COPY --chown=ubuntu package.json  package-lock.json  requirements.txt  setup.sh /home/ubuntu/gat2video-deps/


WORKDIR /home/ubuntu/gat2video-deps
RUN bash setup.sh

COPY --chown=ubuntu setup-ansible.sh /home/ubuntu/gat2video-deps/
RUN bash setup-ansible.sh

RUN sudo pip install ansible

WORKDIR /home/ubuntu/gat2video/
ENTRYPOINT ["python3", "gat2video.py"]
