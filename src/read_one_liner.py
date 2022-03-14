import base64
import argparse


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('oneliner', type=str, help='a')

args = parser.parse_args()
print(base64.b64decode(args.oneliner))
