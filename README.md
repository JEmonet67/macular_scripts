# macular_scripts

This tool allows you to run Macular simulations in batch mode sequentially. It is based on the macular-batch command and a batch configuration file.

## Prerequisites

Linux.

## Installation

Clone the macular_scripts directory from the GitHub repository (using SSH or HTML).

```bash
git clone git@github.com:JEmonet67/macular_scripts.git (ssh)
```

```bash
git clone https://github.com/JEmonet67/macular_scripts.git (html)
```

Then make the macular-batch and macularscript executable accessible everywhere.



**Case 1 :** 
 
From the root repository of the Macular folder.
```bash
sudo ln -s "$(pwd)/build/bin/macular-batch" /usr/local/bin/nom_utilisateur/macular-batch
```

From the root repository of the Macular Scripts.
```bash
sudo chmod +x "$(pwd)/macuscript.sh"
sudo ln -s "$(pwd)/macuscript.sh" /usr/local/bin/nom_utilisateur/macuscript
```


**Case 2 :** 

If you do not have root access, you will need to use a .local folder in your home directory.

```bash
cd ~
mkdir -p .local/bin
```

Then, from your root repository of Macular.
```
ln -s "$(pwd)/build/bin/macular-batch" ~/.local/bin/macular-batch
```

And, from your root repository of Macular Scripts.
```
ln -s "$(pwd)/macuscript.sh" ~/.local/bin/macuscript
```

Once done, you must open your bashrc (nano ~/.bashrc) to add the new path to your PATH variable: 
```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Usage

### Bash command

```bash
./macuscript.sh ~/Documents/These/MacularFiles/config_file.json
```

Bash command used to launch a batch of simulations from macular_scripts, with all parameters defined in the batch configuration file. The bash script launches the Python script of the same name using the path_config_file provided as input. Macuscript.py creates a MacularScriptLauncher based on the path_config_file and then launches all simulations sequentially. 

### Batch configuration file

The batch configuration files used are defined in JSON format with a specific structure.

The file must contain three mandatory items:

- The number of simulations in the batch (*n_sim*).
- The path where the simulation data will be saved (*path_macudata*).
- The path to the Macular session file(s) in json format (*path_macufile*). 

In addition, there are optional items such as: the path to the stimulus or stimuli (*path_macustim*), the path to the Macular graph(s) (*path_macugraph*) if they are different from those defined in the Macular session file, and the dictionary of Macular parameters to be modified with their values (*params_dict*). This dictionary associates the names of the parameters as they appear in the Macular session files with their new values. In all cases, it is possible to give a single value that will apply to all simulations or, conversely, to give a list of values equal to n_sim so that there is a different value for each simulation. If no path to a specific stimulus or graph is defined, the one defined in the Macular session file will be applied by default.

Finally, you can add as many additional items as you want to the batch configuration file, which will be saved and used as aliases for formatting the batch configuration file. These items associate the alias name with what to substitute it with.

### Formatting the batch configuration file

The batch configuration file used in macular_scripts includes the feature of formatting all items in the file that define a path to a file (path_macudata, path_macufile, path_macugraph, and path_macustim). This process has several uses. The first is to facilitate the initialization of multiple similar file paths while limiting repeated terms. The second is to enable the definition of file names based on the same model but varying only in a few sub-parts of their character string. This makes it possible to modify only the value of the condition that is varied in an experiment (e.g., path_barSpeed30dps, path_barSpeed25dps). This approach also makes it easier to identify the elements of interest that vary between each simulation and to modify them more easily.

The batch configuration file is formatted using aliases enclosed in braces, which are placed within the character strings of the file paths. The alias values are initialized for any term defined in the batch configuration file that does not correspond to an expected attribute (path_macufile, n_sim, etc.). When certain Macular parameters are modified in the parameter dictionary (params_dict), the names and values of these parameters are also automatically included in the aliases with a suffix “_name” and ‘_value’ (e.g., “virtual_retina/relative_ampOPL_value” or “virtual_retina/relative_ampOPL_name”). During formatting, aliases in braces are replaced by the value to which they are associated. The value can be unique and apply to all simulations, or a list to apply a different value to each simulation in the batch.

### Example of batch configuration files

Three examples are included in the “resources” directory. 

The batch configuration file “config_macuscript_default.json” performs 10 simulations with the same stimulus (video_whitebar_D187_motion30.mp4) and the same Macular session file (simple_simulation_macular.json). Each simulation differs from the previous one by a modification of the relative_ampOPL parameter of virtual_retina using “params_dict”. This difference is used to vary the name of the output file between each simulation: “RC_RM_dSGpCP0012_ampGang{value_caract_sim}Hz_0f.csv” with value_caract_sim taking a value from 1 to 50 in increments of 5. The output name is formatted to include the simulation identification number, the name of the modified characteristic, its unit, and its value. 

The batch configuration file “config_macuscript_default_test_ampGang.json” is identical to “config_macuscript_default.json” except that it uses one additional alias to define the directory path leading to the Macular simulation file, the output, and the stimulus. 

The batch configuration file “config_macuscript_default_test_barSpeed.json” performs 10 simulations  with the same Macular session (simple_simulation_macular.json). Each simulation differs from the previous one by a modification of the stimulus used so that the speed of the bar changes. This is visible by a path_macustim equal to a list of 10 stimuli, one for each simulation in the batch. The value of the bar speed is defined within the list stored in “value_caract_sim”. The name of the modified characteristic is therefore barSpeed and its unit is dps (°/s). Finally, the identification number also changes here between each simulation, as shown by “id_sim” corresponding to a list of 10 elements. These differences are used to vary the name of the output file between each simulation by formatting it as follows: “RC_RM_dSGpCP{id_sim}barSpeed{value_caract_sim}dps\_0f.csv”.

## Modules

### MacularScriptLauncher Module

Module implementing the MacularScriptLauncher class, whose objects are constructed using the MacularScriptLauncher(path_config_file) constructor, which takes as input the path to the batch configuration file in JSON format. The constructor initializes the dict_config, reg_ext_file, and n_sim attributes with the values found in the file. The other attributes are initialized but empty.

Each MacularScriptLauncher consists of several attributes:

- **dict_config** contains the complete dictionary that has been defined in the batch configuration file. This dictionary must contain at least three mandatory parameters (n_sim, path_macudata, and path_macufile).
- **n_sim** is the number of simulations to be performed in the batch.
- **path_macufile** is the path to one or more session file for a Macular simulation. It is used to define all the default parameters for Macular simulations. You can provide a single file or one for each simulation in the batch.
- **path_macudata** is the path where the simulation data will be saved during the batch. You can provide a single file or one for each simulation in the batch.
- **path_macustim** is the path to the stimulus or stimuli to be used in the batch simulations. You can provide a single one or one for each simulation in the batch.
- **path_macugraph** is the path to the graph file in .mac format created by Macular and used in the batch simulations. You can provide a single path or one for each simulation in the batch. If no graph file is provided, the one defined in the Macular initialization file will be used.ù
- **dict_formatting_alias** is a dictionary containing all the aliases to be replaced in the batch configuration file, along with the value with which they are to be replaced. This can be an integer, a character string, or a list of one of these two types if you want the alias to apply differently to each simulation in the batch. All items in the batch configuration file that do not correspond to an attribute are added as aliases in this dictionary. All names and values of modified Macular parameters are also added to params_dict, but they are distinguished by a suffix “\_name” or “\_value” (e.g., “virtual_retina/relative_ampOPL_value” or “virtual_retina/relative_ampOPL_name”).
- **params_dict** corresponds to the set of Macular parameters that we want to vary between batch simulations. This attribute comes from the key of the same name defined in the batch configuration file. It contains a set of keys corresponding to the names of the parameters to be changed. The keys are associated either with a value to be applied to the entire batch or with a list of values to vary the parameter between each simulation in the batch.
- **reg_ext_file** corresponds to the regular expression used to identify the name of a file within a path to the file. 

The MacularScriptLauncher module consists of the functions detailed below.

**dict_config(dict_config):** Setter for the dict_config attribute that checks for the presence of mandatory parameters, initializes n_sim, and resets all other attributes of MacularScriptLauncher.  It also checks and adds dict_config.

**read_config_file(path_config_file):** Method for reading the contents of a batch configuration file.

**check_list_length(list_params):** Method that checks that the size of the list of values associated with an item in the batch configuration file corresponds to the number of simulations in the batch (n_sim). If not, it returns an error.

**check_config_dict(dict_config):** Method that checks the structure of the dictionary obtained from a batch configuration file. It checks for the presence of mandatory keys and also checks the syntax of optional keys. 

**check_formatting_alias(dict_config):** Method that checks that the names of the aliases chosen do not correspond to any of the reserved terms (path_macufile, path_macudata, path_macustim, path_macugraph, params_dict) and that the values are integers, character strings, or lists. If not, an error is returned.

**check_path_existing(path):** Method that checks whether a path exists within the file tree. If not, returns an error.

**path_file_to_path_dir(path):** Method for extracting paths to the directory containing the file. 

**create_non_existing_path(path):** Method for creating a path that does not already exist.

**check_path_type(paths):** Method for checking that a path (string or list) is correctly typed. Otherwise, returns an error.

**check_dict_type(dictionary):** Method for checking that a dictionary is correctly typed. Otherwise, returns an error.

**check_mandatory_params(dict_config):** Method for checking the presence of the three mandatory parameters (n_sim, path_macufile, and path_macudata) in a configuration dictionary. Otherwise, returns an error.

**check_params_dict(params_dict):** Method for checking a parameter dictionary; the key type must be a string and its value a string or a list of strings, integers, or floats. Otherwise, returns an error.

**next_element(param, i_sim):** Method for retrieving the value of a list of parameter values corresponding to a given index. It is used to update the value of this parameter in the current simulation.

**refresh_dict_formatting_alias(i_sim):** Method for updating the alias dictionary that associates alias names with the values they are associated with in the next simulation. The function is called between each simulation to update and take into account the parameters associated with a list of values. 

**refresh_paths(i_sim):** Method for updating the paths to the files in order to prepare for the next simulation. The function is called between each simulation to update and take into account the parameters associated with a list of values. If there are aliases in the paths, this is when they are substituted. 

**refresh_params_dict(i_sim):** Method for updating the parameter dictionary that associates the names of the parameters with the values they are associated with in the next simulation. The function is called between each simulation to update and take into account the parameters associated with a list of values. 

**load_next_sim(i_sim):** Method that updates all the attributes of the MacularScriptLauncher to retrieve the values corresponding to the next simulation. The next value of all parameters associated with a list of values for the simulation batch is retrieved. First, the parameter dictionary is refreshed, then the alias dictionary that depends on it, and finally the paths that also depend on the aliases are updated.

**multiple_runs():** Method for launching all simulations in a batch. Before each one, the attributes of MacularScriptLauncher are updated.

**run():** Method for launching a simulation from the command line.

**make_subprocess():** Method for creating the command line to be used to launch the simulation in bash.

### TextFormatting Module

Module implementing the TextFormatting class, whose objects are constructed using the TextFormatting(str_to_form, formatting_dict={}) constructor, which takes as input the text to be formatted, containing aliases in braces, and the braces dictionary associating aliases with their replacement text. The constructor simply initializes all attributes. 

Each TextFormatting consists of three attributes:

- **str_to_form** contains the character string to be formatted by substituting the aliases in braces that it contains.
- **formatting_dict** contains the dictionary associating each alias with the character string with which it should be substituted.
- **formatting_reg** contains a compiled regular expression pattern used to extract all sub-strings corresponding to the aliases in braces.

The TextFormatting module consists of the functions detailed below.

**str_to_form(text):** Setter for the str_to_form attribute, which checks that the text to be formatted is indeed a character string; otherwise, an error is returned.

**formatting_dict(dictionary):** Setter for the formatting_dict attribute, which checks that the value applied to it is indeed a dictionary; otherwise, an error is returned.

**to_str():** Method for formatting the text contained in the str_to_form attribute of TextFormatting. The aliases to be substituted are identified from the formatting_reg attribute. The formatting_dict dictionary is used to determine the text to be used in the substitution. If the text contains an alias that is not defined in formatting_dict, an error is returned.

**\__repr__:** Display method using the to_str() method to display the formatted text contained in the str_to_form attribute of the TextFormatting object.

## License

MIT License

## Technologies

Python.

## Contribution

This MacularScript script was created entirely by Jérôme EMONET as part of his thesis to facilitate successive simulations with the Macular software, to which he also contributed. Macular has also been the subject of a publication.

Macular gitlab : https://gitlab.inria.fr/macular/macular

Thesis reference : A retino-cortical model to study movement-generated waves in the visual system (https://hal.science/tel-04827484v2)

Macular article reference : Macular: a multi-scale simulation platform for the retina and the primary visual system (https://inria.hal.science/hal-05312447v2).







