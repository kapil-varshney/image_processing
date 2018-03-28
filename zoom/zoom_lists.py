# Import the required libraries
import numpy as np
from scipy import ndimage,misc
import matplotlib.pyplot as plt

def zoom_image(img, k):

    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]
    z_img_l = [[] for c in range(channels)]
    z_img_lt = [[[0 for a in range(channels)] for b in range(width*k)] for c in range(height*k)]
    print(np.array(z_img_lt).shape)
    for c in range(channels):
        img_l = img[:,:,c].tolist()
        z_img_l[c] = pixel_rep(img_l, height, width, k)

    print(np.array(z_img_l).shape)
    z_img_lt = [[[z_img_l[a][c][b] for a in range(channels)] for b in range(width*k)] for c in range(height*k)]
    print(np.array(z_img_lt).shape)
    return z_img_lt

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


    #zoom_img = np.transpose(np.array(zoom_image(img, scale)), (1,2,0))
    zoom_img = np.array(zoom_image(img, scale))
    #print (zoom_img.shape)
    fig.add_subplot(1,2,2)
    plt.imshow(zoom_img)
    plt.show()
