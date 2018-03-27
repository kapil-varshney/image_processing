# Import the required libraries
import numpy as np
from scipy import ndimage,misc
import matplotlib.pyplot as plt


def pixel_rep(img, k=2):
    '''
    Function to zoom an image using Pixel replication

    img - original image to be zoomed
    k - the zoom factor/scale
    '''

    #Retrieve the dimensions of the image
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]

    # Initialize the zoom image
    zoom_img = np.zeros((height*k, width*k, channels), dtype = np.uint8)

    # Pixel Repition along the width and the height
    for h in range(height):
        for w in range(width):
            zoom_img[h*k : h*k+k, w*k : w*k+k, :] = img[h, w, :]

    return zoom_img


def crop_image(img, crop_size, k, c_h = None, c_w = None):
    '''
    Function to crop the zoomed in image to the size of the original image.

    img - the image to be cropped
    crop_size - shape of the original image in a tuple/list
    k - the zoom factor/scale
    c_h - height of the pivot point
    c_w - width of the pivot point
    '''

    #Provide the default pivot point
    if c_h == None : c_h=crop_size[0]*k/2
    if c_h == None : c_h=crop_size[1]*k/2

    # Define the starting and ending positions for the crop
    start_h = c_h*k - int(crop_size[0]/2)
    end_h = c_h*k + int(crop_size[0]/2)
    start_w = c_w*k - int(crop_size[1]/2)
    end_w = c_w*k + int(crop_size[1]/2)

    # Check if the starting points go out of range(<0)
    if start_h < 0 : start_h = 0
    if start_w < 0 : start_w = 0

    # Crop the image
    crop_img = img[start_h : end_h, start_w : end_w, :]

    return crop_img


if __name__ == '__main__':

    #Ask the user for the image name
    img_name = input("Enter the image name: ")
    if img_name == '':
        img_name = 'image.jpg'

    # Load the image and display it
    img = ndimage.imread(img_name)
    fig = plt.figure()
    fig.add_subplot(1,2,1)
    plt.imshow(img)

    # User input for zoom factor and the pivot point
    scale = int(input('Please enter the zoom factor: '))
    if scale<2:
        print ('Not a valid factor')
        exit()
    x, y = list(map(int, input('Please enter the co-ordinates of the pivot point (space separated): ').split()))
    if x<0 or x>img.shape[0] or y<0 or y>img.shape[1]:
        print ('Pivot point outside image')
        exit()

    # Get the zoomed in image, save it and display it
    zoom_img = pixel_rep(img, scale)
    crop_img = crop_image(zoom_img, img.shape, scale, x, y)
    print('Saving the image...')
    misc.imsave('zoom.jpg', crop_img)
    print('Image saved as zoom.jpg')
    fig.add_subplot(1,2,2)
    plt.imshow(crop_img)
    plt.show()
