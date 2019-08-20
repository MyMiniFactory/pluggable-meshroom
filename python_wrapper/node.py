import os
import subprocess

import parameters
import utils


class Node():
    """ An instance of the class Node represents a node to be run.

    Building arguments
    ----------
    - step_name: the name of the step. Must be one of:
        + camera_init
        + feature_extraction
        + image_matching
        + feature_matching
        + structure_from_motion
        + prepare_dense_scene
        + camera_connection
        + depth_map
        + depth_map_filter
        + meshing
        + mesh_filtering
        + texturing
    - process_directions: the directions needed to run the node. Format is the following:
        {
            "binary_direction": ...,
            "output_folder": path_to_the_folder_where_the_output_is_stacked,
            "intern_locations": {
                "direction_token": "path"
            }
        For more details, see the class Directions in directions.py
    - log_dir: location of the folder where log files are written for each step
    - setups: a instance of the class Setups

    Attributes
    ----------
    - name: name of the step
    - binary_name: path to the binary which is run
    - output_folder: path to the folder where the output is stacked
    - intern_locations: dictonary of the directions used to run the step
    - parameters: set of parameters use to run the step
    - nb_of_images: number of pictures
    - log_dir: location of the folder where log files are written for each step
    - status_dir: direction to the folder where to write the status.json file
    """

    def __init__(self, step_name, process_directions, log_dir, setups):
        self.name = step_name
        self.binary_name = process_directions[step_name]["binary_direction"]
        self.output_folder = process_directions[step_name]["output_folder"]
        self.intern_locations = process_directions[step_name]["intern_locations"]
        self.parameters = parameters.get_the_parameters(setups.quality, setups.nb_of_images)[step_name]
        self.nb_of_images = setups.nb_of_images
        self.log_dir = utils.concat_and_normalize_paths(log_dir, step_name + '_log.txt')

    def run_the_node(self, status_file, status_dict):
        """ Run the step represented by the node and updates the status.json file which gives a live output of the running process.
        """

        utils.create_folder(self.output_folder)

        status_dict[self.name] = {}
        status_dict[self.name]["status"] = "in progress"
        status_dict[self.name]["progress"] = 0
        utils.update_json_file(status_file, status_dict)

        cmd_line = []
        cmd_line.append(self.binary_name)
        for option, value in self.add_locations_to_command_line():
            cmd_line.append(option)
            cmd_line.append(value)
        for option, value in self.add_parameters_to_command_line():
            cmd_line.append(option)
            cmd_line.append(value)

        log = open(self.log_dir, 'w')
        # Dealing with DepthMap particular case
        if (self.name == "depth_map"):
            # Dividing the task if needed
            group_size = self.parameters["groupSize"]
            number_of_groups = (self.nb_of_images + (group_size-1)) // group_size
            for group_iter in range(number_of_groups):
                range_start = group_size * group_iter
                range_size = min(group_size, self.nb_of_images-range_start)
                print("DepthMap Group {}/{} : {}, {}".format(group_iter+1, number_of_groups, range_start, range_size))
                cmd = cmd_line + ['--rangeStart', str(range_start), '--rangeSize', str(range_size)]
                print (cmd)
                subprocess.run(cmd, stderr=log)
                status_dict[self.name]["progress"] = ((group_iter+1)/number_of_groups)*100
                print (status_dict)
                utils.update_json_file(status_file, status_dict)
        else:
            print (cmd_line)
            subprocess.run(cmd_line, stderr=log)
            status_dict[self.name]["progress"] = 100
            utils.update_json_file(status_file, status_dict)

        log.close()

        status_dict[self.name]["status"] = "done"
        status_dict[self.name]["progress"] = 100
        utils.update_json_file(status_file, status_dict)

        return 0

    def add_parameters_to_command_line(self):
        """ Build the parameter part of the command line for a given parameters dictionary.
        Ignore the parameter called "groupSize" in order to deal with the DepthMap particular case.
        """
        parameters_cmd_line = []
        for key in self.parameters:
            if (key == "groupSize"):        # DepthMap particular case
                continue
            else:
                parameters_cmd_line.append(('--'+key, self.parameters[key]))

        return (parameters_cmd_line)

    def add_locations_to_command_line(self):
        """ Build the intern_locations part of the command line for a given intern_locations dictionary.
        """
        locations_cmd_line = []
        for key in self.intern_locations:
            locations_cmd_line.append(('--'+key, self.intern_locations[key]))
        return (locations_cmd_line)

    def report(self):
        """ Returns a full report on the run node.
        """
        step_sucess, locations_report = self.check_locations_existence_and_step_success()
        log_report = self.log_report()
        report = {
            "success": step_sucess,
            "log_report": log_report,
            "locations_report": locations_report
        }
        return (report)

    def log_report(self):
        """ Return a dictionary containing a report on the log file of the step.
        """
        # check log.txt file existence and open it if possible
        log_report = {}
        log_file_existence_key = "log_file"
        try:
            log_file = open(self.log_dir, "r")
            log_report[log_file_existence_key] = True
        except:
            log_report[log_file_existence_key] = False
            return (log_report)
        # Catch informations
        warning_list = []
        error_list = []
        fatal_list = []
        # debug_list = []
        for line in log_file:
            if ("[warning]" in line):
                warning_list.append(line)
            if ("[error]" in line):
                error_list.append(line)
            if ("[fatal]" in line):
                fatal_list.append(line)
            # if ("[debug]" in line):
                # debug_list.append(line)
        log_file.close()
        # Stack information in the log_report
        log_report["warning"] = warning_list
        log_report["error"] = error_list
        log_report["fatal"] = fatal_list
        # log_report["debug"] = debug_list

        return (log_report)

    def check_locations_existence_and_step_success(self):
        """ Return a dictionary containing a report on the existence of the input and output files of the step.
        Deal with the camera_connection particular case which writes .bin files in the prepare_dense_scene folder.
        """
        step_success = True
        locations_to_check = self.intern_locations
        locations_existence_report = {}
        for key in locations_to_check:
            if (os.path.isfile(locations_to_check[key])):
                locations_existence_report[locations_to_check[key]] = "Found"
            elif (os.path.isdir(locations_to_check[key])):
                for root, dirs, files in os.walk(locations_to_check[key]):
                    if (len(files) == 0):
                        locations_existence_report[locations_to_check[key]] = "Empty"
                        step_success = False
                    else:
                        locations_existence_report[locations_to_check[key]] = "Not empty"
            else:
                locations_existence_report[locations_to_check[key]] = "No such path"
                step_success = False
        # camera_connecion particular case
        if (self.name == 'camera_connection'):
            bin_files_existence_key = ".bin_files"
            bin_files_existence = False
            folder = os.path.split(self.intern_locations["ini"])[0]
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path, extension = os.path.splitext(file)
                    if (extension == '.bin'):
                        bin_files_existence = True
            if (bin_files_existence):
                locations_existence_report[bin_files_existence_key] = ".bin files found"
            else:
                locations_existence_report[bin_files_existence_key] = "No .bin files"
                step_success = False
        return (step_success, locations_existence_report)
