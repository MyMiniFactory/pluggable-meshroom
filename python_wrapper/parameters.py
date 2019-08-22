import copy

""" Different bunches of parameters depending on the quality choosen by the user.

Values
----------
- MEDIUM
    + MEDIUM_SMALL_DATASET
    + MEDIUM_AVERAGE_DATASET
    + MEDIUM_BIG_DATASET
- DRAFT
    + DRAFT_SMALL_DATASET
    + DRAFT_AVERAGE_DATASET
    + DRAFT_BIG_DATASET
- HIGH
    + HIGH_SMALL_DATASET
    + HIGH_AVERAGE_DATASET
    + HIGH_BIG_DATASET

"""

MEDIUM = {
    "camera_init": {
        "sensorDatabase": "",
        "defaultFieldOfView": str(45.0),
        "verboseLevel": "debug",
        "allowSingleView": str(1)
    },
    "feature_extraction": {
        "describerTypes": "sift",
        "describerPreset": "normal",
        "forceCpuExtraction": str(True),
        "verboseLevel": "debug",
        "rangeStart": str(-1),
        "rangeSize": str(1)
    },
    "image_matching": {
        "tree": '""',
        "weights": '""',
        "minNbImages": str(200),
        "maxDescriptors": str(500),
        "nbMatches": str(50),
        "verboseLevel": "debug"
    },
    "feature_matching": {
        "describerTypes": "sift",
        "photometricMatchingMethod": "ANN_L2",
        "geometricEstimator": "acransac",
        "geometricFilterType": "fundamental_matrix",
        "distanceRatio": str(0.8),
        "maxIteration": str(2048),
        "maxMatches": str(0),
        "savePutativeMatches": str(False),
        "guidedMatching": str(False),
        "exportDebugFiles": str(False),
        "verboseLevel": "debug",
        "rangeStart": str(-1),
        "rangeSize": str(0)
    },
    "structure_from_motion": {
        "describerTypes": "sift",
        "localizerEstimator": "acransac",
        "lockScenePreviouslyReconstructed": str(False),
        "useLocalBA": str(True),
        "localBAGraphDistance": str(1),
        "maxNumberOfMatches": str(0),
        "minInputTrackLength": str(2),
        "minNumberOfObservationsForTriangulation": str(2),
        "minAngleForTriangulation": str(3.0),
        "minAngleForLandmark": str(2.0),
        "maxReprojectionError": str(4.0),
        "minAngleInitialPair": str(5.0),
        "maxAngleInitialPair": str(40.0),
        "useOnlyMatchesFromInputFolder": str(False),
        "initialPairA": "",
        "initialPairB": "",
        "interFileExtension": ".ply",
        "verboseLevel": "debug"
    },
    "prepare_dense_scene": {
        "verboseLevel": "debug"
    },
    "camera_connection": {
        "verboseLevel": "debug"
    },
    "depth_map": {
        "downscale": str(2),
        "sgmMaxTCams": str(10),
        "sgmWSH": str(4),
        "sgmGammaC": str(5.5),
        "sgmGammaP": str(8.0),
        "refineNSamplesHalf": str(150),
        "refineNDepthsToRefine": str(31),
        "refineNiters": str(100),
        "refineWSH": str(10),
        "refineMaxTCams": str(6),
        "refineSigma": str(15),
        "refineGammaC": str(15.5),
        "refineGammaP": str(8.0),
        "refineUseTcOrRcPixSize": str(False),
        "verboseLevel": "debug",
        "groupSize": 3
    },
    "depth_map_filter": {
        "nNearestCams": str(10),
        "minNumOfConsistensCams": str(3),
        "minNumOfConsistensCamsWithLowSimilarity": str(4),
        "pixSizeBall": str(0),
        "pixSizeBallWithLowSimilarity": str(0),
        "verboseLevel": "debug",
        "rangeStart": str(-1),
        "rangeSize": str(-1)
    },
    "meshing": {
        "maxInputPoints": str(50000000),
        "maxPoints": str(5000000),
        "maxPointsPerVoxel": str(1000000),
        "minStep": str(2),
        "partitioning": "singleBlock",
        "repartition": "multiResolution",
        "angleFactor": str(15.0),
        "simFactor": str(15.0),
        "pixSizeMarginInitCoef": str(2.0),
        "pixSizeMarginFinalCoef": str(4.0),
        "voteMarginFactor": str(4.0),
        "contributeMarginFactor": str(2.0),
        "simGaussianSizeInit": str(10),
        "simGaussianSize": str(10.0),
        "minAngleThreshold": str(1.0),
        "refineFuse": str(True),
        "verboseLevel": "debug"
    },
    "mesh_filtering": {
        "removeLargeTrianglesFactor": str(60.0),
        "keepLargestMeshOnly": str(True),
        "iterations": str(5),
        "lambda": str(1.0),
        "verboseLevel": "debug"
    },
    "texturing": {
        "textureSide": str(8192),
        "downscale": str(2),
        "outputTextureFileType": "png",
        "unwrapMethod": "Basic",
        "fillHoles": str(False),
        "padding": str(15),
        "maxNbImagesForFusion": str(3),
        "bestScoreThreshold": str(0.0),
        "angleHardThreshold": str(90.0),
        "forceVisibleByAllVertices": str(False),
        "flipNormals": str(False),
        "visibilityRemappingMethod": "PullPush",
        "verboseLevel": "debug"
    }
}


# MEDIUM
MEDIUM_SMALL_DATASET = copy.deepcopy(MEDIUM)
MEDIUM_SMALL_DATASET["feature_extraction"]["describerPreset"] = "high"
MEDIUM_AVERAGE_DATASET = copy.deepcopy(MEDIUM)
MEDIUM_AVERAGE_DATASET["feature_extraction"]["describerPreset"] = "high"
MEDIUM_BIG_DATASET = copy.deepcopy(MEDIUM)
MEDIUM_BIG_DATASET["feature_extraction"]["describerPreset"] = "normal"


# DRAFT
DRAFT = copy.deepcopy(MEDIUM)
DRAFT["depth_map"]["downscale"] = str(16)
DRAFT["meshing"]["maxPoints"] = str(50000)
DRAFT["mesh_filtering"]["keepLargestMeshOnly"] = str(False)
DRAFT["texturing"]["downscale"] = str(8)

DRAFT_SMALL_DATASET = copy.deepcopy(DRAFT)
DRAFT_SMALL_DATASET["feature_extraction"]["describerPreset"] = "high"
DRAFT_AVERAGE_DATASET = copy.deepcopy(DRAFT)
DRAFT_AVERAGE_DATASET["feature_extraction"]["describerPreset"] = "high"
DRAFT_BIG_DATASET = copy.deepcopy(DRAFT)
DRAFT_BIG_DATASET["feature_extraction"]["describerPreset"] = "normal"


# HIGH
HIGH = copy.deepcopy(MEDIUM)
HIGH["depth_map"]["downscale"] = str(1)
HIGH["texturing"]["downscale"] = str(1)

HIGH_SMALL_DATASET = copy.deepcopy(HIGH)
HIGH_SMALL_DATASET["feature_extraction"]["describerPreset"] = "high"
HIGH_AVERAGE_DATASET = copy.deepcopy(HIGH)
HIGH_AVERAGE_DATASET["feature_extraction"]["describerPreset"] = "high"
HIGH_BIG_DATASET = copy.deepcopy(HIGH)
HIGH_BIG_DATASET["feature_extraction"]["describerPreset"] = "normal"


def get_the_parameters(quality, nb_of_images):
    """ Returns parameters used to run the process.

    Arguments
    ----------
    - quality: quality desired. Must be one of DRAFT, MEDIUM, HIGH
    - nb_of_images: number of input images

    Returns
    ----------
    A set of parameters.
    """
    parameters_sets_dict = {
        "DRAFT": {
                (nb_of_images < 30): DRAFT_SMALL_DATASET,
                (nb_of_images >= 30 and nb_of_images < 150): DRAFT_AVERAGE_DATASET,
                (nb_of_images >= 150): DRAFT_BIG_DATASET
            },
        "MEDIUM": {
            (nb_of_images < 30): MEDIUM_SMALL_DATASET,
            (nb_of_images >= 30 and nb_of_images < 150): MEDIUM_AVERAGE_DATASET,
            (nb_of_images >= 150): MEDIUM_BIG_DATASET
        },
        "HIGH": {
            (nb_of_images < 30): HIGH_SMALL_DATASET,
            (nb_of_images >= 30 and nb_of_images < 150): HIGH_AVERAGE_DATASET,
            (nb_of_images >= 150): HIGH_BIG_DATASET
        }
    }
    return (parameters_sets_dict[quality][True])
