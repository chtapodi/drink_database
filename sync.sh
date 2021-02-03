#!/bin/bash
#implicit backup

git fetch #download server
git checkout origin/main -- recipes.p #overwrite
python3 sync.py #combine 
git commit -am "syncing recipes"
git push
