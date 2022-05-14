# one-liner
This is the tool I use for creating one-liner python executables.

##Installation:

```curl -Ls https://raw.githubusercontent.com/GodOfKebab/one-liner/master/install.sh | bash```

##Features:

    init:     parse and add one-liner one-liner
    
    create:   parse and add one-liner
    
    override: parse and replace one-liner
    
    rename:   parse and rename one-liner
    
    print:    parse and print one-liner
    
    dump:     parse and dump one-liner 
              contents to either shell or to a file
    
    list:     parse and list
    
    delete:   parse and remove one-liner
    
    fix:      parse and construct the .one-liner file again
    
    sync[N]:  parse, convert to an ecrypted file, and send it.

Below are the aliases to each of the modes

    modes = {"init": ["init"],
             "create": ["create", "cr", "touch"],
             "override": ["override", "ov"],
             "rename": ["rename", "mv"],
             "print": ["print", "pr", "echo"],
             "dump": ["dump", "dmp", "export", "cat"],
             "list": ["list", "ls"],
             "delete": ["delete", "del", "rm"],
             "fix": ["fix", "format"],
             "sync": ["sync"]}

Below is the arguments that each mode requires/makes it optional

    init:     required: script
              optional: - 
    
    create:   required: file
              optional: name
    
    override: required: name file
              optional: - 
    
    rename:   required: name name
              optional: -
    
    print:    required: name
              optional: -
    
    dump:     required: name
              optional: file
    
    list:     required: -
              optional: -
    
    delete:   required: name
              optional: -
    
    fix:      required: -
              optional: -
    
    sync[N]:  required: -
              optional: pull/push


##Example usages:
```
$ oneliner cr --filepath src/welcome_god_of_kebab.py --name greet_the_god
  
  Execute the following in shell for changes to take effect:
      source .../one-liner/src/.one-liner

$ oneliner ls
  greet_the_god
$ oneliner echo -n greet_the_god

    alias greet_the_god='python3 -c "import base64; decoded_string = base64.b64decode(b'"'"'ZnJvbSBhcnQgaW1wb3J0ICoKZnJvbSB0aW1lIGltcG9ydCBzbGVlcAp0ZXh0ID0gdGV4dDJhcnQoJ1dlbGNvbWUsIFxuR29kICBPZiAgS2ViYWIgIDopJykKCmZvciBsaW5lIGluIHRleHQuc3BsaXQoJ1xuJyk6CiAgICBwcmludChsaW5lKQogICAgc2xlZXAoMC4wNSkKCgoK'"'"').decode(); exec(decoded_string)"'

$ oneliner cat -n greet_the_god
  WARNING: filepath is not specified, dumping to the terminal
  **************************************************
  from art import *
  from time import sleep
  text = text2art('Welcome, \nGod  Of  Kebab  :)')

  for line in text.split('\n'):
      print(line)
      sleep(0.05)

  **************************************************
$ oneliner rm -n greet_the_god
$ oneliner ls
```

##Developer's Guide

- Using the below command to create the one-liner alias will come in handy:
        
        $ python3 one-liner.py init  "$(cat one-liner.py)" 

##Features backlog:

* proper logging
* are you sure? prompt
* add install.sh arguments so that DX is better
* add test codes to automate testing going forward
* enable sync mode

