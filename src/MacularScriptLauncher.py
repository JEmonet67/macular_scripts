import src.TextFormatting as tf
import json
import subprocess
import os
import re


class MacularScriptLauncher:
    """Automatic Macular simulation batch launcher.

    The Macular simulations launcher receives a json containing the setup of parameters to be used
    for the batch simulations to be carried out. These json parameters are store into the config dictionary.
    Once the launcher has been configured, the simulations can be started with the multiple_runs() method.

    When initialising a launcher or modifying the batch configuration dictionary it contains, all parameters are reset
    to ‘zero’. This means an empty character string for path_macufile, path_macudata, path_macustim and path_macugraph.
    This means an empty dictionary for params_dict and dict_formatting_alias. Their values will be updated before each
    new simulation based on the contents of the batch configuration dictionary (dict_config). This allows the set of
    parameters to be adapted for use in each simulation.

    It is possible to use formatting for the different file access paths. To do this, you will need to put the terms to
    be replaced in brackets. Once this is done, you will add this term as a key within the json that will be associated
    with a value corresponding to the alias by which it is to be replaced. It is also possible that the term
    in braces refers to one of the names of Macular parameters or its value present in params_dict. In this case, the
    name of the Macular parameter must be placed in braces, followed by the suffix ‘_name’ or ‘_value’. If the value is
    a floating point, the period will be replaced by a comma.
    The alias can vary between batch simulations if it is a list.

    Formatting example :
    RC_RM_dSGpCP{id_sim}_{name_caract_sim}{GanglionGainControl/h_G_value}{unit_caract_sim}_0f.csv

    JSON content :
    "params_dict": {"GanglionGainControl/h_G":0.215}
    "id_sim":0015,
    "name_caract_sim":"hGang",
    "unit_caract_sim":"mVps"

    Result :
    RC_RM_dSGpCP0015_hGang0,215mVps_0f.csv

    Attributes
    ----------
    dict_config : dict
        Macular batch configuration dictionary.

        This dictionary is initially loaded from a json file. It must contain three parameters: n_sim, path_macudata
        and path_macufile. It may also contain other optional parameters: path_macustim, path_macugraph and
        params_dict. Finally, it may contain the names of elements to be replaced by aliases. All these parameters
        can be contained in a list if it is desired that they vary between batch simulations. This list must be of a
        size equal to the number of simulations.

    n_sim : int
        Number of simulations to be carried out.

    path_macufile : str
        Location of the json file containing the configuration file of a Macular simulation obtained and created
        with the Macular software. In case of multiple simulations with different graphs path_macufile will be a
        list of str.

    path_macudata : str
        Location of the directory where Macular simulation data is saved. In the case of multiple simulations
        with different graphs, path_macudata will be a list of str.

    path_macustim : str
        Location of the stimulus video file to be used for the simulation. In the case of
        multiple simulations with different graphs, path_macustim will be a list of str.

    path_macugraph : str
        Location of the mac file of the Macular graph used for the simulation. In the case of multiple simulations
        with different graphs, path_macugraph will be a list of str.

    dict_formatting_alias : dict
        Dictionary containing all the terms to be replaced within the various file path parameters
        and the alias by which they are to be replaced. This alias must be an integer, a character string
        or a list in the case of multiple simulations.

        The names and values of the parameters in the Macular parameter dictionary (params_dict) are all added by
        default in the dict_formatting_alias. It is accessed with the parameter name and the suffix ‘_name’ or ‘_value’.

    params_dict : dict
        Dictionary of Macular parameters allowing the modification of the value of specific Macular parameters in the
        Macular batch simulations.

        This dictionary is formed from a dictionary named ‘params_dict’ and present in the batch configuration json.
        This dictionary associates a key corresponding to the name of the parameter to be modified and as a value a
        single value or a list of values if it is to be varied. It is important that the name of the parameter
        entered as the key corresponds to that present in the Macular configuration json file.

        Example :
        >> params_dict = {"virtual_retina/relative_ampOPL":[0.004, 0.0079, 0.0119]}

    reg_ext_file : re.Pattern
        Pattern regexp to identify the name of a file within a path to a file.

    Example
    ----------
    >> launcher = MacularScriptLauncher(path_dict_config)
    >> launcher.multiple_runs()

    """

    def __init__(self, path_config_file):
        """Init function to make a MacularScriptLauncher object.

        Parameters
        ----------
        path_config_file : str
            Path to the macular simulation batch configuration json file.
        """
        self.dict_config = self.read_config_file(path_config_file)
        self._reg_ext_file = re.compile(".*/(.*?" + re.escape(".") + ".*?$)")

    @property
    def n_sim(self):
        """Getter for the n_sim attribute."""
        return self._n_sim

    @property
    def path_macufile(self):
        """Getter for the path_macufile attribute."""
        return self._path_macufile

    @property
    def path_macudata(self):
        """Getter for the path_macudata attribute."""
        return self._path_macudata

    @property
    def path_macustim(self):
        """Getter for the path_macustim attribute."""
        return self._path_macustim

    @property
    def path_macugraph(self):
        """Getter for the path_macugraph attribute."""
        return self._path_macugraph

    @property
    def params_dict(self):
        """Getter for the params_dict attribute."""
        return self._params_dict

    @property
    def dict_formatting_alias(self):
        """Getter for the dict_formatting_alias attribute."""
        return self._dict_formatting_alias

    @property
    def dict_config(self):
        """Getter for the dict_config attribute."""
        return self._dict_config

    @dict_config.setter
    def dict_config(self, dict_config):
        """Setter for the dict_config attribute.

        Each time a new simulation batch configuration dictionary is added, all other attributes are updated. All path
        parameters (path_macufile, path_macudata, path_macustim, path_macugraph) are reset to an empty string so that
        they can be modified later during the simulations simulations. The same applies to params_dict and
        dict_formatting_alias, which are reset to empty dictionaries.
        The dictionary provided as input must contain path_macufile, path_macudata and n_sim.

        Parameters
        ----------
        dict_config : dict
            Macular batch configuration dictionary.
        """
        self.check_mandatory_params(dict_config)
        self._n_sim = dict_config["n_sim"]
        self._path_macufile = ""
        self._path_macudata = ""
        self._path_macustim = ""
        self._path_macugraph = ""
        self._params_dict = {}
        self._dict_formatting_alias = {}
        self.check_config_dict(dict_config)
        self._dict_config = dict_config

    @staticmethod
    def read_config_file(path_config_file):
        """Loading the configuration json file.

        Parameters
        ----------
        path_config_file : str
            Location of the configuration json file.

        Returns
        ----------
        dict
            Potential configuration dictionary of the simulation batch.
        """
        with open(path_config_file, "r") as outfile:
            return json.load(outfile)

    def check_list_length(self, list_params):
        """Verification of the length of the parameter lists.

        When a parameter must be varied within the Macular simulation batch, the length of the
        list must correspond to the number of simulations n_sim.

        Parameters
        ----------
        list_params : str
            List of values of a parameter to be varied during simulations.

        Raises
        ----------
        IndexError
            The index error is raised if the length of the verified list is not equal to the number of simulations.
        """
        if type(list_params) is list:
            if len(list_params) != self.n_sim and len(list_params) != 1:
                raise IndexError(f"List {list_params} is too long.\nSize must be of the length {self.n_sim} or 1.")

    def check_config_dict(self, dict_config):
        """Verification that the potential batch configuration dictionary has the correct structure.

        The verification is performed only on the parameters used subsequently as class attributes. We have
        path_macufile, path_macudata, path_macustim and path_macugraph, which must be a str or a list.
        We have params_dict, which must be a dictionary with keys that are str and values that are integers, floats
        or a list. Finally, the aliases must be integers, str or a list.

        Parameters
        ----------
        dict_config : dict
            Potential Macular batch configuration dictionary.
        """
        # Vérification des clés obligatoires.
        self.check_dict_type(dict_config)
        self.check_path_type(dict_config["path_macufile"])
        self.check_path_type(dict_config["path_macudata"])

        # Vérification des clés facultatifs.
        try:
            self.check_path_type(dict_config["path_macustim"])
        except KeyError:
            pass

        try:
            self.check_path_type(dict_config["path_macugraph"])
        except KeyError:
            pass

        try:
            self.check_params_dict(dict_config["params_dict"])
        except KeyError:
            pass

        self.check_formatting_alias(dict_config)

    def check_formatting_alias(self, dict_config):
        """Verification of the correct typology of the aliases used for the formatting of the other elements.

        The alias to replace the other elements must be an integer, a character string or a list of
        length n_sim.

        Parameters
        ----------
        dict_config : dict
            Potential Macular batch configuration dictionary.

        Raises
        ----------
        TypeError
            The type error is raised if one of the aliases is not an integer, a str or a list.
        """
        for alias in dict_config:
            if alias not in ("path_macufile", "path_macudata", "path_macustim", "path_macugraph", "params_dict"):
                if type(dict_config[alias]) not in (int, list, str):
                    raise TypeError(f"Formatting alias values have to be int, list or str not "
                                    f"{type(dict_config[alias])}")
                self.check_list_length(dict_config[alias])

    @staticmethod
    def check_path_existing(path):
        """Checking for the existence of a file path.

        Parameters
        ----------
        path : str
            File path whose existence must be verified.

        Raises
        ----------
        FileNotFoundError
            The file not found error is raised if the verified file path does not exist.
        """
        if not os.path.isfile(path):
            raise FileNotFoundError(f"This path doesn't exist : {path}")

    def path_file_to_path_dir(self, path):
        """Get path of directory within path to file.

        The function allows you to remove the file name, if there is one, to obtain only the directory path to
        this file.

        Parameters
        ----------
        path : str
            File path whose existence must be verified.

        Returns
        ----------
        str
            Directories path with no files at the end.
        """
        try:
            file = self._reg_ext_file.findall(path)[0]
            path = path.replace(file, "")
        except IndexError:
            pass

        return path

    def create_non_existing_path(self, path):
        """Creation of a non-existent file path.

        Parameters
        ----------
        path : str
            File path does not exist, please create it.
        """
        try:
            os.makedirs(self.path_file_to_path_dir(path))
        except FileExistsError:
            pass

    def check_path_type(self, paths):
        """Verification of the type of a file path.

        Parameters
        ----------
        paths : str or list
            File path to be evaluated.

        Raises
        ----------
        TypeError
            The type error is raised if the verified path is not a str or a list.
        """
        if type(paths) is not str and type(paths) is not list:
            raise TypeError("Path have to be list or str.")
        self.check_list_length(paths)

    @staticmethod
    def check_dict_type(dictionary):
        """Checking the type of a dictionary.

        Parameters
        ----------
        dictionary : dict
            Dictionary to be evaluated.

        Raises
        ----------
        TypeError
            The type error is raised if the verified dictionary is not one.
        """
        if type(dictionary) is not dict:
            raise TypeError(f"Dict config must be a dictionary, not a {type(dictionary)}.")

    @staticmethod
    def check_mandatory_params(dict_config):
        """Verification of the mandatory parameters in the configuration dictionary.

        The mandatory parameters are: path_macufile, path_macudata, n_sim.

        Parameters
        ----------
        dict_config : dict
            Potential configuration dictionary to evaluate the presence of mandatory parameters.

        Raises
        ----------
        KeyError
            The key error is raised if one of the keys n_sim, path_macufile or path_macudata is missing from
            dict_config.
        """
        try:
            type(dict_config["n_sim"])
            type(dict_config["path_macufile"])
            type(dict_config["path_macudata"])
        except KeyError:
            raise KeyError("Config dictionary must contains n_sim, path_macufile and path_macudata parameters.")

    def check_params_dict(self, params_dict):
        """Verification of the structure of the dictionary of parameters to be modified in the batch of simulations.

        Params_dict must be a dictionary whose keys are str and whose values are integers, floats or a
        list of length n_sim.

        Parameters
        ----------
        params_dict : dict
            Dictionary of Macular parameters containing the Macular parameters to be changed, together with their new
            values.

        Raises
        ----------
        TypeError
            The type error is raised if the params_dict keys are not str and its values are not integers,
            floats or lists.
        """
        for param in params_dict:
            if type(param) is not str:
                raise TypeError(f"Macular parameters must be str not {type(param)}.")
            if type(params_dict[param]) not in (int, float, list):
                raise TypeError(f"Macular parameter value must be int, float or list not "
                                f"{type(params_dict[param])}")
            self.check_list_length(params_dict[param])

    @staticmethod
    def next_element(param, i_sim):
        """Function used to update the value of a configuration parameter of the simulation batch.

        If this parameter is a list, the element located at index i_sim will be accessed in order to only take the
        element corresponding to the next simulation.

        Parameters
        ----------
        param : str, int, float, list
            Configuration parameter of the simulation batch from which the following element must be accessed.

        i_sim : int
            Number of the next simulation. This number is mainly used to determine the index to access in
            list of parameters varying between each simulation.

        Returns
        ----------
        str, int, float
            The returned param has taken the value of the element of the following simulation.
        """
        if type(param) is list:
            if len(param) == 1:
                param = param[0]
            else:
                param = param[i_sim]

        return param

    def refresh_dict_formatting_alias(self, i_sim):
        """Update of the dictionary containing the aliases of the elements to be modified within the names of paths.

        The update is performed by accessing the aliases present in dict_config. All aliases present directly in
        dict_config are added as is. All aliases present in the Macular parameter dictionary (params_dict) are added
        with the suffixes ‘_value’ and ‘_name’ respectively for the name and value of the parameter. When one of the
        aliases is a list, the element located at index i_sim is accessed.

        Parameters
        ----------
        i_sim : int
            Number of the next simulation. This number is mainly used to determine the index to access in
            list of parameters varying between each simulation.
        """
        # Case of aliases defined at the root of the json.
        for alias in self.dict_config:
            if alias not in ("path_macufile", "path_macudata", "path_macustim", "path_macugraph", "params_dict",
                             "n_sim"):
                self._dict_formatting_alias[alias] = self.next_element(self.dict_config[alias], i_sim)

        # Case of aliases defined in the params_dict of the json.
        try:
            for alias in self.dict_config["params_dict"]:
                self._dict_formatting_alias[f"{alias}_name"] = alias
                self._dict_formatting_alias[f"{alias}_value"] = str(self.next_element(
                    self.dict_config["params_dict"][alias], i_sim)).replace(".", ",")
        except KeyError:
            pass

    def refresh_paths(self, i_sim):
        """Update of attributes containing file paths (path_macufile, path_macudata, path_macustim, path_macugraph).

        The update is performed by accessing the paths present in dict_config. When one of the paths is a list, the
        element located at index i_sim is accessed. All these paths are formatted by the TextFormatting class
        using the alias formatting dictionary (dict_formatting_alias). All the elements in brackets to be replaced are
        substituted by their alias for the current simulation.

        Parameters
        ----------
        i_sim : int
            Number of the next simulation. This number is mainly used to determine the index to access in
            list of parameters varying between each simulation.
        """
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
        """Update of the Macular parameter dictionary ‘params_dict’.

        The update is performed by accessing the keys and values from params_dict present in dict_config.
        When one of the values is a list, the element located at index i_sim is accessed.

        Parameters
        ----------
        i_sim : int
            Number of the next simulation. This number is mainly used to determine the index to access in
            list of parameters varying between each simulation.
        """
        try:
            for param in self.dict_config["params_dict"]:
                self._params_dict[param] = self.next_element(self.dict_config["params_dict"][param], i_sim)
        except KeyError:
            pass

    def load_next_sim(self, i_sim):
        """Update of all the attributes of the launcher with those of the next batch simulation.

        Parameters
        ----------
        i_sim : int
            Number of the next simulation. This number is mainly used to determine the index to access in
            list of parameters varying between each simulation.
        """
        self.refresh_params_dict(i_sim)
        self.refresh_dict_formatting_alias(i_sim)
        self.refresh_paths(i_sim)

    def multiple_runs(self):
        """Function to launch a simulation batch.

        All the attributes of the launcher are updated before each simulation to correspond to what is in the batch
        simulation configuration dictionary.
        """
        for i_sim in range(self.n_sim):
            self.load_next_sim(i_sim)
            self.run()

    def run(self):
        """Function allowing the Macular simulation to be launched from a linux subprocess and with the current
        simulation parameters.
        """
        list_subprocess = self.make_subprocess()
        subprocess.run(list_subprocess)

    def make_subprocess(self):
        """Creation function of the linux subprocess enabling macular-batch to be launched.

        The macular-batch process requires path_macufile (-f) and path_macudata (-o). It can also take a
        path_macustim (-s), path_macugraph (-g) and a params_dict (-p).

        Returns
        ----------
        list of str
            List of the linux subprocess to run macular-batch with the parameters of the current simulation.
        """
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
