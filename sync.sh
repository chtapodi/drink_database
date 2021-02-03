#!/bin/bash
git fetch
git checkout origin/main recipes.p
python3 sync.py
git commit -am "syncing recipes"
git push
