# one-liner
This is the tool I use for creating one-liner python bash aliases.
Basically, this tool will convert your python script to a one-line
bash alias by using compression and base64 encoding of the script
file and then saving it to a source-able file (at $HOME/.one-liner) 
so that you can use that python script without relying on the original
script file. This way, even if the original script file is deleted/moved,
since its contents would be encoded in the one-liner alias, you can
still use the script.

This tool is especially useful if the script's path changes often
or if you don't want to risk the execution of a script if the path 
changes. Other use cases may include the easy creation of python
executable-likes.

## Installation:
### one-liner install [recommended]
For easy installation, copy and paste the following line in the shell. 
Make sure to have curl installed in your system. This installation
will not leave any other file than the .one-liner file in your system.

    curl -Ls https://raw.githubusercontent.com/GodOfKebab/one-liner/master/install.sh | bash

### GitHub install [recommended only for devs]
This installation option is only recommended if you want to add features
to the tool. This installation will leave the repo code folder and 
.one-liner file in your system.

    git clone git@github.com:GodOfKebab/one-liner.git
    cd one-liner
    python3 one-liner.py init "$(cat one-liner.py)" 

## Quickstart Guide:
### Usage

To use this tool, first, specify your mode and then the arguments it takes (if any).

    one-liner mode [-h] [-v] OPTIONS

To view the available modes simply type the mode with the 
help flag, like so:

    one-liner -h
      usage: one-liner [-h] [-v] mode [mode-specific-required-args]...
    
      Manage one-liner python bash aliases without relying on the original script file. To view the required arg(s) for each of the modes, add the help flag (-h) to the mode. For example, -> one-liner create -h
    
      positional arguments:
        mode           init ->        initialize the .one-liner file
                       create [aliases: cr, touch] ->         create and add one-liner
                       overwrite      [aliases: ov] ->        create and overwrite one-liner
                       rename [aliases: mv] ->        rename a one-liner
                       print  [aliases: pr, echo] ->  print the alias line of one-liner
                       dump   [aliases: dmp, export, cat] ->  decode the one-liner and dump it either on the shell or to a file
                       list   [aliases: ls] ->        list the all one-liners
                       delete [aliases: del, rm] ->   remove a one-liner
                       fix    [aliases: format] ->    fix .one-liner file by parsing and construct the .one-liner file again
    
      optional arguments:
        -h, --help     show this help message and exit
        -v, --verbose  enable debug printing
        -y, --yes      skip the 'Do you want to continue? [y/N]' prompt


To view the arguments that a mode takes, simply type the mode with the 
help flag, like so:

    one-liner create -h
      usage: one-liner create [-h] [-v] [-y] [name] filepath
    
      selected mode -> create: create and add one-liner
    
      positional arguments:
        name           alias name for the one-line. If rename mode, first name is the old and the second name is the new name.
        filepath       file path for the python script to be converted to/from one-liner
    
      optional arguments:
        -h, --help     show this help message and exit
        -v, --verbose  enable debug printing
        -y, --yes      skip the 'Do you want to continue? [y/N]' prompt

### Example Usage

    one-liner create greet_the_god scripts/welcome_god_of_kebab.py
      Creating one-liner 'greet_the_god' is successful 💥

      👍 Execute the following in shell for changes to take effect:
           source /USERS-HOME/YOUR-USERNAME/.one-liner

    source /USERS-HOME/YOUR-USERNAME/.one-liner
    greet_the_god
      __        __       _                                   
      \ \      / /  ___ | |  ___   ___   _ __ ___    ___     
       \ \ /\ / /  / _ \| | / __| / _ \ | '_ ` _ \  / _ \    
        \ V  V /  |  __/| || (__ | (_) || | | | | ||  __/ _  
         \_/\_/    \___||_| \___| \___/ |_| |_| |_| \___|( ) 
                                                         |/  
        ____             _     ___    __    _  __       _             _          __  
       / ___|  ___    __| |   / _ \  / _|  | |/ /  ___ | |__    __ _ | |__     _ \ \ 
      | |  _  / _ \  / _` |  | | | || |_   | ' /  / _ \| '_ \  / _` || '_ \   (_) | |
      | |_| || (_) || (_| |  | |_| ||  _|  | . \ |  __/| |_) || (_| || |_) |   _  | |
       \____| \___/  \__,_|   \___/ |_|    |_|\_\ \___||_.__/  \__,_||_.__/   (_) | |
                                                                                 /_/
    one-liner ls
      greet_the_god
    one-liner echo greet_the_god
      ✅ Below is the alias for the one-liner 'greet_the_god' 👇

          alias greet_the_god='python3 -c "import base64; import zlib; decoded_string = zlib.decompress(base64.b64decode(b'"'"'eNo1TbsKAjEQ7PcrpktW5DgtD6wtLCxtrrnTDSzkRS6Fn28ScJphhnm4kgK2UqEhp0Ynct2pGuRvHV4kU5VvxQ2dri1vzUv8OwU5Y4339AGeDnjIvu3AwoaJXCrwGttOHLXpyF5bcY2GF0JDLhqr7RkeejzZeZovTD9cNi/d'"'"')).decode(); exec(decoded_string)"'

    one-liner cat greet_the_god
      WARNING: filepath is not specified ❌ , dumping to the terminal 👇
      **************************************************
      from art import *
      from time import sleep
      text = text2art('Welcome, \nGod  Of  Kebab  :)')
    
      for line in text.split('\n'):
          print(line)
          sleep(0.01)
    
      **************************************************
    one-liner rm greet_the_god
      You are about to delete the one-liner: 'greet_the_god' ⚠️ Do you want to continue? [y/N] y
      Deleting 'greet_the_god' is successful 💥
    one-liner ls
    one-liner fix
      ✅  Parsing and de-parsing the .one-liner file was successful! 👍
    

## Available modes:

    init:     description: initialize the .one-liner file
              aliases:     -
              required:    script
              optional:    -
    
    create:   description: create and add one-liner
              aliases:     cr, touch
              required:    file
              optional:    name

    overwrite: description: create and overwrite one-liner
              aliases:     ov
              required:    name file
              optional:    -

    rename:   description: rename a one-liner
              aliases:     mv
              required:    name name
              optional:    -

    print:    description: print the alias line of one-liner
              aliases:     pr, echo
              required:    name
              optional:    -

    dump:     description: decode the one-liner and dump 
                           it either on the shell or to a file
              aliases:     dmp, export, cat
              required:    name
              optional:    file

    list:     description: list the all one-liners 
              aliases:     ls
              required:    -
              optional:    -

    delete:   description: remove a one-liner
              aliases:     del, rm
              required:    name
              optional:    -

    fix:      description: fix .one-liner file by parsing and 
                           construct the .one-liner file again
              aliases:     format
              required:    -
              optional:    -

## Developer's Guide

It is highly recommended that you install the tool using the
dev-recommended way if you want to develop the tool. Then, to test your changes, simply run the
following command to overwrite the one-liner alias.

    python3 one-liner.py -y init "$(cat one-liner.py)"; source $HOME/.one-liner 
