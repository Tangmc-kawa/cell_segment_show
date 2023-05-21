import numpy as np
from skimage import morphology, io
from scipy.ndimage import binary_dilation, binary_erosion
from joblib import Parallel, delayed


def add_protective_round(array, border_size):
    # Calculate the new dimensions for the protective round
    new_shape = tuple(np.array(array.shape) + 2 * border_size)

    # Create a new array with zeros and the new dimensions
    protected_array = np.zeros(new_shape, dtype=array.dtype)

    # Copy the original array into the new array, leaving a border of zeros
    protected_array[
        border_size:-border_size, border_size:-border_size, border_size:-border_size
    ] = array

    return protected_array


def remove_protective_round(protected_array, border_size):
    # Extract the central region of the array, excluding the protective round border
    processed_array = protected_array[
        border_size:-border_size, border_size:-border_size, border_size:-border_size
    ]

    return processed_array


def process_label(image, label, selem, iterations, border_size):
    # Find the indices of the label in the array
    indices = np.argwhere(image == label)

    # Determine the bounding box of the region
    min_z, min_y, min_x = np.min(indices, axis=0)
    max_z, max_y, max_x = np.max(indices, axis=0)

    # Crop the array to include only the region of interest
    cropped_binary_array = (
        image[min_z : max_z + 1, min_y : max_y + 1, min_x : max_x + 1] == label
    )
    protected_array = add_protective_round(
        cropped_binary_array, border_size=border_size
    )

    # Perform dilation and erosion on the cropped region
    dilated_region = binary_dilation(
        protected_array, iterations=iterations, structure=selem
    )
    eroded_region = binary_erosion(
        dilated_region, iterations=iterations, structure=selem
    )
    remove_protect_array = remove_protective_round(
        eroded_region, border_size=border_size
    )
    print(label)
    return (label, (min_z, max_z, min_y, max_y, min_x, max_x), remove_protect_array)


def perform_dilation_erosion(image, kernel_size=9, iterations=1, border_size=10):
    # Initialize an empty result array
    result = np.zeros_like(image)

    unique_labels = np.unique(image)

    print("total_round:", len(unique_labels))

    selem = morphology.ball(kernel_size)
    # Perform processing in parallel
    processed_regions = Parallel(n_jobs=-1)(
        delayed(process_label)(image, label, selem, iterations, border_size)
        for label in unique_labels
        if label != 0
    )

    # Update the result array with the processed regions
    for (
        label,
        (min_z, max_z, min_y, max_y, min_x, max_x),
        remove_protect_array,
    ) in processed_regions:
        result[min_z : max_z + 1, min_y : max_y + 1, min_x : max_x + 1][
            remove_protect_array
        ] = label

    return result
