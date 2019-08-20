import utils


class Directions():

    """ An instance of the class Directions represents the directions needed to run the process.

    Building arguments
    ----------
    - bin_dir: direction to Meshroom executable files folder
    - input_dir: direction to the input images folder
    - output_dir: direction where the output is saved
    - log_dir: location of the folder where log files are written for each step
    - kwargs:
        + results_dir: results.json file address
        + metadata_dir: direction to the folder where to write the metadata.json file
        + status_dir: direction to the folder where to write the status.json file

    Attributes
    ----------
    - bin_dir: direction to Meshroom executable files folder
    - input_dir: direction to the input images folder
    - output_dir: direction where the output is saved
    - log_dir: location of the folder where log files are written for each step
    - results_file: results.json file address (optionnal)
    - metadata_file: path to the metadata.json file (optionnal)
    - status_file: path to the status.json file
    """

    def __init__(self, bin_dir, input_dir, output_dir, log_dir, **kwargs):
        self.bin_dir = bin_dir                          # binary folder address
        self.input_dir = input_dir                      # input folder address
        self.output_dir = output_dir                    # output folder address
        self.log_dir = log_dir                          # log file folder address
        self.results_file = kwargs["results_dir"]        # results.json file address
        self.metadata_file = utils.concat_and_normalize_paths(kwargs["metadata_dir"], 'metadata.json')      # metadata.json file address
        self.status_file = utils.concat_and_normalize_paths(kwargs["status_dir"], 'status.json')            # status.json file address

    def get_the_process_directions(self):
        """ Returns the directions used to run each step of the process.
        """
        camera_init_direction_set = {
            "binary_direction": utils.concat_and_normalize_paths(self.bin_dir, 'aliceVision_cameraInit'),
            "output_folder": utils.concat_and_normalize_paths(self.output_dir, 'carame_init'),
            "intern_locations": {
                "imageFolder": self.input_dir,
                "output": utils.concat_and_normalize_paths(self.output_dir, 'carame_init', 'camera.sfm')
            }
        }
        feature_extraction_direction_set = {
            "binary_direction": utils.concat_and_normalize_paths(self.bin_dir, 'aliceVision_featureExtraction'),
            "output_folder": utils.concat_and_normalize_paths(self.output_dir, 'feature_extraction'),
            "intern_locations": {
                "input": camera_init_direction_set["intern_locations"]["output"],
                "output": utils.concat_and_normalize_paths(self.output_dir, 'feature_extraction')
            }
        }
        image_matching_direction_set = {
            "binary_direction": utils.concat_and_normalize_paths(self.bin_dir, 'aliceVision_imageMatching'),
            "output_folder": utils.concat_and_normalize_paths(self.output_dir, 'image_matching'),
            "intern_locations": {
                "input": camera_init_direction_set["intern_locations"]["output"],
                "featuresFolder": feature_extraction_direction_set["intern_locations"]["output"],
                "output": utils.concat_and_normalize_paths(self.output_dir, 'image_matching', 'image_matches.txt')
            }
        }
        feature_matching_direction_set = {
            "binary_direction": utils.concat_and_normalize_paths(self.bin_dir, 'aliceVision_featureMatching'),
            "output_folder": utils.concat_and_normalize_paths(self.output_dir, 'feature_matching'),
            "intern_locations": {
                "input": camera_init_direction_set["intern_locations"]["output"],
                "featuresFolders": feature_extraction_direction_set["intern_locations"]["output"],
                "imagePairsList": image_matching_direction_set["intern_locations"]["output"],
                "output": utils.concat_and_normalize_paths(self.output_dir, 'feature_matching')
            }
        }
        structure_from_motion_direction_set = {
            "binary_direction": utils.concat_and_normalize_paths(self.bin_dir, 'aliceVision_incrementalSfM'),
            "output_folder": utils.concat_and_normalize_paths(self.output_dir, 'structure_from_motion'),
            "intern_locations": {
                "input": camera_init_direction_set["intern_locations"]["output"],
                "featuresFolders": feature_extraction_direction_set["intern_locations"]["output"],
                "matchesFolders": feature_matching_direction_set["intern_locations"]["output"],
                "outputViewsAndPoses": utils.concat_and_normalize_paths(self.output_dir, 'structure_from_motion', 'cameras.sfm'),
                "extraInfoFolder": utils.concat_and_normalize_paths(self.output_dir, 'structure_from_motion', 'extra_info'),
                "output": utils.concat_and_normalize_paths(self.output_dir, 'structure_from_motion', 'bundle.sfm')
            }
        }
        prepare_dense_scene_direction_set = {
            "binary_direction": utils.concat_and_normalize_paths(self.bin_dir, 'aliceVision_prepareDenseScene'),
            "output_folder": utils.concat_and_normalize_paths(self.output_dir, 'prepare_dense_scene'),
            "intern_locations": {
                "input": structure_from_motion_direction_set["intern_locations"]["output"],
                "output": utils.concat_and_normalize_paths(self.output_dir, 'prepare_dense_scene')
            }
        }
        camera_connection_direction_set = {
            "binary_direction": utils.concat_and_normalize_paths(self.bin_dir, 'aliceVision_cameraConnection'),
            "output_folder": utils.concat_and_normalize_paths(self.output_dir, 'camera_connection'),
            "intern_locations": {
                "ini": utils.concat_and_normalize_paths(prepare_dense_scene_direction_set["intern_locations"]["output"], 'mvs.ini')
            }
        }
        depth_map_direction_set = {
            "binary_direction": utils.concat_and_normalize_paths(self.bin_dir, 'aliceVision_depthMapEstimation'),
            "output_folder": utils.concat_and_normalize_paths(self.output_dir, 'depth_map'),
            "intern_locations": {
                "ini": utils.concat_and_normalize_paths(prepare_dense_scene_direction_set["intern_locations"]["output"], 'mvs.ini'),
                "output": utils.concat_and_normalize_paths(self.output_dir, 'depth_map')
            }
        }
        depth_map_filter_direction_set = {
            "binary_direction": utils.concat_and_normalize_paths(self.bin_dir, 'aliceVision_depthMapFiltering'),
            "output_folder": utils.concat_and_normalize_paths(self.output_dir, 'depth_map_filter'),
            "intern_locations": {
                "ini": utils.concat_and_normalize_paths(prepare_dense_scene_direction_set["intern_locations"]["output"], 'mvs.ini'),
                "depthMapFolder": depth_map_direction_set["intern_locations"]["output"],
                "output": utils.concat_and_normalize_paths(self.output_dir, 'depth_map_filter')
            }
        }
        meshing_direction_set = {
            "binary_direction": utils.concat_and_normalize_paths(self.bin_dir, 'aliceVision_meshing'),
            "output_folder": utils.concat_and_normalize_paths(self.output_dir, 'meshing'),
            "intern_locations": {
                "ini": utils.concat_and_normalize_paths(prepare_dense_scene_direction_set["intern_locations"]["output"], 'mvs.ini'),
                "depthMapFolder": depth_map_direction_set["intern_locations"]["output"],
                "depthMapFilterFolder": depth_map_filter_direction_set["intern_locations"]["output"],
                "output": utils.concat_and_normalize_paths(self.output_dir, 'meshing', 'mesh.obj')
            }
        }
        mesh_filtering_direction_set = {
            "binary_direction": utils.concat_and_normalize_paths(self.bin_dir, 'aliceVision_meshFiltering'),
            "output_folder": utils.concat_and_normalize_paths(self.output_dir, 'mesh_filtering'),
            "intern_locations": {
                "input": meshing_direction_set["intern_locations"]["output"],
                "output": utils.concat_and_normalize_paths(self.output_dir, 'mesh_filtering', 'filtered_mesh.obj')
            }
        }
        texturing_direction_set = {
            "binary_direction": utils.concat_and_normalize_paths(self.bin_dir, 'aliceVision_texturing'),
            "output_folder": utils.concat_and_normalize_paths(self.output_dir, 'texturing'),
            "intern_locations": {
                "ini": utils.concat_and_normalize_paths(prepare_dense_scene_direction_set["intern_locations"]["output"], 'mvs.ini'),
                "inputMesh": mesh_filtering_direction_set["intern_locations"]["output"],
                "inputDenseReconstruction": utils.concat_and_normalize_paths(meshing_direction_set["output_folder"], 'denseReconstruction.bin'),
                "output": utils.concat_and_normalize_paths(self.output_dir, 'texturing')
            }
        }

        process_directions = {
            "camera_init": camera_init_direction_set,
            "feature_extraction": feature_extraction_direction_set,
            "image_matching": image_matching_direction_set,
            "feature_matching": feature_matching_direction_set,
            "structure_from_motion": structure_from_motion_direction_set,
            "prepare_dense_scene": prepare_dense_scene_direction_set,
            "camera_connection": camera_connection_direction_set,
            "depth_map": depth_map_direction_set,
            "depth_map_filter": depth_map_filter_direction_set,
            "meshing": meshing_direction_set,
            "mesh_filtering": mesh_filtering_direction_set,
            "texturing": texturing_direction_set
        }

        return (process_directions)
