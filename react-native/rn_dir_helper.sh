#!/usr/bin/env zsh
# A helper script to create all those files and directories as
# chalked out in this blog - https://medium.com/the-react-native-log/organizing-a-react-native-project-9514dfadaa0#.fredxmhja

echo "Creating app/"
mkdir -p app && cd app

echo "Creating index.js inside app/"
touch --no-create index.js

dir_struct=('components' 'config' 'images' 'layouts' 'includes' 'routes')

echo "Creating directories inside app/"
for dir_name in $dir_struct;do
    echo "Creating $dir_name..."
    mkdir -p "$dir_name"
done

