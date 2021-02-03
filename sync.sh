#!/bin/bash
#implicit backup

git fetch #download server
git checkout origin/main -- recipes.p #overwrite
python3 sync.py #combine
git commit -m "syncing recipes" recipes.p
git push origin main
