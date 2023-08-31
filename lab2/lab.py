#!/usr/bin/env python3

# NO ADDITIONAL IMPORTS!
# (except in the last part of the lab; see the lab writeup for details)
import math
from PIL import Image

###FROM LAB1
def inverted(image):
    return apply_per_pixel(image, lambda c: 255 - c)

def get_pixel(image, x, y):
    return image['pixels'][x][y] 
        
def set_pixel(image, x, y, c):
    new_index = image['width']*x + y 
    image['pixels'][new_index] = c 

def apply_per_pixel(image, func, kernel = None, ker = False):
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': image['pixels'][:],
    }
     
    new_image = rearrange(image)
    for x in range(image['height']):
        for y in range(image['width']):
            color = get_pixel(new_image, x, y)
            if ker:
                newcolor = func(new_image, kernel, x, y)
            else:
                newcolor = func(color)
            set_pixel(result, x, y, newcolor)
    return result

def rearrange(image):
    """Takes an image dictionary with pixels as a list and returns another image dictionary
    with the same size and pixel colors but now as a 2d array.
    """
    new_list = []
    for x in range(0, math.floor(len(image['pixels'])/image['width'])):
        image_rows = []
        for y in range(0, image['width']): 
            image_rows.append(image['pixels'][y + x*image['width']]) 
        new_list.append(image_rows) 
        
    new_image = {'height': image['height'], 'width': image['width'], 'pixels': new_list} 
    return new_image


def ker_mult(image, kernel, x, y):
    """
    Takes an image dictionary with pixels as a 2d array, a kernel dictionary with pixels as 
    a 2d array and the image's pixel coordinates. It multiplies the kernel arround the pixel making the new pixel
    a linear combination of the pixels around the old selected pixel of coordinates x, y by centering
    the kernel on said pixel and using a for loop to iterate through the kernel's and the image's pixels. 
    Using obtain_pixel() it makes sure that no pixels are out of bounds (no index error).
    Returns the new value for the selected pixel.
    """
    linear_comb = 0
    height_diff = int((kernel['height']-1)/2)
    width_diff = int((kernel['width']-1)/2)
    
    for a in range(kernel['height']):
        for b in range(kernel['width']):
            linear_comb += kernel['pixels'][a][b]*obtain_pixel(image,x-height_diff+a, y-width_diff+b)
    return linear_comb   

def obtain_pixel(image, x, y):
    """Takes an image dictionary and the pixels coordinates in the 2d array
    as inputs. If the input pixel is out of bounds, it returns the closes border
    pixel, else it returns the input pixel's color.
    """
    if x < 0 and y < 0:
        return image['pixels'][0][0]
    elif x < 0 and y > image['width']-1:
        return image['pixels'][0][image['width']-1]
    elif x > image['height']-1 and y < 0:
        return image['pixels'][image['height']-1][0]
    elif x > image['height']-1 and y > image['width']-1:
        return image['pixels'][image['height']-1][image['width']-1]
    elif x < 0:
        return image['pixels'][0][y]
    elif y < 0: 
        return image['pixels'][x][0]
    elif x > image['height']-1:
        return image['pixels'][image['height']-1][y]
    elif y > image['width']-1:
        return image['pixels'][x][image['width']-1]
    else:
        return image['pixels'][x][y]   

def correlate(image, kernel):
    """
    Compute the result of correlating the given image with the given kernel.

    The output of this function should have the same form as a 6.009 image (a
    dictionary with 'height', 'width', and 'pixels' keys), but its pixel values
    do not necessarily need to be in the range [0,255], nor do they need to be
    integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a 
    separate structure to represent the output.

    DESCRIBE YOUR KERNEL REPRESENTATION HERE
    """
    new_kernel = rearrange(kernel)
    return apply_per_pixel(image, ker_mult, new_kernel, True)



def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the 'pixels' list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    pixels = image['pixels']
    
    for i in range(len(pixels)):
        if pixels[i] > 255:
            pixels[i] = 255
        elif pixels[i] < 0:
            pixels[i] = 0
        else:
            pixels[i] = round(pixels[i])
            
    return image

def edges(image):
    """Takes an image dictionary as an input. Creates the two kernels Kx and Ky, 
    obtains Ox and Oy (here defined as correlate_x and correlate_y) by correlating 
    the respective kernels to the image. Uses the equation O_{x,y} = round(sqrt((Ox_{x,y})**2 + (Oy_{x,y})**2))
    to create the new pixels through a for loop.
    Outputs the new image dictionary generated.
    
    """
    
    old_pixels = image['pixels']
    new_pixels = []
    
    kernel_x = {'height': 3, 'width': 3, 'pixels':[-1, 0, 1, -2, 0, 2, -1, 0, 1]}
    kernel_y = {'height': 3, 'width': 3, 'pixels':[-1, -2, -1, 0, 0, 0, 1, 2, 1]}
    
    correlate_x = correlate(image, kernel_x)
    correlate_y = correlate(image, kernel_y)
    
    for i in range(len(old_pixels)):
        new_pixels.append((correlate_x['pixels'][i]**2 + correlate_y['pixels'][i]**2)**0.5)
    
    new_image = {'height': image['height'], 'width': image['width'], 'pixels': new_pixels}
    
    return round_and_clip_image(new_image)

###LAB 2 BEGINS

def split(color_image):
    """
    Takes in a ditionary containing the pixels of a color image as a list of tuples.
    Returns three dictionaries separately containing the rgb pixels values of the image.
    """
    red_pixels = []
    green_pixels = []
    blue_pixels = []
        
    for rgb in color_image['pixels']:
        red_pixels.append(rgb[0]) 
        green_pixels.append(rgb[1])
        blue_pixels.append(rgb[2])
        
    red_dict = {'height': color_image['height'], 'width': color_image['width'], 'pixels': red_pixels}
    green_dict = {'height': color_image['height'], 'width': color_image['width'], 'pixels': green_pixels}
    blue_dict = {'height': color_image['height'], 'width': color_image['width'], 'pixels': blue_pixels}
    
    return (red_dict, green_dict, blue_dict)

def unsplit(red_vals, green_vals, blue_vals):
    """
    Takes in three dictionaries containing the rgb pixel components of a color image.
    Returns a dictionary where the 'pixels' key is a list of tuples containing the rgb values.
    (Reverts the process of split()).
    """
    rgb = []
    
    for r,g,b in zip(red_vals['pixels'], green_vals['pixels'], blue_vals['pixels']):
        rgb.append((r,g,b))
    
    return {'height': red_vals['height'], 'width': red_vals['width'], 'pixels': rgb}
  
def get_el(array, x, y):
    """Takes a  2d array
    as input. If the input pixel is out of bounds, it returns the closes border
    pixel, else it returns the input pixel's color.
    """
    if x < 0 and y < 0:
        return array[0][0]
    elif x < 0 and y > len(array[0])-1:
        return array[0][len(array[0])-1]
    elif x > len(array)-1 and y < 0:
        return array[len(array)-1][0]
    elif x > len(array)-1 and y > len(array[0])-1:
        return array[len(array)-1][len(array[0])-1]
    elif x < 0:
        return array[0][y]
    elif y < 0: 
        return array[x][0]
    elif x > len(array)-1:
        return array[len(array)-1][y]
    elif y > len(array[0])-1:
        return array[x][len(array[0])-1]
    else:
        return array[x][y]   
    
def fix(x):
    if x < 0:
        return 0
    else:
        return x
    
def obtain_index(image, x, y):
    """Takes an image dictionary and the pixels coordinates in the 2d array
    as inputs. If the input pixel is out of bounds, it returns the closes border
    pixel, else it returns the input pixel's color.
    """
    if x < 0 and y < 0:
        return (0,0)
    elif x < 0 and y > image['width']-1:
        return (0,image['width']-1)
    elif x > image['height']-1 and y < 0:
        return (image['height']-1, 0)
    elif x > image['height']-1 and y > image['width']-1:
        return (image['height']-1,image['width']-1)
    elif x < 0:
        return (0,y)
    elif y < 0: 
        return (x,0)
    elif x > image['height']-1:
        return (image['height']-1, y)
    elif y > image['width']-1:
        return (x, image['width']-1)
    else:
        return (x,y)   
    

# VARIOUS FILTERS  

def color_filter_from_greyscale_filter(filt):
    
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """
    
    def my_color_filter(color_image):
        rgb = split(color_image)
        
        red_vals = filt(rgb[0])
        green_vals = filt(rgb[1])
        blue_vals = filt(rgb[2])
        
        new_rgb = unsplit(red_vals, green_vals, blue_vals) 
        
        return new_rgb
    
    return my_color_filter

def make_blur_filter(n):
    pixels = []
    for i in range(n**2):
        pixels.append(1/n**2)
    kernel = {'height': n, 'width': n, 'pixels': pixels}
    
    def blur_filter(color_image):
        blurred_image = correlate(color_image, kernel)
        return round_and_clip_image(blurred_image)
    
    return blur_filter
        


def make_sharpen_filter(n):
    pixels = []
    
    for i in range(n**2):
        pixels.append(-1/n**2)
    middle = math.floor((n**2)/2)   
    pixels[middle] = 2 - 1/n**2
        
    kernel = {'height': n, 'width': n, 'pixels': pixels}  
    
    def sharpen_filter(color_image):
        sharpenned_image = correlate(color_image, kernel)
        return round_and_clip_image(sharpenned_image)
    
    return sharpen_filter


def filter_cascade(filters):
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """    
    def cascade(color_image):
        new_image = color_image.copy()
        for i in filters:
            new_image = i(new_image) 
        return new_image
    
    return cascade


# SEAM CARVING

# Main Seam Carving Implementation

def seam_carving(image, ncols):
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image.
    """ 
    for i in range(ncols):
        grey_image = greyscale_image_from_color_image(image)
        energy_image = compute_energy(grey_image)
        cumm_energy = cumulative_energy_map(energy_image)
        seam = minimum_energy_seam(cumm_energy)
        image = image_without_seam2(image, seam) 
        print("removed ", i+1, "columns!")
        
    return image
        
    


# Optional Helper Functions for Seam Carving

def greyscale_image_from_color_image(image):
    """
    Given a color image, computes and returns a corresponding greyscale image.

    Returns a greyscale image (represented as a dictionary).
    """
    gray_pixels = []
    for rgb in image['pixels']:
        gray_pixels.append(round(.299*rgb[0]+.587*rgb[1]+.114*rgb[2]))
        
    return {'height': image['height'], 'width': image['width'], 'pixels': gray_pixels}


def compute_energy(grey):
    """
    Given a greyscale image, computes a measure of "energy", in our case using
    the edges function from last week.

    Returns a greyscale image (represented as a dictionary).
    """
    return edges(grey)


def cumulative_energy_map(energy):
    """
    Given a measure of energy (e.g., the output of the compute_energy
    function), computes a "cumulative energy map" as described in the lab 2
    writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys (but where
    the values in the 'pixels' array may not necessarily be in the range [0,
    255].
    """
    cumm_paths = []
    cumm_cols = []
    new_pixels = []
    new_energy = rearrange(energy) 
    pixel = new_energy['pixels'][:]
    for y in range(energy['width']): 
        cumm_cols.append(pixel[0][y])
    cumm_paths.append(cumm_cols)
    for x in range(1, energy['height']):
        cumm_cols = []
        for y in range(energy['width']):
            cumm_cols.append(pixel[x][y] + min(get_el(cumm_paths,x-1,y), get_el(cumm_paths,x-1,y-1), get_el(cumm_paths,x-1,y+1)))
        cumm_paths.append(cumm_cols)
        
    for x in range(len(cumm_paths)):
        for y in range(len(cumm_paths[0])):
            new_pixels.append(cumm_paths[x][y])
            
    # print(new_pixels)
    return {'height': energy['height'], 'width': energy['width'], 'pixels': new_pixels}
                

def minimum_energy_seam(cem):
    """
    Given a cumulative energy map, returns a list of the indices into the
    'pixels' list that correspond to pixels contained in the minimum-energy
    seam (computed as described in the lab 2 writeup).
    """
    new_cem = rearrange(cem) 
    pixel = new_cem['pixels']
    paths = []
    for y in range(cem['width']):
        paths.append(pixel[cem['height']-1][y])
        
    min_path = min(paths) 
    
    for y in range(cem['width']):
        if pixel[cem['height']-1][y] == min_path: 
            y_index = y
            break
    
    seam_path = [obtain_index(cem, cem['height']-1, y_index)] 
    
    ###CHECK FOR NEIGHBOR
    for x in range(cem['height']-2, -1, -1):
        min_pixel = min(obtain_pixel(new_cem,x,y_index), obtain_pixel(new_cem,x,y_index-1), obtain_pixel(new_cem,x,y_index+1))
        if y_index == 0:
            if pixel[x][y_index] == min_pixel:
                seam_path.append(obtain_index(cem, x, y_index))
            else:
                seam_path.append(obtain_index(cem, x, y_index+1))
                y_index = y_index+1
        elif y_index == cem['width'] -1:
            if pixel[x][y_index-1] == min_pixel:
                seam_path.append(obtain_index(cem, x, y_index-1))
                y_index = y_index-1
            else:
                seam_path.append(obtain_index(cem, x, y_index))
        else:
            if pixel[x][y_index-1] == min_pixel:
                seam_path.append(obtain_index(cem, x, y_index-1))
                y_index = y_index-1
            elif pixel[x][y_index] == min_pixel:
                seam_path.append(obtain_index(cem, x, y_index))
            else:
                seam_path.append(obtain_index(cem, x, y_index+1))
                y_index = y_index+1
    
    new_path = []
    for x in seam_path:
        new_path.append(cem['width']*x[0] + x[1])
        
    return new_path

def image_without_seam(image, seam):
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """
    seam.sort()
    seam.reverse()
    new_pixels = image['pixels'][:] 
    for index in seam:
        new_pixels.pop(index)
        ###If you use remove() instead of pop() you get a swirly effect!!!!
    return {'height': image['height'], 'width': image['width'] - 1, 'pixels': new_pixels}

def image_without_seam2(image, seam):
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """
    seam.sort()
    seam.reverse()
    new_pixels = image['pixels'][:] 
    for index in seam:
        new_pixels.remove(new_pixels[index])
        ###If you use remove() instead of pop() you get a swirly effect!!!!
    return {'height': image['height'], 'width': image['width'] - 1, 'pixels': new_pixels}


# HELPER FUNCTIONS FOR LOADING AND SAVING COLOR IMAGES

def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img = img.convert('RGB')  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_color_image(image, filename, mode='PNG'):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode='RGB', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns an instance of this class
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith('RGB'):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == 'LA':
            pixels = [p[0] for p in img_data]
        elif img.mode == 'L':
            pixels = list(img_data)
        else:
            raise ValueError('Unsupported image mode: %r' % img.mode)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_greyscale_image(image, filename, mode='PNG'):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode='L', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    
    # color_cat = load_color_image('test_images/cat.png')
    # color_invert = color_filter_from_greyscale_filter(inverted)
    # inverted_cat = color_invert(color_cat)
    # save_color_image(inverted_cat, 'inverted_cat.png')
    
    # color_py = load_color_image('test_images/python.png')
    # color_blur = color_filter_from_greyscale_filter(make_blur_filter(9))
    # blurred_py = color_blur(color_py)
    # save_color_image(blurred_py, 'blurred_py.png')
    
    # color_chick = load_color_image('test_images/sparrowchick.png')
    # color_sharpen = color_filter_from_greyscale_filter(make_sharpen_filter(7))
    # sharp_chick = color_sharpen(color_chick)
    # save_color_image(sharp_chick, 'sharpSparrowchick.png')
    
    # filter1 = color_filter_from_greyscale_filter(edges)
    # filter2 = color_filter_from_greyscale_filter(make_blur_filter(5))
    # filt = filter_cascade([filter1, filter1, filter2, filter1])
    # new_img = filt(load_color_image('test_images/frog.png'))
    # save_color_image(new_img, 'cascadedFrog.png')
    
    ###TESTING SEAM-----------------------------------------------------
    # color_pig = load_color_image('test_images/pigbird.png')
    # turn_grey = greyscale_image_from_color_image(color_pig)
    # save_greyscale_image(turn_grey, 'greyPigbird.png')
    # energy_map = compute_energy(turn_grey)
    # save_greyscale_image(energy_map, 'energyPigbird.png')
    # cumm_map = cumulative_energy_map(energy_map)
    # save_greyscale_image(cumm_map, 'cummulativeEnergyPigbird.png')
    #pass

    color_pig = load_color_image('test_images/Twocats.png') 
    new_img = seam_carving(color_pig, 3)
    save_color_image(new_img, 'SwirledTwocats.png')
    
    color_pig = load_color_image('test_images/Pigbird.png') 
    new_img = seam_carving(color_pig, 3)
    save_color_image(new_img, 'SwirledPigbird.png')
    # pass
    