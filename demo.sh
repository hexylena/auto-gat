#!/bin/bash
pip config --user set global.progress_bar off
. ./demo-magic/demo-magic.sh -n
clear
pe "pip install ansible"
git clone -q https://github.com/hexylena/git-gat/
cd git-gat
pe 'git status'
for commit in $(git log --pretty=oneline | tac | head -n 4 | cut -f 1 -d' '); do
	pe "git checkout $commit"
	echo "Here's what changed"
	pe "git show"
	pe "ls -al"
	reqs=$(git show --name-only | grep --quiet requirements.yml)
	ec=$?
	if (( ec == 0 )); then
		echo "The requirements have changed."
		pe "ansible-galaxy install -p roles -r requirements.yml"
	fi
done
