import subprocess

import src.TextFormatting as tf
import json
import subprocess
import os
import re


class MacularScriptLauncher:
    def __init__(self, path_config_file):
        # TODO Voir si je peux mettre certaine méthodes privées avec un underscores
        # TODO Ajouter la création du path_macudata s'il n'existe pas. "check_and_create_path"
        # TODO Rendre les tests de code embarqués dans le dossier en créant les fichiers nécessaires
        self.dict_config = self.read_config_file(path_config_file)
        self._reg_ext_file = re.compile(".*/(.*?"+re.escape(".")+".*?$)")

    @property
    def n_sim(self):
        return self._n_sim

    @property
    def path_macufile(self):
        return self._path_macufile

    @property
    def path_macudata(self):
        return self._path_macudata

    @property
    def path_macustim(self):
        return self._path_macustim

    @property
    def path_macugraph(self):
        return self._path_macugraph

    @property
    def params_dict(self):
        return self._params_dict

    @property
    def dict_formatting_alias(self):
        return self._dict_formatting_alias

    @property
    def dict_config(self):
        return self._dict_config

    @dict_config.setter
    def dict_config(self, dictionary):
        #TODO utiliser dictionnaire ou plutôt directement un path de fichier init.
        self.check_mandatory_params(dictionary)
        self._n_sim = dictionary["n_sim"]
        self._path_macufile = ""
        self._path_macudata = ""
        self._path_macustim = ""
        self._path_macugraph = ""
        self._params_dict = {}
        self._dict_formatting_alias = {}
        self.check_config_dict(dictionary)
        self._dict_config = dictionary


    @staticmethod
    def read_config_file(path_config_file):
        with open(path_config_file, "r") as outfile:
            return json.load(outfile)

    def check_list_length(self, list_params):
        if type(list_params) == list:
            if len(list_params) != self.n_sim and len(list_params) != 1:
                raise IndexError(f"List {list_params} is too long.\nSize must be of the length {self.n_sim} or 1.")

    def check_config_dict(self, dictionary):
        # Check if dict config have the correct structure.
        self.check_dict_type(dictionary)
        self.check_path_type(dictionary["path_macufile"])
        self.check_path_type(dictionary["path_macudata"])

        try:
            self.check_path_type(dictionary["path_macustim"])
        except KeyError:
            pass

        try:
            self.check_path_type(dictionary["path_macugraph"])
        except KeyError:
            pass

        try:
            self.check_params_dict(dictionary["params_dict"])
        except KeyError:
            pass

        self.check_formatting_alias(dictionary)

    def check_formatting_alias(self, dictionary):
        for alias in dictionary:
            if alias not in ("path_macufile", "path_macudata", "path_macustim", "path_macugraph", "params_dict"):
                if type(dictionary[alias]) not in (int, list, str):
                    raise TypeError(f"Formatting alias values have to be int, list or str not "
                                    f"{type(dictionary[alias])}")
                self.check_list_length(dictionary[alias])

    @staticmethod
    def check_path_existing(path):
        if not os.path.isfile(path):
            raise FileNotFoundError(f"This path doesn't exist : {path}")

    def path_file_to_path_dir(self, path):
        # File "file.ext"
        try:
            file = self._reg_ext_file.findall(path)[0]
            path = path.replace(file, "")
        except IndexError:
            pass

        return path

    def create_non_existing_path(self, path):
        try:
            os.makedirs(self.path_file_to_path_dir(path))
        except FileExistsError:
            print("File exist already.")
            pass

    def check_path_type(self, paths):
        if type(paths) != str and type(paths) != list:
            raise TypeError("Path have to be list or str.")
        self.check_list_length(paths)

    @staticmethod
    def check_dict_type(dictionary):
        if type(dictionary) != dict:
            raise TypeError(f"Dict config must be a dictionary, not a {type(dictionary)}.")

    @staticmethod
    def check_mandatory_params(dictionary):
        try:
            type(dictionary["n_sim"])
            type(dictionary["path_macufile"])
            type(dictionary["path_macudata"])
        except KeyError:
            raise KeyError("Config dictionary must contains n_sim, path_macufile and path_macudata parameters.")

    def check_params_dict(self, params_dict):
        for param in params_dict:
            if type(param) != str:
                raise TypeError(f"Macular parameters must be str not {type(param)}.")
            if type(params_dict[param]) not in (int, list):
                raise TypeError(f"Macular parameter value must be int or list not "
                                f"{type(params_dict[param])}")
            self.check_list_length(params_dict[param])

    @staticmethod
    def next_element(param, i_sim):
        if type(param) == list:
            if len(param) == 1:
                param = param[0]
            else:
                param = param[i_sim]

        return param

    def refresh_dict_formatting_alias(self, i_sim):
        for alias in self.dict_config:
            if alias not in ("path_macufile", "path_macudata", "path_macustim", "path_macugraph", "params_dict",
                             "n_sim"):
                self._dict_formatting_alias[alias] = self.next_element(self.dict_config[alias], i_sim)

        try:
            for alias in self.dict_config["params_dict"]:
                self._dict_formatting_alias[f"{alias}_name"] = alias
                self._dict_formatting_alias[f"{alias}_value"] = self.next_element(
                    self.dict_config["params_dict"][alias], i_sim)
        except KeyError:
            pass

    def refresh_paths(self, i_sim):
        self._path_macufile = tf.TextFormatting(self.next_element(self.dict_config["path_macufile"], i_sim),
                                                self._dict_formatting_alias).to_str()
        self._path_macudata = tf.TextFormatting(self.next_element(self.dict_config["path_macudata"], i_sim),
                                                self._dict_formatting_alias).to_str()
        self.check_path_existing(self._path_macufile)
        self.create_non_existing_path(self._path_macudata)

        try:
            self._path_macustim = tf.TextFormatting(self.next_element(self.dict_config["path_macustim"], i_sim),
                                                    self._dict_formatting_alias).to_str()
            self.check_path_existing(self._path_macustim)
        except KeyError:
            pass

        try:
            self._path_macugraph = tf.TextFormatting(self.next_element(self.dict_config["path_macugraph"], i_sim),
                                                     self._dict_formatting_alias).to_str()
            self.check_path_existing(self._path_macugraph)
        except KeyError:
            pass

    def refresh_params_dict(self, i_sim):
        try:
            for param in self.dict_config["params_dict"]:
                self._params_dict[param] = self.next_element(self.dict_config["params_dict"][param], i_sim)
        except KeyError:
            pass

    def load_next_sim(self, i_sim):
        self.refresh_params_dict(i_sim)
        self.refresh_dict_formatting_alias(i_sim)
        self.refresh_paths(i_sim)

    def multiple_runs(self):
        for i_sim in range(self.n_sim):
            self.load_next_sim(i_sim)
            self.run()

    def run(self):
        list_subprocess = self.make_subprocess()
        subprocess.run(list_subprocess)

    def make_subprocess(self):
        list_subprocess = ["macular-batch", "-r",
                           "-f", f"{self.path_macufile}",
                           "-o", f"{self.path_macudata}"]

        if self.path_macustim != "":
            list_subprocess += ["-s", f"{self.path_macustim}"]
        if self.path_macugraph != "":
            list_subprocess += ["-g", f"{self.path_macugraph}"]

        for param in self.params_dict:
            list_subprocess += ["-p", f"{param}={self.params_dict[param]}"]

        print(list_subprocess)


        return list_subprocess
