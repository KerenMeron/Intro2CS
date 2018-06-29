#####################################################################
# FILE :ex6.py
# WRITER :Keren Meron, keren.meron, 200039626
# EXERCISE : intro2cs ex6 2015-2016
# DESCRIPTION: PhotoMosaic - taking a picture and replacing segments
# of it with pictures with similar pixels to the original
#####################################################################

from mosaic import *
from copy import deepcopy
import sys

NULL = 0
NUM_OF_ARGS = 5
MAX_VAL = 10000



def compare_pixel(pixel1, pixel2):
    '''
    Returns the sum of distances between the R, G, B values of two pixels,
    as an int.
    pixel1, pixel2: tuples with RGB values of pixels.
    '''

    r_distance = abs(pixel1[0] - pixel2[0])
    g_distance = abs(pixel1[1] - pixel2[1])
    b_distance = abs(pixel1[2] - pixel2[2])

    return r_distance + g_distance + b_distance


def compare(image1, image2):
    '''
    Finds common area between image1 and image 2, and returns the sum of
    distances between all pixels in that area, as an int.
    image1, image2: list of lists: values represent pixels.
    '''

    #finds joint area of images
    shortest_height = min(len(image1),len(image2))
    shortest_width = min(len(image1[0]),len(image2[0]))

    #sums distances between pixels
    distance = NULL
    for row in range(shortest_height):
        for col in range(shortest_width):
            distance += compare_pixel(image1[row][col], image2[row][col])
    return distance


def get_piece(image, upper_left, size):
    '''
    Returns a piece of image, as a list of lists, according to the size and
    starting point given in parameters. If size exceeds image limits,
    stops cut at end of image.
    image: list of lists: values represent pixels.
    upper_left: tuple of row, column, representing a pixel position.
    size: tuple of height, width, representing how much to cut out of image.
    '''

    #size parameters to cut out
    shortest_height = min(len(image) - upper_left[0], size[0])
    shortest_width = min(len(image[0]) - upper_left[1], size[1])
    new_image = [[NULL for i in range(shortest_width)]
                 for j in range(shortest_height)]


    for row in range(shortest_height):
        for col in range(shortest_width):
            new_image[row][col] = image[upper_left[0]+row][upper_left[1]+col]

    return new_image


def set_piece(image, upper_left, piece):
    '''
    Alters image: places the piece parameter in image, starting at the
    upper_left point given. No return value.
    If size of piece exceeds image boundaries, cuts the piece to fit.
    image: list of lists.
    upper_left: tuple of row, column, representing a pixel position.
    piece: list of lists, the picture to place.
    '''

    #size parameters to cut out
    shortest_height = min(len(piece) ,len(image) - upper_left[0])
    shortest_width = min(len(piece[0]), len(image[0]) - upper_left[1])

    #replace pixels
    for row in range(shortest_height):
        for col in range(shortest_width):
            image[row+upper_left[0]][col+upper_left[1]] = piece[row][col]


def average(image):
    '''
    Returns the average RGB values of all pixels in image, as a tuple (R,G,B).
    image: list of lists: values of tuples with RGB values.
    '''

    avg_rgb = [NULL,NULL,NULL]
    count, color_sum = NULL, NULL

    #sums up all RGB values, and counts pixels
    for row in image:
        for col in row:
            avg_rgb[0] += col[0]
            avg_rgb[1] += col[1]
            avg_rgb[2] += col[2]
            count += 1

    avg_rgb = tuple([i/count for i in avg_rgb])

    return avg_rgb


def preprocess_tiles(tiles):
    '''
    Returns the average RGB value, as a tuple (R,G,B) of each image in tiles.
    tiles: list of [images] lists of lists [pixels of each image].
    '''

    average_colors = list()

    for tile in tiles:
        average_colors.append((average(tile)))

    return average_colors


def get_best_tiles(objective, tiles, averages , num_candidates):
    '''
    Returns a list [of lists of lists] the length of num_candidates with the
    tiles which have the closest RGB values to those of the objective's.
    objective: list of lists: an image.
    tiles: list of [images] lists of lists.
    averages: list of tuples with average RGB values for each tile.
    num_candidates: int, number of tiles to return.
    '''

    #creates list of distances between the objective's and the tile's averages
    dist_list = list()
    obj_avg = average(objective)
    for avg in averages:
        dist_list.append(compare_pixel(avg, obj_avg))

    #finds smallest distances in list
    closest_tiles = list()
    for i in range(num_candidates):
        curr_min = min(dist_list)
        curr_min_idx = dist_list.index(curr_min)
        closest_tiles.append(tiles[curr_min_idx])
        dist_list[curr_min_idx] = MAX_VAL

    return closest_tiles



def choose_tile(piece, tiles):
    '''
    Returns a tile (from tiles) which is most similar to piece, according
    to a pixel by pixel comparison. Returns tile as a list of lists.
    piece: list of lists: image with pixel values.
    tiles: list of [images] lists of lists.
    '''

    tiles_dist = list()

    #create list of distances of each tile from piece
    for tile in tiles:
        tiles_dist.append(compare(tile, piece))

    #find minimal distance in list
    min_dist = min(tiles_dist)
    min_index = tiles_dist.index(min_dist)

    return tiles[min_index]


def make_mosaic(image, tiles, num_candidates):
    '''
    Returns a photomosaic, as a list of lists, by replacing each piece in
    original image with a smaller picture from tiles which has similar
    pixel values.
    Steps: Picks current piece to replace from the image, finds tile with
    closest pixel values to that piece, and replaces the tile in the image.
    image: list of lists.
    tiles: list of [images] lists of lists.
    num_candidates: int: num of potential tiles to narrow down search with.
    '''

    height = len(tiles[0])
    width = len(tiles[0][0])
    mosaic = deepcopy(image)
    averages = preprocess_tiles(tiles) #list of tuples with avg RGB per tile

    for row in range(0, len(image), height):
        for col in range(0, len(image[row]), width):
            piece = get_piece(image, (row,col), (height, width))
            potential_tiles = get_best_tiles(piece, tiles, averages,
                                             num_candidates)
            best_tile = choose_tile(piece, potential_tiles)
            set_piece(mosaic, (row, col), best_tile)

    return mosaic


def main():
    '''
    Turns an image into a photomosaic by replacing pieces with other images.
    Receives parameters from user and runs mosaic.
    Saves mosaic image to file
    '''

    image = load_image(image_source)
    tiles = build_tile_base(images_dir, tile_height)
    mosaic = make_mosaic(image, tiles, num_candidates)
    save(mosaic, output_name)

#if user calls program with proper arguments, runs main
if __name__ == '__main__':
    if len(sys.argv) == NUM_OF_ARGS+1:
        script_name = sys.argv[0]
        image_source = sys.argv[1]
        images_dir = sys.argv[2]
        output_name = sys.argv[3]
        tile_height = int(sys.argv[4])
        num_candidates = int(sys.argv[5])
        main()
    else:
        print('Wrong number of parameters. The correct usage is:\nex6.py '
               '<image_source> <images_dir> <output_name> <tile_height> '
               '<num_candidates>')

