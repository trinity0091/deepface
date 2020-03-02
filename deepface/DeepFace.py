import matplotlib.pyplot as plt
from keras.preprocessing import image
import warnings
warnings.filterwarnings("ignore")
import time
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import json
import keras.backend as K

#from basemodels import VGGFace, OpenFace, Facenet, FbDeepFace
#from extendedmodels import Age, Gender, Race, Emotion
#from commons import functions, distance as dst

from deepface.basemodels import VGGFace, OpenFace, Facenet, FbDeepFace
from deepface.extendedmodels import Gender, Race
from deepface.commons import functions, distance as dst

def verify(img1_path, img2_path
	, model_name ='VGG-Face', distance_metric = 'cosine', plot = False):
	
	tic = time.time()
	
	if os.path.isfile(img1_path) != True:
		raise ValueError("Confirm that ",img1_path," exists")
	
	if os.path.isfile(img2_path) != True:
		raise ValueError("Confirm that ",img2_path," exists")
	
	#-------------------------
	
	#tuned thresholds for model and metric pair
	threshold = functions.findThreshold(model_name, distance_metric)
	
	#-------------------------
	
	if model_name == 'VGG-Face':
		print("Using VGG-Face model backend and", distance_metric,"distance.")
		model = VGGFace.loadModel()
		input_shape = (224, 224)	
	
	elif model_name == 'OpenFace':
		print("Using OpenFace model backend", distance_metric,"distance.")
		model = OpenFace.loadModel()
		input_shape = (96, 96)
	
	elif model_name == 'Facenet':
		print("Using Facenet model backend", distance_metric,"distance.")
		model = Facenet.loadModel()
		input_shape = (160, 160)
	
	elif model_name == 'DeepFace':
		print("Using FB DeepFace model backend", distance_metric,"distance.")
		model = FbDeepFace.loadModel()
		input_shape = (152, 152)
	
	else:
		raise ValueError("Invalid model_name passed - ", model_name)

	#-------------------------
	#crop face
	
	img1 = functions.detectFace(img1_path, input_shape)
	img2 = functions.detectFace(img2_path, input_shape)
	
	#-------------------------
	#find embeddings
	
	img1_representation = model.predict(img1)[0,:]
	img2_representation = model.predict(img2)[0,:]
	
	#-------------------------
	#find distances between embeddings
	
	if distance_metric == 'cosine':
		distance = dst.findCosineDistance(img1_representation, img2_representation)
	elif distance_metric == 'euclidean':
		distance = dst.findEuclideanDistance(img1_representation, img2_representation)
	elif distance_metric == 'euclidean_l2':
		distance = dst.findEuclideanDistance(dst.l2_normalize(img1_representation), dst.l2_normalize(img2_representation))
	else:
		raise ValueError("Invalid distance_metric passed - ", distance_metric)
	
	#-------------------------
	#decision
	
	if distance <= threshold:
		identified =  "true"
	else:
		identified =  "false"
	
	#-------------------------
	
	if plot:
		label = "Verified: "+identified
		label += "\nThreshold: "+str(round(distance, 2))
		label += ", Max Threshold to Verify: "+str(threshold)
		label += "\nModel: "+model_name
		label += ", Similarity metric: "+distance_metric
		
		fig = plt.figure()
		fig.add_subplot(1,2, 1)
		plt.imshow(img1[0][:, :, ::-1])
		plt.xticks([]); plt.yticks([])
		fig.add_subplot(1,2, 2)
		plt.imshow(img2[0][:, :, ::-1])
		plt.xticks([]); plt.yticks([])
		fig.suptitle(label, fontsize=17)
		plt.show(block=True)
	
	#-------------------------
	
	toc = time.time()
	
	resp_obj = "{"
	resp_obj += "\"verified\": "+identified
	resp_obj += ", \"distance\": "+str(distance)
	resp_obj += ", \"max_threshold_to_verify\": "+str(threshold)
	resp_obj += ", \"model\": \""+model_name+"\""
	resp_obj += ", \"similarity_metric\": \""+distance_metric+"\""
	resp_obj += "}"
	
	resp_obj = json.loads(resp_obj) #string to json
	
	#print("identification lasts ",toc-tic," seconds")
	
	return resp_obj

race_model = Race.loadModel()
gender_model = Gender.loadModel()

def analyze(img_path):
    if os.path.isfile(img_path) != True:
        raise ValueError("Confirm that ",img_path," exists")
    #for action in actions:
    global gender_model
    global race_model
    img = functions.detectFace(img_path, (224, 224), False)
    gender_prediction = gender_model.predict(img)[0,:]
    race_predictions = race_model.predict(img)[0,:]
    K.clear_session()
    if np.argmax(gender_prediction) == 0:
        gender = "Woman"
    elif np.argmax(gender_prediction) == 1:
        gender = "Man"

    race_labels = ['asian', 'indian', 'black', 'white', 'middle eastern', 'latino hispanic']
    sum_of_predictions = race_predictions.sum()

    for i in range(0, len(race_labels)):
        race_label = race_labels[i]
        race_prediction = 100 * race_predictions[i] / sum_of_predictions
    #del gender_model
    #del race_model
    #del img
    gc.collect()

    return gender, race_labels[np.argmax(race_predictions)]

def detectFace(img_path):
	img = functions.detectFace(img_path)[0] #detectFace returns (1, 224, 224, 3)
	return img[:, :, ::-1] #bgr to rgb

#---------------------------

functions.initializeFolder()

#---------------------------
