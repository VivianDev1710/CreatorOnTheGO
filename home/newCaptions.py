import cv2
import os
import numpy as np
import pickle
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model

def idx_to_word(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

def predict_caption(model, image, tokenizer, max_length):
    in_text = 'startseq'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], max_length)
        yhat = model.predict([image, sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = idx_to_word(yhat, tokenizer)
        if word is None:
            break
        in_text += " " + word
        if word == 'endseq':
            break
      
    return in_text

def genNewCaption(vid,req):
    model=VGG16()
    model=Model(inputs=model.inputs,outputs=model.layers[-2].output)

    cap = cv2.VideoCapture('C:/Users/Admin/Desktop/Semester 5/Software Eng/harry/media/video/22/'+vid[9:])
   # image=load_img(img_path, target_size=(224,224))
    fps = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    width = cap. get(cv2. CAP_PROP_FRAME_WIDTH )
    height = cap. get(cv2. CAP_PROP_FRAME_HEIGHT )
    if width>=height:
        h=width
        w=width
    else:
        h=height
        w=height
    print("done")
    cap.set(cv2.CAP_PROP_POS_FRAMES, fps/2)
    ret, image = cap.read()
    image=img_to_array(image)
    image = image[int(height/2-h/2):int(height/2+h/2),int(width/2-w/2):int(width/2+w/2)]
    image= cv2.resize(image, (224,224))
    # print(image.shape)
    image=image.reshape((1,image.shape[0],image.shape[1],image.shape[2]))
    # print(image.shape)
    image=preprocess_input(image)
    
    feature=model.predict(image,verbose=0)
    model = load_model('C:/Users/Admin/Desktop/Semester 5/Software Eng/harry/static/img_model.h5')
 
    with open('C:/Users/Admin/Desktop/Semester 5/Software Eng/harry/static/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    cap=predict_caption(model, feature, tokenizer, 34)
    return cap[9:-7]