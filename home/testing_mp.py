from moviepy.editor import *
from skimage.filters import gaussian

def blur(image):
    """ Returns a blurred (radius=2 pixels) version of the image """
    return gaussian(image.astype(float), sigma=2)

clip = VideoFileClip("/media/video/22/"+vid)
clip_blurred = clip.fl_image( blur )
clip_blurred.write_videofile("/media/video/22/results/"+vid)