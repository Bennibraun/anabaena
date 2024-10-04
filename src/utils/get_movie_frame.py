import numpy as np

def get_movie_frame(movie, frame_idx: int, frame_return: str = 'np2'):
    """
    Given a movie and a frame index, load the frame from the movie.
    
    Args:
        movie: The movie object (assumed to have a get_frame method or be a ndarray).
        frame_idx (int): The index of the frame to retrieve.
        frame_return (str): Specifies the return type - 'np2' for numpy array or 'index' for direct indexing.
    
    Returns:
        np.ndarray or None: The specified frame in the requested format or None if an invalid return type is specified.
    """
    # Check if movie is an object with a method get_frame
    if hasattr(movie, 'get_frame'):
        # Set bundle axes if the movie object requires it
        movie.bundle_axes = ["y", "x", "c"]  # Only needed if movie is a special object
        movie_frame = movie.get_frame(frame_idx)
        if frame_return == 'np2':
            return np.array(movie_frame, dtype=np.uint16)
        elif frame_return == 'index':
            return movie_frame  # Return the frame directly if it supports indexing
    elif isinstance(movie, np.ndarray):
        try:
            return movie[frame_idx]  # Direct indexing if movie is a numpy array
        except IndexError:
            print(f"Error: Frame index {frame_idx} is out of bounds for the movie with shape {movie.shape}.")
    else:
        print(f"Error: The movie is of type {type(movie)} and does not support frame extraction.")
    
    return None
