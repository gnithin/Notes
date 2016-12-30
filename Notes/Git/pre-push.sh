#!/bin/sh
# This basically is a pre-push git hook. 
# It's run after a connection is established with the remote and before anything is pushed.

# This script basically does this -
# - Executes a file
# - Adds the changes made, to git
# - Pushes the commit to remote
# To prevent the last push to recursively call this hook infinitely,
# referred to this awesome answer (point 3) - http://stackoverflow.com/a/21334985/1518924 

# Run the file and try to commit 
# Note: It's expected that readme_maker will print the names of the files that've been modified
OP_CONTENTS="$(python readme_maker.py)"

# Get the multi-line filenames and make'em in one line
OP_FILE=$(echo "${OP_CONTENTS}" | tail -n +2 | tr '\n' ' ')

if [ "$OP_FILE" = "" ]
then
    echo "Something went wrong with readme_maker.py. Run with PRINT_LOG on"
    echo "Aborting..."
    exit 2
else
    git add $OP_FILE
fi

echo "---------------------------------"

git commit -m "[README] Auto-update README.md"

if [ $? -ne 0 ]
then
    exit 0
else
    echo "Automatically updated the README!"
    echo "---------------------------------"
    git push -uf origin master

    echo "*******************************************************************************************"
    echo "It's been pushed. Do not worry about the final error message. It is because of the git hook"
    echo "*******************************************************************************************"
    exit 1
fi
