#!/usr/bin/env python3

import base64
import argparse
import os
import re
import parser
from os import path


class OneLiner:
    # change name mv
    modes = {"init":     ["init"],
             "create":   ["create", "cr", "touch"],
             "override": ["override", "ov"],
             "rename":   ["rename", "mv"],
             "print":    ["print", "pr", "cat"],
             "dump":     ["dump", "dmp"],
             "list":     ["list", "ls"],
             "delete":   ["delete", "del", "rm"]}

    one_liner_alias_file = os.environ["ONELINER_PATH"]
    one_liner_python_exec = os.environ["ONELINER_PYTHON_EXEC"]

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Make or read one-liner python executable commands without relying on any file.')
        self.parser.add_argument('mode',
                                 type=str,
                                 choices=[mode_cli for mode in OneLiner.modes for mode_cli in OneLiner.modes[mode]],
                                 help=OneLiner.create_mode_help_text(),
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
        self.parser.add_argument('--init_file_contents',
                                 type=str,
                                 default="",
                                 help='code for the one-liner')

        self.args = self.parser.parse_args()

    @staticmethod
    def create_mode_help_text():
        mode_help_text = "select mode: "
        for mode in OneLiner.modes:
            for i, mode_cli in enumerate(OneLiner.modes[mode]):
                if i == 0:
                    if len(OneLiner.modes[mode]) == 1:
                        mode_help_text += mode_cli + ", "
                    else:
                        mode_help_text += mode_cli + " [, "
                elif i != len(OneLiner.modes[mode]) - 1:
                    mode_help_text += mode_cli + ", "
                else:
                    mode_help_text += mode_cli + "], "
        return mode_help_text

    def init(self):
        print("Initializing...")

        one_liner_name = "one-liner"
        byte_array = self.args.init_file_contents.encode('utf-8')
        one_liner = "alias {}='{} -c \"import base64; decoded_string = base64.b64decode(b'\"'\"'{}'\"'\"').decode(); exec(decoded_string)\"'".format(one_liner_name, OneLiner.one_liner_python_exec, base64.b64encode(byte_array).decode("utf-8"))

        if self.args.verbose:
            print(one_liner)

        with open(OneLiner.one_liner_alias_file, 'a+', encoding='utf-8') as file:
            file.write("\n" + one_liner + "\n")

    def _handle_args_required(self, name_required=False, name_and_filepath_required=False):
        if name_and_filepath_required:
            if (not self.args.name) and self.args.filepath:
                self.parser.error("one-liner name is required for this mode! Specify it by --name [-n]")

            if (not self.args.filepath) and self.args.name:
                self.parser.error("one-liner name is required for this mode! Specify it by --filepath [-f]")

            if not (self.args.name and self.args.filepath):
                self.parser.error("one-liner name and filepath are required for this mode! Specify it by --name [-n] "
                                  "and --filepath [-f]")

        if name_required:
            if not self.args.name:
                self.parser.error("one-liner name is required for this mode! Specify it by --name [-n]")

    def handle(self):
        if self.args.mode in OneLiner.modes["init"]:
            self.init()
        elif self.args.mode in OneLiner.modes["print"]:
            self._handle_args_required(name_required=True)
            self._handle_print()
        elif self.args.mode in OneLiner.modes["create"]:
            self._handle_args_required(name_and_filepath_required=True)
            self._handle_create()
        elif self.args.mode in OneLiner.modes["override"]:
            self._handle_args_required(name_and_filepath_required=True)
            self._handle_override()
        elif self.args.mode in OneLiner.modes["dump"]:
            self._handle_args_required(name_required=True)
            self._handle_export()
        elif self.args.mode in OneLiner.modes["list"]:
            self._handle_list()
        elif self.args.mode in OneLiner.modes["delete"]:
            self._handle_args_required(name_required=True)
            self._handle_delete()
        else:
            self.parser.error("Invalid mode")

    def _handle_print(self):
        with open(OneLiner.one_liner_alias_file, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                if line.startswith("alias "):
                    oneliner_name = line.lstrip("alias ")[:line.lstrip("alias ").index("=")].strip(" ")
                    if oneliner_name == self.args.name:
                        print("\n\t" + line)
                        print("") if not line.endswith("\n") else None

    def _handle_create(self):
        one_liner_name = self.args.name if self.args.name != "" else self.args.filepath
        # one_liner_alias_file = path.expanduser('~') + '/.one-liner'

        with open(self.args.filepath, encoding='utf-8') as file:
            byte_array = file.read().encode('utf-8')

        one_liner = "alias {}='{} -c \"import base64; decoded_string = base64.b64decode(b'\"'\"'{}'\"'\"').decode(); exec(decoded_string)\"'".format(one_liner_name, OneLiner.one_liner_python_exec, base64.b64encode(byte_array).decode("utf-8"))

        if self.args.verbose:
            print(one_liner)

        with open(OneLiner.one_liner_alias_file, 'a+', encoding='utf-8') as file:
            file.write("\n" + one_liner + "\n")

        OneLiner._source()

    def _handle_override(self):
        with open(OneLiner.one_liner_alias_file, 'r+', encoding='utf-8') as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                line_to_override = False

                if line.startswith("alias "):
                    oneliner_name = line.lstrip("alias ")[:line.lstrip("alias ").index("=")].strip(" ")
                    if oneliner_name == self.args.name:
                        line_to_override = True

                        one_liner_name = self.args.name if self.args.name != "" else self.args.filepath

                        with open(self.args.filepath, encoding='utf-8') as new_file:
                            byte_array = new_file.read().encode('utf-8')

                        one_liner = "alias {}='{} -c \"import base64; decoded_string = base64.b64decode(b'\"'\"'{}'\"'\"').decode(); exec(decoded_string)\"'".format(
                            one_liner_name, OneLiner.one_liner_python_exec,
                            base64.b64encode(byte_array).decode("utf-8"))

                        file.write(one_liner)

                if not line_to_override:
                    file.write(line)
            file.truncate()
        OneLiner._source()

    def _handle_decode(self):
        with open(OneLiner.one_liner_alias_file, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                if line.startswith("alias "):
                    oneliner_name = line.lstrip("alias ")[:line.lstrip("alias ").index("=")].strip(" ")
                    if oneliner_name == self.args.name:
                        b = line[line.index("base64.b64decode(b'")+len("base64.b64decode(b'"):line.index("').decode();")]
                        print(base64.b64decode(b).decode())

    def _handle_export(self):
        with open(OneLiner.one_liner_alias_file, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                if line.startswith("alias "):
                    oneliner_name = line.lstrip("alias ")[:line.lstrip("alias ").index("=")].strip(" ")
                    if oneliner_name == self.args.name:
                        base64_code = re.search("'\"'\"'.*'\"'\"'", line).group().strip("'\"'\"'")

                        if not self.args.filepath:
                            print("filepath is not specified, dumping to the terminal\n")
                            print("*" * 50)
                            print(base64.b64decode(base64_code).decode("utf-8"))
                            print("*" * 50)
                        else:
                            print("filepath is specified, saving to that file")

                            filepath = str(self.args.filepath)
                            filepath = filepath + ".py" if not filepath.endswith(".py") else filepath
                            try:
                                with open(filepath, 'x', encoding='utf-8') as new_file:
                                    new_file.write(base64.b64decode(base64_code).decode("utf-8"))
                            except FileExistsError:
                                print("Override protection: This file already exists!")

    def _handle_list(self):
        with open(OneLiner.one_liner_alias_file, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                if line.startswith("alias "):
                    print(line.lstrip("alias ")[:line.lstrip("alias ").index("=")].strip(" "))

    def _handle_delete(self):
        with open(OneLiner.one_liner_alias_file, 'r+', encoding='utf-8') as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                line_to_delete = False

                if line.startswith("alias "):
                    oneliner_name = line.lstrip("alias ")[:line.lstrip("alias ").index("=")].strip(" ")
                    if oneliner_name == self.args.name:
                        line_to_delete = True

                if not line_to_delete:
                    file.write(line)
            file.truncate()

    @staticmethod
    def _source():
        print("\nExecute the following in shell for changes to take effect:")
        print("\t$ source {}\n".format(OneLiner.one_liner_alias_file))


if __name__ == "__main__":
    oneLiner = OneLiner()
    oneLiner.handle()

