# one-liner
This is the tool I use for creating one-liner python executables.

Installation:

```curl -Ls https://raw.githubusercontent.com/GodOfKebab/one-liner/master/install.sh | bash```

Features:

    init:     parse and add one-liner one-liner
    
    create:   parse and add one-liner
    
    override: parse and replace one-liner
    
    rename[N]:parse and rename one-liner
    
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

Example usages:
```
$ one-liner cr --filepath src/welcome_god_of_kebab.py --name greet_the_god
  
  Execute the following in shell for changes to take effect:
      source .../one-liner/src/.one-liner

$ one-liner ls
  greet_the_god
$ one-liner echo -n greet_the_god

      alias greet='python3 -c "import base64; import zlib; decoded_string = zlib.decompress(base64.b64decode(b'"'"'eNo1TbsKAjEQ7PcrpktW5DgEmwNrCwtLm2vudAMLeZFL4eebBJxmmGEerqSArVRoyKnRiVx3qgb5W4cXyVTlW3FDp0vLW/MS/05BzljjPX2ApwMesm87sLBhIpcKvMa2E0dtOrLXVlyj4YXQkIvGanuGhx5Pdp7mK9MPXEIv4Q=='"'"')).decode(); exec(decoded_string)"'

$ one-liner cat -n greet_the_god
  WARNING: filepath is not specified, dumping to the terminal
  **************************************************
  from art import *
  from time import sleep
  text = text2art('Welcome, \nGod  Of  Kebab  :)')

  for line in text.split('\n'):
      print(line)
      sleep(0.05)

  **************************************************
$ one-liner rm -n greet_the_god
$ one-liner ls
```

Currently, the tool works stable, however, for rename mode to work, semi-major upgrade is needed. This is why the latest release is <1.0.

Features tracker:

* rename mode
* are you sure? prompt
* add install.sh arguments so that DX is better
* add test codes to automate testing going forward
* enable sync mode

