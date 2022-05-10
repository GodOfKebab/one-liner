#! /bin/bash

echo "#######################"
echo "Setting up one-liner..."

ONELINER_TEMPLATE="https://raw.githubusercontent.com/GodOfKebab/one-liner/master/.one-liner"
ONELINER_PYTHON_URL="https://raw.githubusercontent.com/GodOfKebab/one-liner/master/one-liner.py"

# PARAMETERS START
ONELINER_PATH="$HOME/.one-liner"
#ONELINER_PATH="$(pwd)/.one-liner" # DEBUG
export ONELINER_PATH

ONELINER_PYTHON_EXEC="python3"
export ONELINER_PYTHON_EXEC
# PARAMETERS END

curl -Ls $ONELINER_TEMPLATE -o "$ONELINER_PATH"
curl -Ls $ONELINER_PYTHON_URL | python3 - init --init_file_contents "$(curl -Ls $ONELINER_PYTHON_URL)"
#python3 "$(dirname "$0")/one-liner.py" init --init_file_contents "$(cat "$(dirname "$0")/one-liner.py")" # DEBUG

