#! /bin/bash

echo "Setting up one-liner..."

ONELINER_TEMPLATE="https://raw.githubusercontent.com/GodOfKebab/one-liner/master/.one-liner"
ONELINER_PYTHON_URL="https://raw.githubusercontent.com/GodOfKebab/one-liner/master/one-liner.py"

curl -Ls $ONELINER_TEMPLATE -o ~/.one-liner
ONELINER_PATH="$HOME/.one-liner"
export ONELINER_PATH
ONELINER_FILE_CONTENTS=$(curl -Ls $ONELINER_PYTHON_URL)
curl -Ls $ONELINER_PYTHON_URL | python3 - init --init_file_contents "$ONELINER_FILE_CONTENTS"

if [ $SHELL = "/bin/bash" ]; then
	echo "detected bash"
	echo "source ~/.one-liner" >> ~/.bashrc
elif [ $SHELL = "/bin/zsh" ]; then
	echo "detected zsh"
	echo "source ~/.one-liner" >> ~/.zshrc
fi

source "$HOME/.one-liner"
echo "All set. You can start using one-liner."

