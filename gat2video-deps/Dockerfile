FROM ubuntu:20.04

ENV TZ=Europe/Amsterdam \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8

RUN echo "force-unsafe-io" > /etc/dpkg/dpkg.cfg.d/02apt-speedup \
    && echo "Acquire::http {No-Cache=True;};" > /etc/apt/apt.conf.d/no-cache \
    && apt-get -qq update && apt-get install --no-install-recommends -y locales \
    && locale-gen en_US.UTF-8 && dpkg-reconfigure locales \
    && apt-get autoremove -y && apt-get clean

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt install -y git sudo
RUN apt install -y pkg-config xvfb libx11-dev libxi-dev libxext-dev libglx-dev libglu1-mesa-dev freeglut3-dev mesa-common-dev ffmpeg pv silversearcher-ag fonts-dejavu-core fonts-dejavu-extra curl
RUN apt install -y unzip
RUN  curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash - && \
	sudo apt-get install -y nodejs

RUN useradd ubuntu -m
RUN echo "ubuntu ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/ubuntu
RUN mkdir /home/ubuntu/.aws

RUN apt install -y build-essential
# Playwright ships a custom thing to install deps
RUN npx -y playwright install-deps chromium
RUN sudo apt install -y ruby
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && ./aws/install
RUN sudo apt install -y python3-pip

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
