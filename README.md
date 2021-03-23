# Fully Automated Luxury GAT Screen Capture

**Premise**: We can record all of GAT automatically. Every terminal interaction, everything. Fully automated, so we can just relax on the beach while it records our workshop for us.

## WIP Demo

Write a script like this

```
#!/bin/bash
. ./demo-magic/demo-magic.sh -n
clear
pe "pwd"
pe 'git status'
pe 'git log --oneline --decorate -n 20 | cat'
pe "ls"
```

and then automatically record it (to be done in github.)

```
rm -f out.cast; asciinema rec out.cast -c ./demo.sh
```

Amazing. We're halfway there.
