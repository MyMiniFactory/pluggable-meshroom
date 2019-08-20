## Build the container (just in case)
```shell
docker build -t tag_name -f dockerfile_path path_to_the_folder_containing_the_docker_file
```
The -f tag is optional on LINUX if the `Dockerfile` is properly named (no file extension).

## Run the container
```shell
docker run image_name --bin bin_dir --input input_dir --output output_dir --quality quality_choice --outputType output_type_choice --nbOfImages nb_of_images --results path_to_the_results_json_file --metadata path_to_the_folder_where_to_write_the_metadata_json_file --status path_to_the_folder_where_to_write_the_status_json_file
```

|                         parameter                        |                 (possible) values             |
|----------------------------------------------------------|:---------------------------------------------:|
|                         `bin_dir`                        |    /app/Meshroom-2018.1.0/aliceVision/bin/    |
|                        `input_dir`                       |                /app/files/input/              |
|                        `output_dir`                      |                /app/files/output/             |
|                      `quality_choice`                    |               DRAFT, MEDIUM, HIGH             |
|                    `output_type_choice`                  |POINT_CLOUD, MESH, FILTERED_MESH, TEXTURED_MESH|
|                       `nb_of_images`                     |         number of images in the dataset       |
|              `path_to_the_results_json_file`             |             /app/files/results.json           |
|`path_to_the_folder_where_to_write_the_metadata_json_file`|               /app/files/output/              |
| `path_to_the_folder_where_to_write_the_status_json_file` |               /app/files/output/              |


Parameters:

- `bin_dir`: the relative or absolute path to the folder which contains Meshroom binaries. In the downloaded version: `Mershroom-2018.1.0/aliceVision/bin`
- `input_dir`: the relative or absolute path to the folder which contains the images you want to compute 
- `output_dir`: the relative or absolute path to the folder where the outputs folder will be stacked. Note that the path must exist. 
- `quality_choice`: the quality you desire. Must be one of:
    - DRAFT: the images are downscaled by 16 during DepthMap, by 8 during Texturing,
    - MEDIUM: the images are downscaled by 2 during DepthMap, by 2 during Texturing,
    - HIGH: the images are not downscaled during DepthMap and Texturing.
- `output_type_choice`: the type of output you desire. Must be one of:
    - POINT_CLOUD: computes the steps until getting the point cloud,
    - MESH: computes the steps until getting the mesh,
    - FILTERED_MESH: refines the mesh previously computed. This step will remove the biggest triangles and will only keep the biggest connected mesh,
    - TEXTURED_MESH: creates the textured mesh.
- `nb_of_images`: the number of input images.
- `path_to_the_results_json_file` (optional): you can give a results.json file in input of the wrapper specifying where the resulting files should be moved.
- `path_to_the_folder_where_to_write_the_metadata_json_file` (optional): you can decide to have a full report on the process by specifying a folder where to write the metadata.json file.
- `path_to_the_folder_where_to_write_the_status_json_file`: the relative or absolute path to the folder which will contain the status.json file which consists in a live report of the process.