#!/usr/bin/python
from copy import deepcopy


def swap_biggest_image(data, n_row, n_col):
    # In order to find related images we need to keep track of images related
    # to the row above the current point and the images on the left of the
    # current point.
    # An image is defined by the list of its points.
    images_from_row_above = []
    images_from_current_row = []

    # We also keep track of the biggest image as we go.
    biggest_image = None

    # We navigate the image from upper left corner, fixing each row and
    # iterating through the columns.x
    for row in range(n_row):
        # When we start a new row, copy current to above and reset current.
        images_from_row_above = images_from_current_row
        images_from_current_row = []
        for col in range(n_col):
            current_image = None
            if data[row][col] == 1:
                # Look for images above (left, center, right) or on the left
                # of current point.
                # In case there's an image on the left and upper right corner
                # we need to merge them, otherwise we can safely assume they're
                # already merged, i.e. look out for this case
                # One pass ok: 110  Merge needed: 001
                #              010                110

                comes_from_upper_right = False
                # Check for an image above
                if col < len(images_from_row_above):
                    if col > 0 and images_from_row_above[col-1] is not None:
                        # Upper left corner
                        current_image = images_from_row_above[col-1]
                    if current_image is None and \
                       images_from_row_above[col] is not None:
                        # Just above
                        current_image = images_from_row_above[col]
                    if current_image is None and \
                       col + 1 < len(images_from_row_above) and \
                       images_from_row_above[col + 1] is not None:
                        # Upper right corner
                        current_image = images_from_row_above[col+1]
                        comes_from_upper_right = True

                # Check for an image on the left if we haven't found any or if
                # it comes from the upper right
                if (current_image is None or comes_from_upper_right) and \
                   col > 0 and images_from_current_row[col-1] is not None:
                    if comes_from_upper_right:
                        # Merge images in this case
                        current_image.extend(images_from_current_row[col-1])
                    else:
                        current_image = images_from_current_row[col-1]

                # Now we need to add the current point or create a new image if
                # we haven't found any related ones
                if current_image is None:
                    current_image = [(row, col)]
                else:
                    current_image.append((row, col))

            # Add current image (or None) to images_from_current_row
            images_from_current_row.append(current_image)
            # Keep track of the biggest image on the fly
            if current_image is not None:
                if biggest_image is None:
                    biggest_image = current_image
                elif len(biggest_image) < len(current_image):
                    biggest_image = current_image

    # Let's not alter the input
    result = deepcopy(data)
    if biggest_image is not None:
        # Now swap 1 to 0
        for (row, col) in biggest_image:
            result[row][col] = 0
    # And we're done!
    return result


def run_example(inp):
    def _pretty_print(data):
        for row in data:
            print ''.join(map(str, row))
    out = swap_biggest_image(inp, len(inp), len(inp[0]))
    print 'Input'
    _pretty_print(inp)
    print '=>'
    print 'Result'
    _pretty_print(out)
    print

run_example([[1, 0, 0],
             [0, 0, 0]])

run_example([[0, 0],
             [0, 0]])

run_example([[0, 0, 0, 1],
             [0, 1, 1, 1],
             [1, 0, 0, 1]])

run_example([[0, 0, 0, 1, 0],
             [0, 1, 1, 1, 1],
             [0, 0, 0, 0, 1],
             [1, 1, 1, 0, 0],
             [1, 1, 1, 1, 1],
             [0, 1, 0, 1, 0]])
