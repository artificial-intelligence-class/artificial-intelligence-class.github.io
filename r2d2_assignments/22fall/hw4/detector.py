import cv2
import pickle
import numpy as np
from rpi_sensor import RPiCamera

### Comment all keras import before submission ###
from keras.models import Sequential, load_model
from keras.preprocessing.image import img_to_array
from keras.models import model_from_json
from keras.models import Model

# Part 1: Face Detection

def preprocess(target, average_face):
    if len(target.shape) == 3:
        target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    # resize
    target_resized = cv2.resize(target, (64, 64), interpolation = cv2.INTER_AREA)
    # reshape
    target_vector = target_resized.reshape((64*64,))
    # substract mean
    target_vector = target_vector - average_face
    return target_vector

def proj2face_space(target_vector, eigenfaces):
    # Copy and paste your code from notebook
    pass

def dist2face_space(target_vector, face_space_vector):
    # Copy and paste your code from notebook
    pass

### Comment all functions below before submission ###
def pca_face_detection(camera, k, THRESHOLD):
    # Find the best k
    eigenfaces = pickle.load(open('eigenfaces.p', 'rb'))[:k,:]
    average_face = pickle.load(open('average_face.p', 'rb'))
    bounding_box = [512, 384, 400, 400] # x y w h
    # THRESHOLD = 50000 #Find the best threshold
    while True:
        img = camera.get_frame()
        cv2.rectangle(img, (312, 184), (712, 584), (0, 255, 0), 2)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        target = gray[184: 584, 312:712]
        target_vector = preprocess(target, average_face)
        face_space_vector = proj2face_space(target_vector, eigenfaces)
        distance = dist2face_space(target_vector, face_space_vector)
        if distance > THRESHOLD:
            color = (255, 255, 0)
        else:
            color = (0, 255, 0)
        cv2.rectangle(img, (312, 184), (712, 584), color, 2)
        cv2.putText(img, str(int(distance)), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA) 
        cv2.imshow('Faces', img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            cv2.destroyAllWindows()
            break
    pass

def opencv_face_detection(camera):
    # for fun
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    while True:
        img = camera.get_frame()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for x, y, w, h in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        key = cv2.waitKey(1)
        if key == ord('q'):
            cv2.destroyAllWindows()
            break

# Part 2: Mask Detection
def preprocess_mask(rgb):
    # You may need to change the resize parameter if your model takes in a different shape
    rgb = cv2.resize(rgb, (128, 128), interpolation = cv2.INTER_AREA)
    processed_img = (rgb / 255 - 0.5) * 2
    return processed_img

def predict_mask(img, model):
    processed_image = preprocess_mask(img)
    processed_image = np.expand_dims(processed_image, axis = 0)
    image_prediction = model.predict(processed_image)
    ind = np.argmin(image_prediction)
    return ind

def mask_detection(camera):
    bounding_box = [512, 384, 400, 400]
    # mask net
    with open('model.json', 'r') as f:
        model = model_from_json(f.read())
    model.load_weights('weight.h5')

    mask_dict = {1: "you probably won't die", 0: "put on your mask"}
    font = cv2.FONT_HERSHEY_PLAIN
    colors = [(0, 0, 255), (255, 255, 0)]

    while True:
        img = camera.get_frame()
        cv2.rectangle(img, (312, 184), (712, 584), (0, 255, 0), 2)
        target = img[184: 584, 312:712, :]
        ind = predict_mask(target, model)
        color = colors[ind]
        sentence = mask_dict[ind]
        cv2.rectangle(img, (312, 184), (712, 584), color, 2)
        cv2.putText(img, sentence,(100, 100), font, 3, color, 2)
        cv2.imshow("Faces found", img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    with RPiCamera('tcp://IP_ADDRESS:65433') as camera:
        mask_detection(camera)
        # pca_face_detection(camera, 20, 50000)



