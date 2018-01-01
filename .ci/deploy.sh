#!/bin/bash

set -e -x

# build
python flocktex/app.py build
mkdir /tmp/build
mv flocktex/build/** /tmp/build

# commit
git remote rm origin
git remote add origin https://$GITHUB_TOKEN@github.com/flocktex/flocktex.github.io.git
git fetch origin
git checkout master
rm -rf *
mv -f /tmp/build/** ./
echo "www.flocktex.in" > CNAME
git add .
commit_message=$(git log dev -1 --pretty="[%h $(date)] %s")
git commit -m "$commit_message"
git push origin master
