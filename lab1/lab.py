#!/usr/bin/env python3

import math 

from PIL import Image as Image

# NO ADDITIONAL IMPORTS ALLOWED!


        
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

def inverted(image):
    return apply_per_pixel(image, lambda c: 255 - c)

# HELPER FUNCTIONS

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

def generate_box_blur(n):
    """Takes a kernel size as input, returns the blur box kernel.
    Each element in the kernel is simply one over the number of elements in the
    kernel so that when each is multiplied to a pixel and added up it returns the 
    average pixel value between the selected pixels.
    """
    
    pixels = []
    for i in range(n**2):
        pixels.append(1/n**2)

    return  {'height': n, 'width': n, 'pixels': pixels}

def generate_sharp_ker(n):
    """Takes in a kernel size, returns a kernel dictionary that sharpens an image if correlated.
    
    Generates a kernel that when correlated to an image follows the Sx,y = 2*Ix,y - Bx,y
    equation. This kernel can be thought of as a matrix which is in itself the sum of two matrices.
    Thee first is a nxn zero matrix with the middle element set to 2 so that when correlated with 
    each pixel of an image it simply returns twice that pixel. The second is negative the blurr box kernel.
    Summing the two matrices and correlating it two an image is equivalent as correlating each individually
    and summing the result. Thus creating the negative blur box kernel and then replacing the middle element by 
    2-1/n**2 achieves the same purpose.
    """
    
    pixels = []
    
    for i in range(n**2):
        pixels.append(-1/n**2)
    middle = math.floor((n**2)/2)   
    pixels[middle] = 2 - 1/n**2
        
    return {'height': n, 'width': n, 'pixels': pixels}      

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

# FILTERS

def blurred(image, n):
    
    """
    Return a new image representing the result of applying a box blur (with
    kernel size n) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    blur = generate_box_blur(n)
    blurred_image = correlate(image, blur)
    return round_and_clip_image(blurred_image)

def sharpened(image, n):
    """
    Applies Sx,y = 2*Ix,y - Bx,y equation to an image in order to sharpen it.
    Uses helper function generate_sharp_ker() which generates a kernel using the
    function above.
    """
    kernel = generate_sharp_ker(n)
    sharp_image = correlate(image, kernel)
    return round_and_clip_image(sharp_image)
    
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
# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES
 
def load_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_image('test_images/cat.png')
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


def save_image(image, filename, mode='PNG'):
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
    filename = 'test_images/bluegill.png'
    
    ##---------------INVERT BLUREGILL------------------
    """Tests invert on the bluegill.png image.
    """
    # my_image = load_image(filename)
    # inv_image = inverted(my_image)
    # save_image(inv_image, 'invertedGill.png')
    
    ##----------------INVERT SHROOM--------------------
    # my_image2 = load_image('invertedShroom.png')
    # inv_image2 = inverted(my_image2)
    # save_image(inv_image2, 'revertedShroom.png')
    
    ##---------------TEST CORRELATE--------------------
    """
    Tests correlate with a 9x9 kernel on the pigbird.png image.
    """
    # lista = [0]*81
    # lista[18] = 1
    # kernel = {'height': 9, 'width': 9, 'pixels': lista}
    
    # my_image = load_image('test_images/pigbird.png')
    # image_edit = correlate(my_image, kernel)
    # save_image(image_edit, 'pigbirdedit.png')
    
    ##---------------TEST BLURR------------------------
    # my_image = load_image('test_images/cat.png')
    # blurred_image = blurred(my_image, 5)
    # save_image(blurred_image, 'blurredCat.png')
    
    ##---------TEST BLURR CENTERED PIXEL---------------
    # my_image = load_image('test_images/centered_pixel.png')
    # blurred_image = blurred(my_image, 5)
    # save_image(blurred_image, 'blurredPixel.png')
    
    ##----------TEST BLACK IMAGE-----------------------
    """Tests blurred() on the same black image with 
    two different kernel sizes to see if there is any difference (there is not).
    """
    # pixels = [0 for i in range(30)]
    # black_image = {'height': 6, 'width': 5, 'pixels': pixels}
    # blurred_black_1 = blurred(black_image, 5)
    # save_image(blurred_black_1, 'blurredBlack1.png')
    # blurred_black_2 = blurred(black_image, 9)
    # save_image(blurred_black_2, 'blurredBlack2.png')
    # save_image(black_image, 'blackImage.png')
    
    #-----------TEST SHARPEN-----------------------------
    # my_image = load_image('test_images/python.png')
    # sharp_image = sharpened(my_image, 11) 
    # save_image(sharp_image, 'sharpPython.png')
    
    #-----------TEST EDGES-----------------------------
    # my_image = load_image('test_images/construct.png')
    # edges_image = edges(my_image) 
    # save_image(edges_image, 'constructEdges.png')
    
    #-----------TEST EDGES 2----------------------------
    """
    Tests edges() on cenetered_pixel.png image and saves it.
    """    
    # my_image = load_image('test_images/centered_pixel.png')
    # edges_image = edges(my_image) 
    # save_image(edges_image, 'pixelEdges.png')