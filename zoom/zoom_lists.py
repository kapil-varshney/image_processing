# Import the required libraries
import numpy as np
from scipy import ndimage,misc
import matplotlib.pyplot as plt

def zoom_image(img, k):

    # Retrieve the image dimensions
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]

    #Initialize zoom image lists
    z_img_l = [[] for c in range(channels)]
    z_img_lt = [[[0 for a in range(channels)] for b in range(width*k)] for c in range(height*k)]

    # Perform Pixel replication for each channel and append the channels
    for c in range(channels):
        img_l = img[:,:,c].tolist()
        z_img_l[c] = pixel_rep(img_l, height, width, k)

    #Transpose the zoomed image in appropriate dimensions
    z_img_lt = [[[z_img_l[a][c][b] for a in range(channels)] for b in range(width*k)] for c in range(height*k)]

    # Crop the image by calling the crop_image function
    zoom_img = np.array(crop_image(z_img_lt, height, width, k, y, x))

    #Return the zoomed image in lists format
    return zoom_img

def pixel_rep(img_l, height, width, k=2):
    '''
    Function to apply Pixel replication on a single channel of an image

    img_l - single channel of the original image in list
    height - height of the Image
    width - width of the image
    k - the zoom factor/scale

    returns the Pixel Replicated zoomed-in channel of the image
    '''

    # Initialize the zoom channel
    zoom_ch = [[0 for j in range(width*k)] for i in range(height*k)]

    # Pixel Repition along the width and height
    for h in range(height):
        for w in range(width):

            for i in range(h*k, h*k+k):
                for j in range(w*k, w*k+k):
                    zoom_ch[i][j] = img_l[h][w]

    return zoom_ch

def crop_image(img_l, height, width, k, c_h, c_w):
    '''
    Function to crop the zoomed image to original image dimensions

    img_l - zoom image in list format
    height - height of the original Image
    width- width of the original image
    k - zoom/scale factor
    c_h - height of pivot point (y axis)
    c_w - width of pivot point (x axis)

    Returns crop_imgl - cropped image in list format
    '''

    # Define the starting and ending positions for the crop
    start_h = c_h*k - int(height/2)
    end_h = c_h*k + int(height/2)
    start_w = c_w*k - int(width/2)
    end_w = c_w*k + int(width/2)

    # Check if the starting points go out of range(<0)
    if start_h < 0 : start_h = 0
    if start_w < 0 : start_w = 0

    crop_imgl = [[img_l[h][w] for w in range(start_w, end_w)] for h in range(start_h, end_h)]

    '''
    i = 0
    j = 0
    for h in range(start_h, end_h):
        for w in range(start_w, end_w):
            crop_imgl[i][j] = img_l[h][w]
            j+=1
        i+=1
    '''

    return crop_imgl


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
    y, x = list(map(int, input('Please enter the co-ordinates of the pivot point (space separated): ').split()))
    if y<0 or y>img.shape[0] or x<0 or x>img.shape[1]:
        print ('Pivot point outside image')
        exit()

    # Call the zoom_image function and get the zoomed image
    zoom_img = zoom_image(img, scale)

    #Save the image
    print('Saving the image...')
    misc.imsave('zoom.jpg', zoom_img)
    print('Image saved as zoom.jpg')

    #Display the zoomed image
    fig.add_subplot(1,2,2)
    plt.imshow(zoom_img)
    plt.show()
