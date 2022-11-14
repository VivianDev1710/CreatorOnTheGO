##from .models import Video
##from django.http import request
# from moviepy.editor import *
# from skimage.filters import gaussian
import cv2
import numpy as np
from scipy.interpolate import UnivariateSpline
import textwrap 
# from ffpyplayer.player import MediaPlayer

def LookupTable(x, y):
  spline = UnivariateSpline(x, y)
  return spline(range(256))

def sepia(img):
    img_sepia = np.array(img, dtype=np.float64) # converting to float to prevent loss
    img_sepia = cv2.transform(img_sepia, np.matrix([[0.272, 0.534, 0.131],
                                    [0.349, 0.686, 0.168],
                                    [0.393, 0.769, 0.189]])) # multipying image with special sepia matrix
    img_sepia[np.where(img_sepia > 255)] = 255 # normalizing values greater than 255 to 255
    img_sepia = np.array(img_sepia, dtype=np.uint8)
    return img_sepia
def summer(img):
    increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
    decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
    blue_channel, green_channel,red_channel  = cv2.split(img)
    red_channel = cv2.LUT(red_channel, increaseLookupTable).astype(np.uint8)
    blue_channel = cv2.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
    sum= cv2.merge((blue_channel, green_channel, red_channel ))
    return sum

def winter(img):
    increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
    decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
    blue_channel, green_channel,red_channel = cv2.split(img)
    red_channel = cv2.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
    blue_channel = cv2.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
    win= cv2.merge((blue_channel, green_channel, red_channel))
    return win

def crop_vid(vid,req):
    kernel = np.ones((3,3), np.float32)/9
    # haar_file = 'C:/Users/Admin/Desktop/Semester 5/Software Eng/harry/static/haarcascade_frontalface_default.xml'
    # face_cascade = cv2.CascadeClassifier(haar_file)
    cap = cv2.VideoCapture('C:/Users/Admin/Desktop/Semester 5/Software Eng/harry/media/video/22/'+vid[9:])
    width = cap. get(cv2. CAP_PROP_FRAME_WIDTH )
    height = cap. get(cv2. CAP_PROP_FRAME_HEIGHT )
    fps = cap. get(cv2. CAP_PROP_FPS)
    h=int(height)
    w=int(height*(1080/1920))
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    # fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    # fourcc=cv2.VideoWriter_fourcc('V','P','8','0')
    outcrop = cv2.VideoWriter('C:/Users/Admin/Desktop/Semester 5/Software Eng/harry/media/video/22/results/'+vid[9:-4]+'.mp4', fourcc, fps, (w,h))
    # player = MediaPlayer('C:/Users/Admin/Desktop/Semester 5/Software Eng/harry/media/video/22/'+vid[9:])
    i=0
    trim =False
    face=False
    if 'face' in req.POST:
        face=req.POST.get("face")
    if req.POST.get("from")!="" and req.POST.get("to")!="":
        trim = True
        print("from time rquest check",type(req.POST.get("from")))
        from_t=int(req.POST.get("from"))
        to_t=int(req.POST.get("to"))
        if from_t==-1:
            raise TypeError("Only whole numbers are allowed")
        cntr=(to_t-from_t)*fps
    try:
        # print("hi2")
        while True:
            ret, frame = cap.read()
            # if face:
            #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #     faces = face_cascade.detectMultiScale(gray, 1.3, 4)
            #     if len(faces>=1):
            #         x,y,w_face,h_face=faces[0]
            #         x_start=x+w_face-w/2
            #         if x+w_face-w/2<=0:
            #             x_start=0
            #         elif x+w_face+w/2>=width:
            #             x_start=width-w
            #         sky = frame[int(0):int(h),int(x_start):int(x_start+w)]
            #     else:
            #         sky = frame[int(0):int(h),int(width/2-w/2):int(width/2+w/2)]
            # else:
            sky = frame[int(0):int(h),int(width/2-w/2):int(width/2+w/2)]
            # audio_frame, val = player.get_frame()
            # print('status','filter' in req.POST,req.POST.get("filter"))
            
            if 'filter' in req.POST:
                fil=int(req.POST.get("filter"))
                # print("filter",fil)
                if fil==2:
                    sky = cv2.cvtColor(sky, cv2.COLOR_BGR2GRAY)
                    sky = cv2.cvtColor(sky, cv2.COLOR_GRAY2BGR)
                elif fil==3:
                    sky = cv2.convertScaleAbs(sky, beta=60)
                elif fil==4:
                    sky = cv2.convertScaleAbs(sky, beta=-60)
                elif fil==5:
                    sky=sepia(sky)
                elif fil==6:
                    sky=summer(sky)
                elif fil==7:
                    sky=winter(sky)
            cv2.rectangle(sky, (5,h-150), (w-5,h-75),(0, 255, 0), -1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            text="this is actually a dog but not really"
            wrapped_text = textwrap.wrap(text, width=15)
            cv2.putText(sky, text, (5,h-120), font, 1, (255, 255, 255), 1, scale= cv2.LINE_4)
            # filt_2D = cv2.filter2D(sky, -1, kernel)
            # sky = filt_2D 
            
            #(5,h-200), (w-10,40)
            if trim:
                if i>=from_t*fps:
                    outcrop.write(sky) 
                    if i>cntr:
                        raise TypeError("Video trim over")     
            else:
                outcrop.write(sky)
            k = cv2.waitKey(0) & 0xFF
            if k == 27:
                break
            i+=1
    except:
        cap.release()
        outcrop.release()
        cv2.destroyAllWindows()

    # cap = cv2.VideoCapture('C:/Users/Admin/Desktop/Semester 5/Software Eng/harry/media/video/22/results/final.avi')
    # width = cap. get(cv2. CAP_PROP_FRAME_WIDTH )
    # height = cap. get(cv2. CAP_PROP_FRAME_HEIGHT )
    # print(width,height)
##crop_vid(1)


# def blur(image):
#     """ Returns a blurred (radius=2 pixels) version of the image """
#     return gaussian(image.astype(float), sigma=2)

# def blur_vid(vid):
#     clip = VideoFileClip("/media/video/22/"+vid)
#     clip_blurred = clip.fl_image( blur )
#     clip_blurred.write_videofile("/media/video/22/results/"+vid)

def editVideo(vid,req):
    crop_vid(vid['video'],req)
    print("hellooozzzz",vid['video'],req.POST['filter'])
