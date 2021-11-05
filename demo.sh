#!/bin/bash
OUR_DIR=$(pwd)
# Disable git's paging which can cause a hang
export GIT_PAGER=cat
export GALAXY_HOSTNAME="$(hostname -f)"
export GALAXY_API_KEY=adminkey
echo 'password' > ~/.vault-password.txt;
echo '[galaxyservers]' > ~/.hosts
echo "$(hostname -f) ansible_connection=local ansible_user=$(whoami)"  >> ~/.hosts
echo '[pulsarservers]' >> ~/.hosts
echo "$(hostname -f) ansible_connection=local ansible_user=$(whoami)"  >> ~/.hosts

# Prevent pip from shouting everywhere
pip config --user set global.progress_bar off
# Setup the demo-magic
. ${OUR_DIR}/demo-magic/demo-magic.sh -n
# Hide our demo-magic activation
clear

# Install ansible (move to pre-setup?)
cd git-gat
pwd
ls

# Show what's there
ansible-galaxy install -p roles galaxyproject.self_signed_certs > /dev/null 2>/dev/null

# We'll loop over the commits in the repo, one by one
OLDIFS="$IFS"
IFS=$'\n'
for thing in $(cat .scripts/10-ansible-galaxy-script.txt); do
	if [[ "$thing" == "git checkout"* ]]; then
		# Checkout this commit
		bash -c "$thing"
		current_Commit=$(git show --format=%H | head -n 1)
		echo "$(tput bold)Next step: $(git show --format="%s" | head -n 1 | sed 's/[^:]*: //g') $(tput sgr0)"
		sleep 2

		# Checkout the previous commit so we can show the diff properly
		git checkout -q "$current_Commit^1"
		# This will pretend to edit it in """"vim""""
		python3 ${OUR_DIR}/diffplayer.py \
			--diff <(git show "$current_Commit") \
			--nosave \
			--speed 0.1
		# And revert back to the commit we said we're on
		git checkout -q "$current_Commit"
	elif [[ "$thing" ==  "ansible-galaxy"* ]]; then
		echo "The requirements have changed, we'll need to install the new ones."
		pe "ansible-galaxy install -p roles -r requirements.yml"

	elif [[ "$thing" ==  "ansible-playbook"* ]]; then
		echo "Let's re-run the playbook"
		p "ansible-playbook galaxy.yml -u ${USER}"
		ansible-playbook galaxy.yml -u ${USER} -e "nginx_ssl_role=galaxyproject.self_signed_certs openssl_domains={{ certbot_domains }}" --vault-password-file ~/.vault-password.txt -i ~/.hosts
	fi
done
