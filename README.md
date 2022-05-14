# one-liner
This is the tool I use for creating one-liner python executables.
Basically, this tool will convert your python script to a one-line
bash alias by using compression and base64 encoding of the script
file and then saving it to a source-able file so that you can
execute the one-liner script without relying on any script file. 
This way, even if the original script file is deleted/moved, since
the contents of it would be encoded in the one-liner alias, you can
still use the script.

This tool is especially useful if the script's path changes often
or if you don't want to risk the execution of a script if the path 
changes. Other use cases may include the easy creation of python
executables.

## Installation:
### one-liner install [recommended]
For easy installation, copy and paste the following line in the shell. 
Make sure to have curl installed in your system. This installation
will not leave any other file than the .one-liner file in your system.

    $ curl -Ls https://raw.githubusercontent.com/GodOfKebab/one-liner/master/install.sh | bash

### GitHub install [recommended only for devs]
This installation option is only recommended if you want to add features
to the tool. This installation will leave the repo code folder and 
.one-liner file in your system.

    $ git clone git@github.com:GodOfKebab/one-liner.git
    $ cd one-liner
    $ python3 one-liner.py init  "$(cat one-liner.py)" 

## Quickstart Guide:
### Usage

To use this tool, first, specify your mode and then the arguments it can take.

    $ one-liner mode [-h] [-v] OPTIONS

To view the arguments that a mode takes, simply type the mode with the 
help flag like so:

    $ one-liner create -h

### Example Usage

    $ one-liner create greet_the_god src/welcome_god_of_kebab.py
      
      Execute the following in shell for changes to take effect:
          source .../.one-liner
    
    $ one-liner ls
      greet_the_god
    $ one-liner echo greet_the_god
    
        alias greet_the_god='python3 -c "import base64; import zlib; decoded_string = zlib.decompress(base64.b64decode(b'"'"'eNo1TbsKAjEQ7PcrpktW5DgEmwNrCwtLm2vudAMLeZFL4eebBJxmmGEerqSArVRoyKnRiVx3qgb5W4cXyVTlW3FDp0vLW/MS/05BzljjPX2ApwMesm87sLBhIpcKvMa2E0dtOrLXVlyj4YXQkIvGanuGhx5Pdp7mK9MPXEIv4Q=='"'"')).decode(); exec(decoded_string)"'    
    
    $ one-liner cat greet_the_god
      WARNING: filepath is not specified, dumping to the terminal
      **************************************************
      from art import *
      from time import sleep
      text = text2art('Welcome, \nGod  Of  Kebab  :)')
    
      for line in text.split('\n'):
          print(line)
          sleep(0.05)
    
      **************************************************
    $ one-liner rm greet_the_god
    $ one-liner ls
    $ one-liner fix
    $

## Available modes:

    init:     description: initialize the .one-liner file
              aliases:     -
              required:    script
              optional:    -
    
    create:   description: create and add one-liner
              aliases:     cr, touch
              required:    file
              optional:    name

    override: description: create and override one-liner
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

    sync[N]:  description: encrypt all the one-liners and sync
                           with the one-liner servers (not functional)
              aliases:     - 
              required:    -
              optional:    pull/push

## Developer's Guide

It is highly recommended that you install the tool using the
dev-recommended way. Then, to test your changes, simply run the
following commands to override the one-liner alias.

    $ one-liner rm one-liner
    $ python3 one-liner.py init "$(cat one-liner.py)"

## TODO List:

- [ ] proper logging (verbose flag isn't fully functional yet)
- [ ] are you sure? prompt
- [ ] add install.sh arguments so that DX is better
- [ ] add test codes to automate testing going forward
- [ ] enable sync mode

