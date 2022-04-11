# one-liner
This is the tool I use for creating one-liner python executables.

Example usages:
```
$ oneliner cr --filepath src/welcome_god_of_kebab.py --name greet_the_god
    
    Execute the following in shell for changes to take effect:
    $ source /Users/yasaridikut/PycharmProjects/one-liner/src/.one-liner

$ oneliner ls
    greet_the_god
$ oneliner print -n greet_the_god

    alias greet_the_god='python3 -c "import base64; decoded_string = base64.b64decode(b'"'"'ZnJvbSBhcnQgaW1wb3J0ICoKZnJvbSB0aW1lIGltcG9ydCBzbGVlcAp0ZXh0ID0gdGV4dDJhcnQoJ1dlbGNvbWUsIFxuR29kICBPZiAgS2ViYWIgIDopJykKCmZvciBsaW5lIGluIHRleHQuc3BsaXQoJ1xuJyk6CiAgICBwcmludChsaW5lKQogICAgc2xlZXAoMC4wNSkKCgoK'"'"').decode(); exec(decoded_string)"'

$ oneliner rm -n greet_the_god
$ oneliner ls
```
Here are the available modes:

	init

	print to terminal
		print, echo or pr

	create from a file
		create or cr
		
	override from a file
		override or ov

	decode to a file
		decode or dec

	export to a file
		export ex

	list current one-liners
		list or ls

	delete a one-liner
		delete or rm

