#!/bin/bash
. ./demo-magic/demo-magic.sh -n
clear
pe "pwd"
pe 'git status'
pe 'git log --oneline --decorate -n 20 | cat'
pe "ls"
