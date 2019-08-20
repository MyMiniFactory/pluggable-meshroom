""" Structure of the pipeline that is run on the images.

Values
----------
For now, the pipelines listed only depend on the output_type_choice:
    - POINT_CLOUD
    - MESH
    - FILTERED_MESH
    - TEXTURED_MESH

As long as Meshroom is built on several independant nodes, here can be built several pipeline structures
depending on the quality and the type of results desired.
"""

POINT_CLOUD = {
    1: "camera_init",
    2: "feature_extraction",
    3: "image_matching",
    4: "feature_matching",
    5: "structure_from_motion"
}

MESH = {
    1: "camera_init",
    2: "feature_extraction",
    3: "image_matching",
    4: "feature_matching",
    5: "structure_from_motion",
    6: "prepare_dense_scene",
    7: "camera_connection",
    8: "depth_map",
    9: "depth_map_filter",
    10: "meshing"
}

FILTERED_MESH = {
    1: "camera_init",
    2: "feature_extraction",
    3: "image_matching",
    4: "feature_matching",
    5: "structure_from_motion",
    6: "prepare_dense_scene",
    7: "camera_connection",
    8: "depth_map",
    9: "depth_map_filter",
    10: "meshing",
    11: "mesh_filtering"
}

TEXTURED_MESH = {
    1: "camera_init",
    2: "feature_extraction",
    3: "image_matching",
    4: "feature_matching",
    5: "structure_from_motion",
    6: "prepare_dense_scene",
    7: "camera_connection",
    8: "depth_map",
    9: "depth_map_filter",
    10: "meshing",
    11: "mesh_filtering",
    12: "texturing"
}


def get_the_pipeline_structure(quality, output_type):
    """ Returns the pipeline structure to be run.

    Arguments
    ----------
    - quality: quality desired. Must be one of DRAFT, MEDIUM, HIGH
    - output_type: output desired. Must be one of POINT_CLOUD, MESH, FILTERED_MESH, TEXTURED_MESH

    Returns
    ----------
    A pipeline structure.
    """

    pipeline_structure_dict = {
        "DRAFT": {
            (output_type == 'POINT_CLOUD'): POINT_CLOUD,
            (output_type == 'MESH'): MESH,
            (output_type == 'FILTERED_MESH'): FILTERED_MESH,
            (output_type == 'TEXTURED_MESH'): TEXTURED_MESH
            },
        "MEDIUM": {
            (output_type == 'POINT_CLOUD'): POINT_CLOUD,
            (output_type == 'MESH'): MESH,
            (output_type == 'FILTERED_MESH'): FILTERED_MESH,
            (output_type == 'TEXTURED_MESH'): TEXTURED_MESH
            },
        "HIGH": {
            (output_type == 'POINT_CLOUD'): POINT_CLOUD,
            (output_type == 'MESH'): MESH,
            (output_type == 'FILTERED_MESH'): FILTERED_MESH,
            (output_type == 'TEXTURED_MESH'): TEXTURED_MESH
            }
        }
    return (pipeline_structure_dict[quality][True])
