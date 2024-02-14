from numpy.random import default_rng

class BufferingChoice:
    """
    extends numpy choice function by a buffer to boost performance
    """

    def __init__(self, options, probabilities, buffer_size: int = 1000, seed: int = None):
        """
        creates a new buffering choice

        Parameters
        ----------
        options : array-like
            a container (e.g. a list) with the possible options to draw from
        probabilities : array-like
            probability of each option
        buffer_size : int, optional
            defines how many options are drawn at each buffer creation, by default 1000.
            must be at least 1.
        seed : int, optional
            seed for reproducible behavior, by default None

        Raises
        ------
        ValueError
            if one of the parameters has an invalid value
        """
        if len(options) != len(probabilities):
            raise ValueError(f'options {options} and probabilities {probabilities} must have the same size')
        if buffer_size < 1:
            raise ValueError(f'buffer_size must be at least 1, but was {buffer_size}')
        self.__options = options
        self.__probabilities = probabilities
        self.__buffer_size = buffer_size
        self.__random_generator = default_rng(seed)
        self.__buffer_iterator = iter([])

    def next_sample(self):
        """
        returns the next sample, which is one of the given options in the constructor
        """
        try:
            return next(self.__buffer_iterator)
        except StopIteration:
            self.__buffer_iterator = iter(self.__random_generator.choice(
                self.__options, p=self.__probabilities, size=self.__buffer_size))
            return next(self.__buffer_iterator)
