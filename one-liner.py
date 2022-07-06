#!/usr/bin/env python3

import base64
import argparse
import sys
import os
import re
import logging
import zlib


class OneLiner:
    class Args(argparse.Namespace):
        mode = name = filepath = script = verb = ""
        verbose = yes = False

    class Formatter:
        rocket = '🚀'
        bang = '💥'
        lightning = '⚡️'
        thumbsup = '👍'
        writing = '💾'
        lookbelow = '👇'
        checkmark = '✅'
        warning = '⚠️'
        crossmark = '❌ '

        def green_text(self, format_str):
            return '\033[92m' + format_str + '\033[0m'

        def red_text(self, format_str):
            return '\033[91m' + format_str + '\033[0m'

        def bold_text(self, format_str):
            return '\033[1m' + format_str + '\033[0m'

        def underline_text(self, format_str):
            return '\033[4m' + format_str + '\033[0m'

    def __init__(self, cmd_args):
        self.modes = {
            "init": ["init"],
            "create": ["create", "cr", "touch"],
            "override": ["override", "ov"],
            "rename": ["rename", "mv"],
            "print": ["print", "pr", "echo"],
            "dump": ["dump", "dmp", "export", "cat"],
            "list": ["list", "ls"],
            "delete": ["delete", "del", "rm"],
            "fix": ["fix", "format"],
            "sync": ["sync"]
        }

        self.mode_desc_dict = {
            "init": "initialize the .one-liner file",
            "create": "create and add one-liner",
            "override": "create and override one-liner",
            "rename": "rename a one-liner",
            "print": "print the alias line of one-liner",
            "dump": "decode the one-liner and dump it either on the shell or to a file",
            "list": "list the all one-liners",
            "delete": "remove a one-liner",
            "fix": "fix .one-liner file by parsing and construct the .one-liner file again",
            "sync": "encrypt all the one-liners and sync with the one-liner servers (not functional)",
        }
        # make sure that the aliases are correctly interpreted
        for mode in list(self.mode_desc_dict.keys()).copy():
            for mode_alias in self.modes[mode]:
                self.mode_desc_dict[mode_alias] = self.mode_desc_dict[mode]

        self.one_liner_alias_file = os.environ["ONELINER_PATH"]
        self.one_liner_python_exec = os.environ["ONELINER_PYTHON_EXEC"]

        self.logger = logging.getLogger('one-liner')
        self.logger.setLevel(logging.WARNING)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        self.logger.addHandler(ch)

        self.cmd_args = cmd_args

        self.help_only = self.cmd_args in [['-h'], ['--help']]

        # Check to see if the only argument is the -h or --help
        self.mode_parser = argparse.ArgumentParser(add_help=self.help_only,
                                                   description='Manage one-liner python executable commands '
                                                               'without relying on the original script file.'
                                                               'To view the required arg(s) for each of the modes, '
                                                               'add the help flag (-h) to the mode. '
                                                               'For example, -> one-liner create -h',
                                                   usage="one-liner [-h] [-v] mode [mode-specific-required-args]...",
                                                   formatter_class=argparse.RawTextHelpFormatter)
        self.mode_parser.add_argument('mode', type=str, metavar='mode',
                                      choices=[mode_cli for mode in self.modes for mode_cli in self.modes[mode]],
                                      help=self.modes_help() if self.help_only else argparse.SUPPRESS)
        self.mode_parser.add_argument("-v", "--verbose", default=False, action="store_true",
                                      help="enable debug printing")
        self.mode_parser.add_argument("-y", "--yes", default=False, action="store_true",
                                      help="skip the 'Do you want to continue? [y/N]' prompt")
        self.args = OneLiner.Args()

        self.fmt = OneLiner.Formatter()

    def parse_cli(self):
        try:
            self.mode_parser.parse_known_args(self.cmd_args, namespace=self.args)
        except SystemExit as e:
            if e.code == 2:  # if a parsing error occurs, print help
                OneLiner(['--help']).parse_cli()
            if self.help_only or e.code == 2:
                raise SystemExit

        mode_specific_parser = argparse.ArgumentParser(parents=[self.mode_parser],
                                                       description=self.mode_description(),
                                                       formatter_class=argparse.RawTextHelpFormatter)
        # modes that require/hold-it-optional one-liner name
        modes_name = ["create", "override", "rename", "print", "dump", "delete"]
        if self.args.mode in [a for l in self.modes.items() if l[0] in modes_name for a in l[1]]:
            nargs = "?" if self.args.mode in self.modes["create"] else None
            nargs = 2 if self.args.mode in self.modes["rename"] else nargs
            mode_specific_parser.add_argument('name', type=str, default="",
                                              nargs=nargs,
                                              help='alias name for the one-line. If rename mode, first name is the old'
                                                   ' and the second name is the new name.')
        # modes that require/hold-it-optional one-liner filepath
        modes_name = ["create", "override", "dump"]
        if self.args.mode in [a for l in self.modes.items() if l[0] in modes_name for a in l[1]]:
            mode_specific_parser.add_argument('filepath', type=str, default="",
                                              nargs="?" if self.args.mode in self.modes["dump"] else None,
                                              help='file path for the python script to be converted to/from one-liner')
        # modes that require verb (pull/push)
        modes_name = ["sync"]
        if self.args.mode in [a for l in self.modes.items() if l[0] in modes_name for a in l[1]]:
            mode_specific_parser.add_argument('verb', type=str, choices=["pull", "push"],
                                              nargs="?",
                                              help='[CURRENTLY NOT IMPLEMENTED] '
                                                   'if left empty, the program if upload if the last upload was made '
                                                   'from this computer. To override this, specify verb (pull/push)')
        # modes that require script
        modes_name = ["init"]
        if self.args.mode in [a for l in self.modes.items() if l[0] in modes_name for a in l[1]]:
            mode_specific_parser.add_argument('script', type=str, help='code for the one-liner as a string')

        mode_specific_parser.usage = mode_specific_parser.format_usage(). \
            replace('usage: -c', 'one-liner ' + self.args.mode)
        mode_specific_parser.parse_args(self.cmd_args, namespace=self.args)

        if self.args.verbose:
            self.logger.setLevel(logging.DEBUG)

    def modes_help(self):
        mode_help_text = ""
        for mode in self.modes:
            for i, mode_cli in enumerate(self.modes[mode]):
                if i == 0:
                    if len(self.modes[mode]) == 1:
                        mode_help_text += mode_cli + " -> \t" + self.mode_desc_dict[mode] + "\n"
                    else:
                        mode_help_text += mode_cli + "\t[aliases: "
                elif i != len(self.modes[mode]) - 1:
                    mode_help_text += mode_cli + ", "
                else:
                    mode_help_text += mode_cli + "]" + " -> \t" + self.mode_desc_dict[mode] + "\n"
        return mode_help_text.rstrip(" ").rstrip(",")

    def mode_description(self):
        return "selected mode -> " + self.args.mode + ": " + self.mode_desc_dict[self.args.mode]

    def handle(self):
        self.parse_cli()
        oneLinerDB = self.parse_doc()

        if self.args.mode in self.modes["init"]:
            self._handle_init(oneLinerDB, self.args.script)
        elif self.args.mode in self.modes["print"]:
            self._handle_print(oneLinerDB, self.args.name)
        elif self.args.mode in self.modes["create"]:
            self._handle_create_override(oneLinerDB, self.args.name, self.args.filepath)
        elif self.args.mode in self.modes["override"]:
            self._handle_create_override(oneLinerDB, self.args.name, self.args.filepath, override=True)
        elif self.args.mode in self.modes["rename"]:
            self._handle_rename(oneLinerDB, self.args.name[0], self.args.name[1])
        elif self.args.mode in self.modes["dump"]:
            self._handle_export(oneLinerDB, self.args.name, self.args.filepath)
        elif self.args.mode in self.modes["list"]:
            self._handle_list(oneLinerDB)
        elif self.args.mode in self.modes["delete"]:
            self._handle_delete(oneLinerDB, self.args.name)
        elif self.args.mode in self.modes["fix"]:
            self.construct_doc(oneLinerDB)
        elif self.args.mode in self.modes["sync"]:
            self._handle_sync(oneLinerDB, self.args.verb)

    def parse_doc(self):
        oneLinerDB = {"info_and_params": {"contents": ""}}
        with open(self.one_liner_alias_file, 'r', encoding='utf-8') as file:
            saving_info_and_params = True
            pre_comments = entire_alias = post_comments = ""

            lines = file.readlines()
            lines.append("")
            for i, line in enumerate(lines):
                stripped_line = line.strip("\n").strip(" ")

                if saving_info_and_params:
                    oneLinerDB["info_and_params"]["contents"] += stripped_line + "\n"
                else:
                    if (len(stripped_line) == 0 or i == len(lines) - 1 or stripped_line.startswith("alias ")) and \
                            (len(entire_alias) > 0):
                        alias_name = entire_alias.lstrip("alias").split("=")[0].strip(" ")

                        if not stripped_line.startswith("alias "):
                            post_comments += stripped_line
                        post_comments = post_comments.strip("\n")
                        oneLinerDB[alias_name] = {"entire_line": entire_alias,
                                                  "comments": [pre_comments.strip("\n"),
                                                               post_comments.strip("\n")]
                                                  }
                        pre_comments = entire_alias = post_comments = ""
                        if stripped_line.startswith("alias "):
                            entire_alias = stripped_line
                    else:
                        if re.search("^alias( +)[a-zA-Z0-9-_]+=('.*'|\".*\")$", stripped_line):
                            entire_alias = stripped_line
                        elif len(entire_alias) == 0:
                            pre_comments += stripped_line + "\n"
                        elif len(entire_alias) > 0:
                            post_comments += stripped_line + "\n"

                    if len(stripped_line) == 0:
                        pre_comments = ""

                if stripped_line.startswith("# PARAMETERS END"):
                    saving_info_and_params = False
                    oneLinerDB["info_and_params"]["contents"] = oneLinerDB["info_and_params"]["contents"].rstrip("\n")

        return oneLinerDB

    def construct_doc(self, oneLinerDB):
        with open(self.one_liner_alias_file, 'w', encoding='utf-8') as file:
            file.write(oneLinerDB["info_and_params"]["contents"] + "\n")
            oneLinerDB.pop("info_and_params")

            sorted_one_liners = sorted(oneLinerDB.keys())
            sorted_one_liners.remove("one-liner")
            sorted_one_liners.insert(0, "one-liner")
            for one_liner in sorted_one_liners:
                one_liner_payload = ""
                if oneLinerDB[one_liner]["comments"][0]:
                    one_liner_payload += oneLinerDB[one_liner]["comments"][0] + "\n"
                one_liner_payload += oneLinerDB[one_liner]["entire_line"] + "\n"
                if oneLinerDB[one_liner]["comments"][1]:
                    one_liner_payload += oneLinerDB[one_liner]["comments"][1] + "\n"

                file.write("\n" + one_liner_payload + "\n")

    def _handle_init(self, oneLinerDB, script):
        print("{} Initializing...".format(self.fmt.rocket))

        self._handle_create_override(oneLinerDB, "one-liner", script.encode('utf-8'), init=True)

        # add the "source $HOME/.one-liner" to the .bashrc/.zshrc
        rc_file = "{}/.{}rc".format(os.environ["HOME"], os.environ["SHELL"].split("/")[-1])

        # check for existing "source $HOME/.one-liner"
        source_exists = False
        with open(rc_file, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                if re.search("^( *|)source ( *|)" + self.one_liner_alias_file, line):
                    source_exists = True

        if not source_exists:
            with open(rc_file, 'a', encoding='utf-8') as file:
                file.write("\nsource {}\n".format(self.one_liner_alias_file))

        print("All set! {} You can start using one-liner after sourcing! {}".
              format(self.fmt.checkmark, self.fmt.lightning))

    def _handle_print(self, oneLinerDB, name):
        try:
            print("\n\t" + oneLinerDB[name]["entire_line"] + "\n")
        except KeyError:
            self.logger.error("This one-liner doesn't exist! {}".format(self.fmt.crossmark))

    def _handle_create_override(self, oneLinerDB, name, filepath, override=False, init=False):
        one_liner_name = name if name != "" else filepath.rstrip(".py").split("/")[-1]

        byte_array = filepath if init else open(filepath, encoding='utf-8').read().encode('utf-8')

        base64_zlib_result = base64.b64encode(zlib.compress(byte_array, 9)).decode("utf-8")
        one_liner = "alias {}='{} -c \"import base64; import zlib; decoded_string = zlib.decompress(base64.b64decode(" \
                    "b'\"'\"'{}'\"'\"')).decode(); exec(decoded_string)\"'".format(one_liner_name,
                                                                                   self.one_liner_python_exec,
                                                                                   base64_zlib_result)
        # check for the conflicts between the mode selected and the provided args
        mode_args_no_conflict = ((one_liner_name not in oneLinerDB.keys()) and not override) or \
                             ((one_liner_name in oneLinerDB.keys()) and (override))
        # edit the temporary DB object but hold to check mode
        oneLinerDB[one_liner_name] = {"entire_line": one_liner,
                                      "comments": ['', "{} sync below {}".format("#" * 10, "#" * 10) if init else '']}
        action = ""
        if mode_args_no_conflict:
            self.construct_doc(oneLinerDB)
            action = "Creating" if not override else "Overwriting"
        else:
            if init:
                self._ask_approval("Existing one-liner setup found! Only the one-liner tool will be {} {}".
                                   format(self.fmt.bold_text("overridden"), self.fmt.warning))
                action = "Overwriting"
            elif override:
                self._ask_approval("The one-liner '{}' does not exist and a new one will be created {}".
                                   format(self.fmt.bold_text(one_liner_name), self.fmt.warning))
                action = "Creating"
            else:
                self._ask_approval("The one-liner '{}' already exists and will be {} {}".
                                   format(self.fmt.bold_text(one_liner_name), self.fmt.bold_text("overridden"),
                                          self.fmt.warning))
                action = "Overwriting"
            self.construct_doc(oneLinerDB)

        print("{} one-liner '{}' is successful {}".format(action, self.fmt.bold_text(one_liner_name), self.fmt.bang))
        self._source()

    def _handle_rename(self, oneLinerDB, old_name, new_name):
        try:
            popped = oneLinerDB.pop(old_name)
            popped['entire_line'] = "alias " + new_name + \
                                    popped['entire_line'].lstrip(" ").lstrip("alias").lstrip(" ").lstrip(old_name)
            oneLinerDB[new_name] = popped
            self._ask_approval("You are about to rename a one-liner from '{}' to '{}' {}".
                               format(self.fmt.bold_text(old_name), self.fmt.bold_text(new_name), self.fmt.warning))
            print("Renaming '{}' to '{}' is successful {}".
                  format(self.fmt.bold_text(old_name), self.fmt.bold_text(new_name), self.fmt.bang))
            self.construct_doc(oneLinerDB)
        except KeyError:
            self.logger.error("This one-liner doesn't exist! {}".format(self.fmt.crossmark))

    def _handle_export(self, oneLinerDB, name, filepath):
        try:
            base64_code = re.search("'\"'\"'.*'\"'\"'", oneLinerDB[name]["entire_line"]).group().strip("'\"'\"'")
            if filepath:
                print("filepath is specified {}, saving to that file {}".format(self.fmt.checkmark, self.fmt.writing))
                with open(filepath, 'x', encoding='utf-8') as new_file:
                    new_file.write(zlib.decompress(base64.b64decode(base64_code)).decode())
            else:
                self.logger.warning("filepath is not specified {}, dumping to the terminal {}".
                                    format(self.fmt.crossmark, self.fmt.lookbelow))
                print("{}\n{}\n{}".format("*" * 50, zlib.decompress(base64.b64decode(base64_code)).decode(), "*" * 50))
        except KeyError:
            self.logger.error("This one-liner doesn't exist! {}".format(self.fmt.crossmark))
        except FileExistsError:
            self.logger.warning("Override protection: This file already exists! {}".format(self.fmt.warning))
            self._ask_approval("The existing file will be overwritten.")
            base64_code = re.search("'\"'\"'.*'\"'\"'", oneLinerDB[name]["entire_line"]).group().strip("'\"'\"'")
            with open(filepath, 'w', encoding='utf-8') as new_file:
                new_file.write(zlib.decompress(base64.b64decode(base64_code)).decode())

    def _handle_list(self, oneLinerDB):
        for one_liner in sorted(oneLinerDB.keys()):
            print(one_liner) if one_liner not in ["one-liner", "info_and_params"] else None

    def _handle_delete(self, oneLinerDB, name):
        try:
            oneLinerDB.pop(name)
            self._ask_approval("You are about to {} the one-liner: '{}' {}".
                               format(self.fmt.bold_text("delete"), self.fmt.bold_text(name), self.fmt.warning))
            print("Deleting '{}' is successful {}".format(self.fmt.bold_text(name), self.fmt.bang))
            self.construct_doc(oneLinerDB)
        except KeyError:
            self.logger.error("This one-liner doesn't exist! {}".format(self.fmt.crossmark))

    def _handle_sync(self, oneLinerDB, verb):
        self.logger.warning("This feature isn't implemented yet.")

        from cryptography.fernet import Fernet

        one_liners = sorted(oneLinerDB.keys())
        one_liners.remove("one-liner")
        one_liners.remove("info_and_params")
        byte_code = b""
        for one_liner in one_liners:
            for part in [oneLinerDB[one_liner]["comments"][0],
                         oneLinerDB[one_liner]["entire_line"],
                         oneLinerDB[one_liner]["comments"][1]]:
                byte_code += (part + "\n").encode("utf-8")
        if self.args.verbose:
            print(byte_code, end="\n\n")
        byte_code = zlib.compress(byte_code, 9)

        key = Fernet.generate_key()
        f = Fernet(key)
        ciphertext = f.encrypt(byte_code)
        if self.args.verbose:
            print("The size of the ciphertext is {} KB".format(len(ciphertext) / 1024.))
            print(ciphertext, end="\n\n")
        decrypted_msg = f.decrypt(ciphertext)
        decrypted_msg = zlib.decompress(decrypted_msg)
        if self.args.verbose:
            print(decrypted_msg, end="\n\n")

    def _source(self):
        print("\n{} Execute the following in shell for changes to take effect:".format(self.fmt.thumbsup))
        print("\tsource {}\n".format(self.one_liner_alias_file))

    def _ask_approval(self, statement):
        if self.args.yes:
            return
        # if not replied 'y', abort
        try:
            if input(statement + " Do you want to continue? [y/N] ").strip(" ").lower() != 'y':
                print("Aborting... {}".format(self.fmt.crossmark))
                raise SystemExit
        except KeyboardInterrupt:
            print("\nAborting... {}".format(self.fmt.crossmark))
            raise SystemExit


if __name__ == "__main__":
    oneLiner = OneLiner(sys.argv[1:])
    oneLiner.handle()
