#! /bin/sh

echo "Setting up one-liner..."

ONELINER_TEMPLATE="https://raw.githubusercontent.com/GodOfKebab/one-liner/master/src/.one-liner"
ONELINER_PYTHON_URL="https://raw.githubusercontent.com/GodOfKebab/one-liner/master/src/one-liner.py"

curl -Ls $ONELINER_TEMPLATE -o ~/.one-liner
sh ~/.one-liner
ONELINER_FILE_CONTENTS=$(curl -Ls $ONELINER_PYTHON_URL)
curl -Ls $ONELINER_PYTHON_URL | python3 - init --init_file_contents "$ONELINER_FILE_CONTENTS"

if [ $SHELL = "/bin/bash" ]; then
	echo "detected bash"
	echo "source ~/.one-liner" >> ~/.bashrc
elif [ $SHELL = "/bin/zsh" ]; then
	echo "detected zsh"
	echo "source ~/.one-liner" >> ~/.zshrc
fi

sh ~/.one-liner
echo "All set. You can start using one-liner."

