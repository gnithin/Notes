import os
import re
from pprint import pprint
import copy
import sys

PRINT_LOG = False


class DirTree:
    sep = ";"
    default_struct = {
        "files": [],
        "dirs": {},
        "base_path": ""
    }
    link_prefix = "https://github.com/gnithin/Notes/tree/master/Notes/"

    def __init__(self, base_path):
        self.dir_tree = copy.deepcopy(self.default_struct)
        self.base_path = base_path

    def __get_obj_from_working_path(self, working_path):
        current_obj = self.dir_tree
        if working_path is not "":
            try:
                for key in working_path.split(self.sep):
                    if key not in current_obj["dirs"]:
                        current_obj["dirs"][key] = \
                            copy.deepcopy(self.default_struct)
                    current_obj = current_obj["dirs"][key]
            except Exception:
                if PRINT_LOG:
                    print(sys.exc_info()[0])
                current_obj = None
        return current_obj

    def add_values_to_tree(self, working_base_path, dirs, files):
        add_success = False

        if len(dirs) or len(files):
            try:
                working_path = self.get_path_from_base_path(working_base_path)
                current_obj = self.__get_obj_from_working_path(working_path)

                if current_obj:
                    if len(dirs):
                        for d in dirs:
                            current_obj["dirs"][d] = \
                                copy.deepcopy(self.default_struct)

                    if len(files):
                        for f in files:
                            current_obj["files"].append(f)

                    current_obj["base_path"] = working_path.replace(
                        self.sep,
                        "/"
                    ) + "/"
            except:
                print(sys.exc_info()[0])
            else:
                add_success = True

        return add_success

    def get_path_from_base_path(self, working_base_path):
        matched = (re.findall(self.base_path + r'(.+)', working_base_path))
        if len(matched):
            return matched[0].replace(os.sep, self.sep)
        return ""

    def print_tree(self):
        if PRINT_LOG:
            pprint(self.dir_tree)

    def get_text(self):
        current_obj = self.dir_tree
        return self.__text_from_tree(current_obj)

    def __text_from_tree(self, current_obj, level=0,
                         final_text="", dir_name=""):
        current_text = ""
        tab = " " * 2

        files = current_obj.get("files", None)
        base_path = current_obj.get("base_path", "")

        if files and len(files):
            if dir_name != "" and (level - 1) >= 0:
                current_text += "{0}- **{1}**\n".format(
                    tab*(level-1),
                    dir_name
                )

            for f in files:
                current_text += "{0}- [{1}]({2})\n".format(
                    tab*level,
                    self.format_file_name(f),
                    self.link_prefix + base_path + f
                )

        dirs = current_obj.get("dirs", None)
        if dirs and len(dirs):
            for d in dirs:
                current_text += self.__text_from_tree(
                    current_obj["dirs"][d],
                    level+1,
                    current_text,
                    d
                )

        return current_text

    def format_file_name(self, filename):
        return filename


class ReadmeMaker:
    START_LABEL = "<!-- LABEL_BEGIN -->\n"
    END_LABEL = "\n<!-- LABEL_END -->"

    def __init__(self, notes_path, readme_file_path):
        self.path = notes_path
        self.dir_tree = DirTree(notes_path)
        self.readme_file_path = readme_file_path
        self.get_all_files_dirs_from_path()

    def get_all_files_dirs_from_path(self):
        for (dirpath, dirnames, filenames) in os.walk(self.path):
            self.dir_tree.add_values_to_tree(dirpath, dirnames, filenames)

    def print_tree(self):
        self.dir_tree.print_tree()

    def get_text_from_tree(self):
        return self.dir_tree.get_text()

    def update_readme(self):
        did_update = False

        # Fetch the readme.
        with open(self.readme_file_path, 'r') as fp:
            readme_contents = (fp.read()).strip()

        if readme_contents != "":
            # Fetch the location between the thing is supposed to be written.
            start_label = self.START_LABEL
            end_label = self.END_LABEL
            start_index = readme_contents.find(start_label)
            end_index = readme_contents.find(end_label)

            # Get markdown string to be printed
            print_text = self.get_text_from_tree()

            # Insert markdown between labels
            new_contents = (readme_contents[:start_index + len(start_label)] +
                            print_text +
                            readme_contents[end_index:])

            # Writing the contents to the file
            try:
                with open(self.readme_file_path, 'w') as fw:
                    fw.write(new_contents)
            except:
                if PRINT_LOG:
                    print("Could not write to file")
                    print(sys.exc_info()[0])
            else:
                did_update = True
        return did_update


if __name__ == "__main__":
    notes_path = ".{0}Notes{0}".format(os.sep)
    readme_path = "README.md"

    rd_maker = ReadmeMaker(notes_path, readme_path)
    # rd_maker.print_tree()
    did_update = rd_maker.update_readme()

    if did_update:
        print("Updated :)")
        print(readme_path)
    else:
        print("Failed!")
