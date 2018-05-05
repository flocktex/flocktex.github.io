#!/bin/bash

set -e -x

# build
python flocktex/app.py build -opt
mv flocktex/build /tmp

# commit
git remote rm origin
git remote add origin https://$GITHUB_TOKEN@github.com/flocktex/flocktex.github.io.git
git fetch origin
git checkout -f master
rm -rf *
mv -f /tmp/build/** ./
echo "www.flocktex.in" > CNAME
git add .
commit_message=$(git log dev -1 --pretty="[%h $(date)] %s")
git commit -m "$commit_message"
git push origin master
