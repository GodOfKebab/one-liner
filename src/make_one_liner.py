import base64
import argparse


parser = argparse.ArgumentParser(description='Make one-liner python executable commands without relying on any files.')
parser.add_argument('filepath', type=str, help='path for the python file to be converted to one-liner')
parser.add_argument('--name', type=str, default="", help='alias name for the one-liner')
parser.add_argument('--alias_file', type=str, default="", help='alias file for the one-liner')

args = parser.parse_args()
file_path = args.filepath
one_liner_name = args.name if args.name != "" else file_path.split('/')[-1].rstrip('.py')
one_liner_alias_file = args.alias_file if args.alias_file != "" else '~/.bash_aliases'

with open(file_path, encoding='utf-8') as file:
    byte_array = file.read().encode('utf-8')

print("\nalias one-liner-{}=\"python3 -c \\\"import base64; decoded_string = base64.b64decode({}).decode(); exec(decoded_string)\\\"\"\n".format(one_liner_name, base64.b64encode(byte_array)))

with open(one_liner_alias_file, 'a+', encoding='utf-8') as file:
    one_liner_alias_file_str = file.read()

print(one_liner_alias_file_str)