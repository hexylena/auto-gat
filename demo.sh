#!/bin/bash
# Disable git's paging which can cause a hang
export GIT_PAGER=cat
# Prevent pip from shouting everywhere
pip config --user set global.progress_bar off
# Setup the demo-magic
. ./demo-magic/demo-magic.sh -n
# Hide our demo-magic activation
clear

# Install ansible (move to pre-setup?)
pe "pip install ansible"
# Clone git-gat
git clone -q https://github.com/hexylena/git-gat/
cd git-gat
# Show what's there
pe 'git status'

# We'll loop over the commits in the repo, one by one
for commit in $(git log --pretty=oneline | tac | head -n 4 | cut -f 1 -d' '); do
	pe "git checkout $commit"
	echo "Here's what changed"
	pe "git show"
	pe "ls -al"

	# If the requirements file was changed, then we need to re-run ansible-galaxy install
	reqs=$(git show --name-only | grep --quiet requirements.yml)
	ec=$?
	if (( ec == 0 )); then
		echo "The requirements have changed."
		pe "ansible-galaxy install -p roles -r requirements.yml"
	fi

	# TODO: ansible-playbook
done
