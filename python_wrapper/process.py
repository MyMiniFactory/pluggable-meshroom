import argparse
import json
import os
import time

import directions
import node
import pipeline_structure
import setups
import utils


def process(binary_folder_direction, input_folder_direction, output_folder_direction,
            quality_choice, output_type_choice, nb_of_images, **kwargs):
    """ Entry point of the wrapper. Runs the process.

    Arguments
    ----------
    - binary_folder_direction: path to the folder that contains Meshroom binary files
    - input_folder_direction: path to the folder which contains the input images
    - output_folder_direction: path to the folder where the output will be stacked (must exist)
    - quality_choice: quality desired. Must be one of DRAFT, MEDIUM, HIGH
    - output_type_choice: type of output desired. Must be one of POINT_CLOUD, MESH, FILTERED_MESH, TEXTURED_MESH
    - nb_of_images: number of input images
    - kwargs:
        + path_to_results_json_file: path to the results.json file (optional)
        + path_to_metadata_json_file_directory: path to the folder where the metadata.json file will be written (optional)
        + path_to_status_json_file_directory: path to the folder where the status.json file will be written
    """
    # Set setups
    set_setups = setups.Setups(
        quality_choice,
        output_type_choice,
        nb_of_images
        )
    # Set directions
    set_directions = directions.Directions(
        binary_folder_direction,
        input_folder_direction,
        output_folder_direction,
        utils.concat_and_normalize_paths(output_folder_direction, 'log'),
        results_dir=kwargs["path_to_results_json_file"],
        metadata_dir=kwargs["path_to_metadata_json_file_directory"],
        status_dir=kwargs["path_to_status_json_file_directory"]
        )
    # Set pipeline structure
    structure = pipeline_structure.get_the_pipeline_structure(
        set_setups.quality,
        set_setups.output_type
        )

    # Create the log folder to stack the log files
    utils.create_folder(set_directions.log_dir)

    # Initialise the status.json file
    status_dict = {}
    utils.update_json_file(set_directions.status_file, status_dict)

    # Initialize the metadata.json file
    metadata_dict = {
        "global_report": {},
        "step_by_step_report": {}
        }
    utils.update_json_file(set_directions.metadata_file, metadata_dict)

    # Build the pipeline
    pipeline = build_the_pipeline(set_setups, set_directions, structure, status_dict)

    # Run the process
    global_starting_time = time.time()
    for node in pipeline:
        # Run the step
        step_starting_time = time.time()
        node.run_the_node(set_directions.status_file, status_dict)
        step_ending_time = time.time()
        # Stack metadata
        report = node.report()
        metadata_dict["step_by_step_report"][node.name] = {
            "time_taken": step_ending_time - step_starting_time,
            "report": report
            }
        utils.update_json_file(set_directions.metadata_file, metadata_dict)
    global_ending_time = time.time()
    metadata_dict["global_report"]["time_taken"] = global_ending_time - global_starting_time
    utils.update_json_file(set_directions.metadata_file, metadata_dict)

    # Renaming and moving files to fit the given results.json file
    try:
        metadata_dict["global_report"]["results.json_file"] = True
        metadata_dict["global_report"]["output_file_report"] = utils.fitting_the_json_results_file(set_directions)
    except:
        metadata_dict["global_report"]["results.json_file"] = False
        metadata_dict["global_report"]["output_file_report"] = utils.output_file_report(set_directions.get_the_process_directions())

    utils.update_json_file(set_directions.metadata_file, metadata_dict)

    return 0


def build_the_pipeline(setups, directions, structure, status_dict):
    """ Build the pipeline to run as a list of nodes.

    Arguments
    ----------
    - setups: an instance of the class Setups
    - directions: an instance of the class Directions
    - structure: one pipeline structure. Format:
        {
            step_number: step_name;
            ...
        }

    Returns
    ----------
    A list of nodes (instances of the class Node)
    """
    nodes_list = []
    for step_number in range(1, len(structure)+1):
        step_name = structure[step_number]
        node_to_add = node.Node(step_name, directions.get_the_process_directions(),
                                directions.log_dir, setups)
        nodes_list.append(node_to_add)
    return (nodes_list)


parser = argparse.ArgumentParser(description='Launch alicevision pipeline.')
parser.add_argument('--bin', metavar='FOLDER', type=str, required=True,
                    help='Folder which contains Meshroom executable files.')
parser.add_argument('--input', metavar='FOLDER', type=str, required=True,
                    help='Input folder.')
parser.add_argument('--output', metavar='FOLDER', type=str, required=True,
                    help='Output folder.')
parser.add_argument('--quality', type=str, required=True,
                    help='Quality desired. Possible values: DRAFT, MEDIUM, HIGH.')
parser.add_argument('--outputType', type=str, required=True,
                    help='Output desired. Possible values: POINT_CLOUD, MESH, FILTERED_MESH, TEXTURED_MESH.')
parser.add_argument('--nbOfImages', type=int, required=True, help='Number of input pictures.')
parser.add_argument('--results', metavar='JSON FILE', type=str, required=False,
                    help='results.json file address if given.')
parser.add_argument('--metadata', metavar='FOLDER', type=str, required=False,
                    help='Folder where to write the metadata.json file if wanted. Gives a live report of the running process.')
parser.add_argument('--status', metavar='FOLDER', type=str, required=True,
                    help='Folder where to write the status.json file. It gives a live report of the process flow')

args = parser.parse_args()

process(args.bin, args.input, args.output, args.quality, args.outputType, args.nbOfImages,
        path_to_results_json_file=args.results, path_to_metadata_json_file_directory=args.metadata,
        path_to_status_json_file_directory=args.status)
