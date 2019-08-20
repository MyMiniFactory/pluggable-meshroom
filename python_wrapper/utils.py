import json
import os
import shutil


def create_folder(direction):
    """ Creates a folder at the given direction if it does not already exist.
    """
    try:
        os.mkdir(direction)
    except:
        pass
    return 0


def concat_and_normalize_paths(path, *paths):
    """ Join the paths and convert the result to normalize it for the OS used.
    """
    return (os.path.normpath(os.path.join(path, *paths)))


def get_file_direction(file_direction_to_test):
    """ Returns the file direction given in input if it exists. None otherwise.
    """
    if (os.path.isfile(file_direction_to_test)):
        return (file_direction_to_test)
    else:
        return


def fitting_the_json_results_file(directions):
    """ Rename and move the output files to fit the results.json file.
    """
    # Converting the results.json file for python
    with open(directions.results_file, 'r') as results:
        converted_results = json.load(results)

    # Dictionary containing the old locations for the output files if they exist
    process_directions = directions.get_the_process_directions()
    old_dirs_tab = {
        "POINT_CLOUD": get_file_direction(concat_and_normalize_paths(process_directions["structure_from_motion"]["intern_locations"]["extraInfoFolder"], 'cloud_and_poses.ply')),
        "MESH": get_file_direction(process_directions["meshing"]["intern_locations"]["output"]),
        "FILTERED_MESH": get_file_direction(process_directions["mesh_filtering"]["intern_locations"]["output"]),
        "TEXTURED_MESH": get_file_direction(concat_and_normalize_paths(process_directions["texturing"]["intern_locations"]["output"], 'texturedMesh.obj')),
        "TEXTURE_PNG": get_file_direction(concat_and_normalize_paths(process_directions["texturing"]["intern_locations"]["output"], 'texture_0.png')),
        "TEXTURE_MTL": get_file_direction(concat_and_normalize_paths(process_directions["texturing"]["intern_locations"]["output"], 'texturedMesh.mtl'))
        }

    moving_files_report = {}
    # Moving and renaming the files
    for key in converted_results:
        old_dir = old_dirs_tab[key]
        moving_files_report[key] = {}
        moving_files_report[key]["exists"] = True if (old_dir is not None) else False
        moving_files_report[key]["current_dir"] = old_dir

        new_dir = concat_and_normalize_paths(directions.output_dir, '..', converted_results[key]["location"], converted_results[key]["name"])
        try:
            shutil.copyfile(old_dir, new_dir)
            moving_files_report[key]["moving_success"] = True
            moving_files_report[key]["new_dir"] = new_dir
        except:
            moving_files_report[key]["moving_success"] = False
            moving_files_report[key]["new_dir"] = None
    return (moving_files_report)


def output_file_report(process_directions):
    """ Returns a report on the output files (existence and location)

    Arguments
    ----------
    - process_directions: the directions used to run the node. Format is the following:
        {
            "binary_direction": ...,
            "output_folder": path_to_the_folder_where_the_output_is_stacked,
            "intern_locations": {
                "direction_token": "path"
            }

    Returns
    ----------
    A dictionary. Format:
    {
        output_file: {
            success: True if exists, False otherwise,
            location: path to the file if it exists, None otherwise
        },
        ...
    }
    """
    # Dictionary containing the locations for the output files if they exist
    dirs_tab = {
        "POINT_CLOUD": get_file_direction(concat_and_normalize_paths(process_directions["structure_from_motion"]["intern_locations"]["extraInfoFolder"], 'cloud_and_poses.ply')),
        "MESH": get_file_direction(process_directions["meshing"]["intern_locations"]["output"]),
        "FILTERED_MESH": get_file_direction(process_directions["mesh_filtering"]["intern_locations"]["output"]),
        "TEXTURED_MESH": get_file_direction(concat_and_normalize_paths(process_directions["texturing"]["intern_locations"]["output"], 'texturedMesh.obj')),
        "TEXTURE_PNG": get_file_direction(concat_and_normalize_paths(process_directions["texturing"]["intern_locations"]["output"], 'texture_0.png')),
        "TEXTURE_MTL": get_file_direction(concat_and_normalize_paths(process_directions["texturing"]["intern_locations"]["output"], 'texturedMesh.mtl'))
        }
    output_file_report = {}
    for key in dirs_tab:
        output_file_report[key] = {
            "success": True if (dirs_tab[key] is not None) else False,
            "location": dirs_tab[key]
        }
    return (output_file_report)


def update_json_file(file, dictionary):
    """ Updates the .json file if it exists.

    Arguments
    ----------
    - file: path to the file to update
    - dictionary: a python dictionary representig the json file to update
    """
    try:
        with open(file, 'w') as file:
            json.dump(dictionary, file)
    except:
        print ("No such .json file.")
