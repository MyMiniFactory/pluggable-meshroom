class Setups():
    """ An instance of the class Setups represents a set of setups used to run the process.

    Building arguments
    ----------
    - quality_choice: quality chosen by the user
    - output_type_choice: type of output chosen by the user
    - nb_of_images: number of input pictures

    Attributes
    ----------
    - quality: quality chosen by the user
    - output_type: type of output chosen by the user
    - nb_of_images: number of input pictures
    """

    def __init__(self, quality_choice, output_type_choice, nb_of_images):
        self.quality = quality_choice
        self.output_type = output_type_choice
        self.nb_of_images = nb_of_images
