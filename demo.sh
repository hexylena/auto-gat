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
cd git-gat
# Show what's there
pe "ls -al"

# We'll loop over the commits in the repo, one by one
for commit in $(git log --pretty=oneline | tac | head -n 10 | cut -f 1 -d' '); do
	git checkout $commit
	echo "Next step: $(git show | head -n 5 |tail -n 1 | sed 's/[^:]*: //g')"
	# echo "File changed: $(git show --name-only | tail -n 1)"
	# Show the commit
	git show --pretty | tail -n+9

	# If the requirements file was changed, then we need to re-run ansible-galaxy install
	reqs=$(git show --name-only | grep --quiet requirements.yml)
	ec=$?
	if (( ec == 0 )); then
		echo "The requirements have changed."
		pe "ansible-galaxy install -p roles -r requirements.yml"
	fi

	if [[ -f galaxy.yml ]]; then
		echo "Let's re-run the playbook"
		pe "ansible-playbook galaxy.yml"
	fi
done
