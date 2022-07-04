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

# Check to see if there exists an installation of the one-liner tool
if [ -f "$ONELINER_PATH" ]; then
  read -p "Existing one-liner setup found! Only the one-liner tool will be overridden. Do you want to continue? [y/N] " -r yn
  case "$(echo -e "$yn" | tr -d '[:space:]')" in
      [Yy]* ) ;;
      * ) echo "Aborting..."; exit;;
  esac
else
    curl -Ls $ONELINER_TEMPLATE -o "$ONELINER_PATH"
fi

curl -Ls $ONELINER_PYTHON_URL | python3 - init "$(curl -Ls $ONELINER_PYTHON_URL)" -y
#python3 "$(dirname "$0")/one-liner.py" init "$(cat "$(dirname "$0")/one-liner.py")" # DEBUG

