#!/usr/bin/env python3

import base64
import argparse
import os
import re
import logging
import zlib


class OneLiner:
    def __init__(self):
        self.modes = {"init": ["init"],
                      "create": ["create", "cr", "touch"],
                      "override": ["override", "ov"],
                      "rename": ["rename", "mv"],
                      "print": ["print", "pr", "echo"],
                      "dump": ["dump", "dmp", "export", "cat"],
                      "list": ["list", "ls"],
                      "delete": ["delete", "del", "rm"],
                      "fix": ["fix", "format"],
                      "sync": ["sync"]}

        self.one_liner_alias_file = os.environ["ONELINER_PATH"]
        self.one_liner_python_exec = os.environ["ONELINER_PYTHON_EXEC"]

        self.logger = logging.getLogger('one-liner')
        self.logger.setLevel(logging.WARNING)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        self.logger.addHandler(ch)

        self.parser = argparse.ArgumentParser(
            description='Make or read one-liner python executable commands without relying on that script file.')
        self.parser.add_argument('mode',
                                 type=str,
                                 choices=[mode_cli for mode in self.modes for mode_cli in self.modes[mode]],
                                 help=self.create_mode_help_text(),
                                 metavar='mode')
        self.parser.add_argument('-n', '--name',
                                 type=str,
                                 default="",
                                 help='alias name for the one-liner')
        self.parser.add_argument('-f', '--filepath',
                                 type=str,
                                 help='path for the python file to be converted to one-liner')
        self.parser.add_argument("-v", "--verbose",
                                 help="enable debug printing",
                                 action="store_true")
        self.parser.add_argument('--script',
                                 type=str,
                                 default="",
                                 help='code for the one-liner as a string')
        self.args = None
        self.verbose = False

    def parse_cli(self):
        self.args = self.parser.parse_args()
        if self.args.verbose:
            self.verbose = True
            self.logger.setLevel(logging.DEBUG)

    def create_mode_help_text(self):
        mode_help_text = "select mode: "
        for mode in self.modes:
            for i, mode_cli in enumerate(self.modes[mode]):
                if i == 0:
                    if len(self.modes[mode]) == 1:
                        mode_help_text += mode_cli + ", "
                    else:
                        mode_help_text += mode_cli + " [, "
                elif i != len(self.modes[mode]) - 1:
                    mode_help_text += mode_cli + ", "
                else:
                    mode_help_text += mode_cli + "], "
        return mode_help_text

    def _args_req(self, name=False, name_filepath=False, script_required=False):
        msg = "one-liner {} required for this mode! Specify it by {}"
        if name_filepath and not (self.args.name or self.args.filepath):
            msg = msg.format("name and filepath are", "--name [-n] and --filepath [-f]")
        if name_filepath and ((not self.args.filepath) and self.args.name):
            msg = msg.format("filepath is", "--filepath [-f]")
        if (name or (name_filepath and self.args.filepath)) and not self.args.name:
            msg = msg.format("name is", "--name [-n]")
        if script_required and not self.args.script:
            msg = msg.format("script contents are", "--script")

        if msg != "one-liner {} required for this mode! Specify it by {}":
            self.logger.error(msg)
            exit(-1)

    def handle(self):
        self.parse_cli()
        oneLinerDB = self.parse_doc()

        if self.args.mode in self.modes["init"]:
            print("Initializing...")
            self._args_req(script_required=True)
            self._handle_init(oneLinerDB, self.args.script)
        elif self.args.mode in self.modes["print"]:
            self._args_req(name=True)
            self._handle_print(oneLinerDB, self.args.name)
        elif self.args.mode in self.modes["create"]:
            self._args_req(name=True)
            self._handle_create_override(oneLinerDB, self.args.name, self.args.filepath)
        elif self.args.mode in self.modes["override"]:
            self._args_req(name_filepath=True)
            self._handle_create_override(oneLinerDB, self.args.name, self.args.filepath, True)
        elif self.args.mode in self.modes["rename"]:
            self._args_req(name=True)
            self._handle_rename(oneLinerDB, self.args.name)
        elif self.args.mode in self.modes["dump"]:
            self._args_req(name=True)
            self._handle_export(oneLinerDB, self.args.name, self.args.filepath)
        elif self.args.mode in self.modes["list"]:
            self._handle_list(oneLinerDB)
        elif self.args.mode in self.modes["delete"]:
            self._args_req(name=True)
            self._handle_delete(oneLinerDB, self.args.name)
        elif self.args.mode in self.modes["fix"]:
            self.construct_doc(oneLinerDB)
        elif self.args.mode in self.modes["sync"]:
            self._handle_sync(oneLinerDB)
        else:
            self.parser.error("Invalid mode")

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

        print("All set. You can start using one-liner after sourcing.")

    def _handle_print(self, oneLinerDB, name):
        try:
            print("\n\t" + oneLinerDB[name]["entire_line"] + "\n")
        except KeyError:
            self.logger.error("This one-liner doesn't exist!")

    def _handle_create_override(self, oneLinerDB, name, filepath, override=False, init=False):
        one_liner_name = name if name != "" else filepath.rstrip(".py")

        if init:
            byte_array = filepath
        else:
            with open(filepath, encoding='utf-8') as file:
                byte_array = file.read().encode('utf-8')

        base64_zlib_result = base64.b64encode(zlib.compress(byte_array, 9)).decode("utf-8")
        one_liner = "alias {}='{} -c \"import base64; import zlib; decoded_string = zlib.decompress(base64.b64decode(" \
                    "b'\"'\"'{}'\"'\"')).decode(); exec(decoded_string)\"'".format(one_liner_name,
                                                                                   self.one_liner_python_exec,
                                                                                   base64_zlib_result)

        if (one_liner_name not in oneLinerDB.keys() and not override) or \
                (one_liner_name in oneLinerDB.keys() and override):
            if init:
                oneLinerDB[one_liner_name] = {"entire_line": one_liner,
                                              "comments": ['', "#" * 10 + " sync below " + "#" * 10]}
            else:
                oneLinerDB[one_liner_name] = {"entire_line": one_liner, "comments": ['', '']}
            self.construct_doc(oneLinerDB)
            self._source()
        else:
            msg = "This one-liner {}. If you want to {}, use the {} mode({})"
            if not override:
                msg = msg.format("already exists", "override", "override", self.modes["override"])
            else:
                msg = msg.format("does not  exist", "create", "create", self.modes["create"])
            self.logger.error(msg)

    def _handle_rename(self, oneLinerDB, name):
        try:
            self.logger.error("This feature isn't implemented yet!")
            # popped = oneLinerDB.pop(name)
            # new_name = name # TODO: add option for the second name
            # oneLinerDB[new_name] = popped
            # OneLiner.construct_doc(oneLinerDB)
        except KeyError:
            self.logger.error("This one-liner doesn't exist!")

    def _handle_export(self, oneLinerDB, name, filepath):
        try:
            base64_code = re.search("'\"'\"'.*'\"'\"'", oneLinerDB[name]["entire_line"]).group().strip("'\"'\"'")
            if not filepath:
                self.logger.warning("filepath is not specified, dumping to the terminal")
                print("{}\n{}\n{}".format("*" * 50, zlib.decompress(base64.b64decode(base64_code)).decode(), "*" * 50))
            else:
                print("filepath is specified, saving to that file")
                with open(filepath, 'x', encoding='utf-8') as new_file:
                    new_file.write(zlib.decompress(base64.b64decode(base64_code)).decode())
        except KeyError:
            self.logger.error("This one-liner doesn't exist!")
        except FileExistsError:
            self.logger.error("Override protection: This file already exists!")

    def _handle_list(self, oneLinerDB):
        for one_liner in sorted(oneLinerDB.keys()):
            print(one_liner) if one_liner not in ["one-liner", "info_and_params"] else None

    def _handle_delete(self, oneLinerDB, name):
        try:
            oneLinerDB.pop(name)
            self.construct_doc(oneLinerDB)
        except KeyError:
            self.logger.error("This one-liner doesn't exist!")

    def _handle_sync(self, oneLinerDB):
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
        if self.verbose:
            print(byte_code, end="\n\n")
        byte_code = zlib.compress(byte_code, 9)

        key = Fernet.generate_key()
        f = Fernet(key)
        ciphertext = f.encrypt(byte_code)
        if self.verbose:
            print("The size of the ciphertext is {} KB".format(len(ciphertext) / 1024.))
            print(ciphertext, end="\n\n")
        decrypted_msg = f.decrypt(ciphertext)
        decrypted_msg = zlib.decompress(decrypted_msg)
        if self.verbose:
            print(decrypted_msg, end="\n\n")

    def _source(self):
        print("\nExecute the following in shell for changes to take effect:")
        print("\tsource {}\n".format(self.one_liner_alias_file))


if __name__ == "__main__":
    oneLiner = OneLiner()
    oneLiner.handle()

