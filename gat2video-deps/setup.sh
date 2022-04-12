#!/bin/bash
set -e

# Configure AWS
mkdir -p ~/.aws/

cat > ~/.aws/config <<-EOF
[default]
region=us-east-1
EOF

#if [[ ! -f ~/.aws/credentials ]]; then
	#echo "Missing aws creds"
	#exit
#fi

# Node installation will fail otherwise.
if [[ ! -f  /usr/bin/python ]]; then
	sudo ln -s /usr/bin/python3 /usr/bin/python
fi


# Install node requirements.
npm i

FFMPEG_PATH=$(echo "const ffmpeg = require('ffmpeg-static');console.log(ffmpeg.split('/').slice(0, -1).join('/'));" | node -)
echo "Located FFMPEG at $FFMPEG_PATH"
export PATH="$FFMPEG_PATH:$PATH"

# Install python requirements
pip3 install -r requirements.txt


echo password > ~/galaxy/.vault-password.txt

# Setup git-gat
echo 'password' > ~/.vault-password.txt;

cat > ~/.hosts <<-EOF
[galaxyservers]
$(hostname -f) ansible_connection=local ansible_user=$(whoami)
[pulsarservers]
$(hostname -f) ansible_connection=local ansible_user=$(whoami)
EOF

cat > ~/.ansible.cfg <<-EOF
[defaults]
interpreter_python = /usr/bin/python3
inventory = ~/.hosts
retry_files_enabled = false
vault_password_file = ~/.vault-password.txt
EOF


# Run it.
#python3 gat2video.py
