#!/bin/bash
OUR_DIR=$(pwd)
DRY_RUN=0

# Dry
#DRY_RUN=1
SPEED=0.01

# Disable git's paging which can cause a hang
export GIT_PAGER=cat
export GALAXY_HOSTNAME="$(hostname -f)"
export GALAXY_API_KEY=adminkey
echo 'password' > ~/.vault-password.txt;

cat > ~/.hosts <<-EOF
[galaxyservers]
$(hostname -f) ansible_connection=local ansible_user=$(whoami)
[pulsarservers]
$(hostname -f) ansible_connection=local ansible_user=$(whoami)
EOF

cat > ~/.ansible.cfg <<-EOF
[defaults]
Interpreter_python = /usr/bin/python3
iNventory = ~/.hosts
retry_files_enabled = false
vault_password_file = ~/.vault-password.txt
EOF

# Prevent pip from shouting everywhere
pip config --user set global.progress_bar off
# Setup the demo-magic
. ${OUR_DIR}/demo-magic/demo-magic.sh -n
# Hide our demo-magic activation
clear

# Install ansible (move to pre-setup?)
cd git-gat
#pwd
#ls

# Show what's there
ansible-galaxy install -p roles galaxyproject.self_signed_certs > /dev/null 2>/dev/null

# We'll loop over the commits in the repo, one by one
OLDIFS="$IFS"
IFS=$'\n'
for thing in $(cat .scripts/10-ansible-galaxy-script.txt); do
	if [[ "$thing" == "git checkout"* ]]; then
		# Checkout this commit
		bash -c "$thing -q"
		current_Commit=$(git show --format=%H | head -n 1)
		echo "$(tput bold)Next step: $(git show --format="%s" | head -n 1 | sed 's/[^:]*: //g') $(tput sgr0)"
		if (( DRY_RUN == 0 )); then
			sleep 2
		fi

		# This will pretend to edit it in """"vim""""
		fileChanged=$(git show --name-only | tail -n 1)
		# Checkout the previous commit so we can show the diff properly
		git checkout -q "$current_Commit^1"
		p "nano $fileChanged"
		python3 ${OUR_DIR}/diffplayer.py \
			--diff <(git show "$current_Commit") \
			--nosave \
			--speed ${SPEED}
		# And revert back to the commit we said we're on
		git checkout -q "$current_Commit"
	elif [[ "$thing" ==  "ansible-galaxy"* ]]; then
		echo "The requirements have changed, we'll need to install the new ones."
		if (( DRY_RUN == 1 )); then
			p "ansible-galaxy install -p roles -r requirements.yml"
		else
			pe "ansible-galaxy install -p roles -r requirements.yml"
		fi

	elif [[ "$thing" ==  "ansible-playbook"* ]]; then
		echo "Let's re-run the playbook"
		p "ansible-playbook galaxy.yml -u ${USER}"
		if (( DRY_RUN == 1 )); then
			echo ansible-playbook galaxy.yml -u ${USER} -e "nginx_ssl_role=galaxyproject.self_signed_certs openssl_domains={{ certbot_domains }}" --vault-password-file ~/.vault-password.txt -i ~/.hosts
		else
			export ANSIBLE_CONFIG=~/.ansible.cfg
			ansible-playbook galaxy.yml -u ${USER} -e "nginx_ssl_role=galaxyproject.self_signed_certs openssl_domains={{ certbot_domains }}" --vault-password-file ~/.vault-password.txt -i ~/.hosts
		fi
	else
		echo "UNKNOWN $thing"
	fi
done
