import warnings
warnings.filterwarnings("ignore")
import time
import os
from os import path
import numpy as np
import pandas as pd
from tqdm import tqdm
<<<<<<< HEAD
import pickle

from deepface.basemodels import VGGFace, OpenFace, Facenet, FbDeepFace, DeepID, DlibWrapper, ArcFace, Boosting
from deepface.extendedmodels import Age, Gender, Race, Emotion
from deepface.commons import functions, realtime, distance as dst

def build_model(model_name):
	
	"""
	This function builds a deepface model
	Parameters:
		model_name (string): face recognition or facial attribute model
			VGG-Face, Facenet, OpenFace, DeepFace, DeepID for face recognition
			Age, Gender, Emotion, Race for facial attributes
	
	Returns:
		built deepface model
	"""
	
	models = {
		'VGG-Face': VGGFace.loadModel, 
		'OpenFace': OpenFace.loadModel,
		'Facenet': Facenet.loadModel,
		'DeepFace': FbDeepFace.loadModel,
		'DeepID': DeepID.loadModel,
		'Dlib': DlibWrapper.loadModel,
		'ArcFace': ArcFace.loadModel,
		'Emotion': Emotion.loadModel,
		'Age': Age.loadModel,
		'Gender': Gender.loadModel,
		'Race': Race.loadModel
	}
=======
import json
import keras.backend as K

#from basemodels import VGGFace, OpenFace, Facenet, FbDeepFace
#from extendedmodels import Age, Gender, Race, Emotion
#from commons import functions, distance as dst

from deepface.basemodels import VGGFace, OpenFace, Facenet, FbDeepFace
from deepface.extendedmodels import Gender, Race
from deepface.commons import functions, distance as dst
>>>>>>> ab08f87535266c7680d1f2d45890d9f2cfac2450

	model = models.get(model_name)
	
	if model:
		model = model()
		#print('Using {} model backend'.format(model_name))
		return model
	else:
		raise ValueError('Invalid model_name passed - {}'.format(model_name))

def verify(img1_path, img2_path = '', model_name = 'VGG-Face', distance_metric = 'cosine', 
		   model = None, enforce_detection = True, detector_backend = 'mtcnn'):	
	
	"""
	This function verifies an image pair is same person or different persons.	
	
	Parameters:
		img1_path, img2_path: exact image path, numpy array or based64 encoded images could be passed. If you are going to call verify function for a list of image pairs, then you should pass an array instead of calling the function in for loops.
		
		e.g. img1_path = [
			['img1.jpg', 'img2.jpg'], 
			['img2.jpg', 'img3.jpg']
		]
		
		model_name (string): VGG-Face, Facenet, OpenFace, DeepFace, DeepID, Dlib, ArcFace or Ensemble
		
		distance_metric (string): cosine, euclidean, euclidean_l2
		
		model: Built deepface model. A face recognition model is built every call of verify function. You can pass pre-built face recognition model optionally if you will call verify function several times.
		
			model = DeepFace.build_model('VGG-Face')
		
		enforce_detection (boolean): If any face could not be detected in an image, then verify function will return exception. Set this to False not to have this exception. This might be convenient for low resolution images.
		
		detector_backend (string): set face detector backend as mtcnn, opencv, ssd or dlib
	
	Returns:
		Verify function returns a dictionary. If img1_path is a list of image pairs, then the function will return list of dictionary.
		
		{
			"verified": True
			, "distance": 0.2563
			, "max_threshold_to_verify": 0.40
			, "model": "VGG-Face"
			, "similarity_metric": "cosine"
		}
		
	"""
	
	tic = time.time()
	
	img_list, bulkProcess = functions.initialize_input(img1_path, img2_path)	
	functions.initialize_detector(detector_backend = detector_backend)

	resp_objects = []
	
	#--------------------------------
	
	if model_name == 'Ensemble':
		model_names = ["VGG-Face", "Facenet", "OpenFace", "DeepFace"]
		metrics = ["cosine", "euclidean", "euclidean_l2"]
	else:
		model_names = []; metrics = []
		model_names.append(model_name)
		metrics.append(distance_metric)
			
	#--------------------------------
	
	if model == None:
		if model_name == 'Ensemble':
			models = Boosting.loadModel()
		else:
			model = build_model(model_name)
			models = {}
			models[model_name] = model
	else:
		if model_name == 'Ensemble':
			Boosting.validate_model(model)
			models = model.copy()
		else:
			models = {}
			models[model_name] = model
	
	#------------------------------
	
	#calling deepface in a for loop causes lots of progress bars. this prevents it.
	disable_option = False if len(img_list) > 1 else True
	
	pbar = tqdm(range(0,len(img_list)), desc='Verification', disable = disable_option)
	
	for index in pbar:
	
		instance = img_list[index]
		
		if type(instance) == list and len(instance) >= 2:
			img1_path = instance[0]; img2_path = instance[1]
			
			ensemble_features = []
			
			for i in  model_names:
				custom_model = models[i]
				
				#decide input shape
				input_shape = functions.find_input_shape(custom_model)	
				input_shape_x = input_shape[0]; input_shape_y = input_shape[1]
				
				#----------------------
				#detect and align faces
				
				img1 = functions.preprocess_face(img=img1_path
					, target_size=(input_shape_y, input_shape_x)
					, enforce_detection = enforce_detection
					, detector_backend = detector_backend)
				
				img2 = functions.preprocess_face(img=img2_path
					, target_size=(input_shape_y, input_shape_x)
					, enforce_detection = enforce_detection
					, detector_backend = detector_backend)
				
				#----------------------
				#find embeddings
				
				img1_representation = custom_model.predict(img1)[0,:]
				img2_representation = custom_model.predict(img2)[0,:]
				
				#----------------------
				#find distances between embeddings
				
				for j in metrics:
					
					if j == 'cosine':
						distance = dst.findCosineDistance(img1_representation, img2_representation)
					elif j == 'euclidean':
						distance = dst.findEuclideanDistance(img1_representation, img2_representation)
					elif j == 'euclidean_l2':
						distance = dst.findEuclideanDistance(dst.l2_normalize(img1_representation), dst.l2_normalize(img2_representation))
					else:
						raise ValueError("Invalid distance_metric passed - ", distance_metric)
					
					distance = np.float64(distance) #causes trobule for euclideans in api calls if this is not set (issue #175)
					#----------------------
					#decision
					
					if model_name != 'Ensemble':
						
						threshold = dst.findThreshold(i, j)

						if distance <= threshold:
							identified = True
						else:
							identified = False
						
						resp_obj = {
							"verified": identified
							, "distance": distance
							, "max_threshold_to_verify": threshold
							, "model": model_name
							, "similarity_metric": distance_metric
							
						}
						
						if bulkProcess == True:
							resp_objects.append(resp_obj)
						else:
							return resp_obj
					
					else: #Ensemble
						
						#this returns same with OpenFace - euclidean_l2
						if i == 'OpenFace' and j == 'euclidean':
							continue
						else:
							ensemble_features.append(distance)
					
			#----------------------
			
			if model_name == 'Ensemble':
				
				boosted_tree = Boosting.build_gbm()
				
				prediction = boosted_tree.predict(np.expand_dims(np.array(ensemble_features), axis=0))[0]
				
				verified = np.argmax(prediction) == 1
				score = prediction[np.argmax(prediction)]
				
				resp_obj = {
					"verified": verified
					, "score": score
					, "distance": ensemble_features
					, "model": ["VGG-Face", "Facenet", "OpenFace", "DeepFace"]
					, "similarity_metric": ["cosine", "euclidean", "euclidean_l2"]
				}
				
				if bulkProcess == True:
					resp_objects.append(resp_obj)
				else:
					return resp_obj
				
			#----------------------

		else:
			raise ValueError("Invalid arguments passed to verify function: ", instance)

	#-------------------------

	toc = time.time()
	
	if bulkProcess == True:
		
		resp_obj = {}

		for i in range(0, len(resp_objects)):
			resp_item = resp_objects[i]
			resp_obj["pair_%d" % (i+1)] = resp_item
			
		return resp_obj

def analyze(img_path, actions = ['emotion', 'age', 'gender', 'race']
			, models = {}, enforce_detection = True
			, detector_backend = 'mtcnn'):
	
	"""
	This function analyzes facial attributes including age, gender, emotion and race
	
	Parameters:
		img_path: exact image path, numpy array or base64 encoded image could be passed. If you are going to analyze lots of images, then set this to list. e.g. img_path = ['img1.jpg', 'img2.jpg']
		
		actions (list): The default is ['age', 'gender', 'emotion', 'race']. You can drop some of those attributes.
		
		models: facial attribute analysis models are built in every call of analyze function. You can pass pre-built models to speed the function up.
		
			models = {}
			models['age'] = DeepFace.build_model('Age')
			models['gender'] = DeepFace.build_model('Gender')
			models['emotion'] = DeepFace.build_model('Emotion')
			models['race'] = DeepFace.build_model('race')
		
		enforce_detection (boolean): The function throws exception if a face could not be detected. Set this to True if you don't want to get exception. This might be convenient for low resolution images.
		
		detector_backend (string): set face detector backend as mtcnn, opencv, ssd or dlib.
	Returns:
		The function returns a dictionary. If img_path is a list, then it will return list of dictionary.
		
		{
			"region": {'x': 230, 'y': 120, 'w': 36, 'h': 45},
			"age": 28.66,
			"gender": "woman",
			"dominant_emotion": "neutral",
			"emotion": {
				'sad': 37.65260875225067, 
				'angry': 0.15512987738475204, 
				'surprise': 0.0022171278033056296, 
				'fear': 1.2489334680140018, 
				'happy': 4.609785228967667, 
				'disgust': 9.698561953541684e-07, 
				'neutral': 56.33133053779602
			}
			"dominant_race": "white",
			"race": {
				'indian': 0.5480832420289516, 
				'asian': 0.7830780930817127, 
				'latino hispanic': 2.0677512511610985, 
				'black': 0.06337375962175429, 
				'middle eastern': 3.088453598320484, 
				'white': 93.44925880432129
			}
		}
		
	"""

	img_paths, bulkProcess = functions.initialize_input(img_path)
	functions.initialize_detector(detector_backend = detector_backend)
	
	#---------------------------------
	
	built_models = list(models.keys())
	
	#---------------------------------
	
	#pre-trained models passed but it doesn't exist in actions
	if len(built_models) > 0:
		if 'emotion' in built_models and 'emotion' not in actions:
			actions.append('emotion')
			
		if 'age' in built_models and 'age' not in actions:
			actions.append('age')
		
		if 'gender' in built_models and 'gender' not in actions:
			actions.append('gender')
		
		if 'race' in built_models and 'race' not in actions:
			actions.append('race')
	
	#---------------------------------

	if 'emotion' in actions and 'emotion' not in built_models:
		models['emotion'] = build_model('Emotion')

	if 'age' in actions and 'age' not in built_models:
		models['age'] = build_model('Age')

	if 'gender' in actions and 'gender' not in built_models:
		models['gender'] = build_model('Gender')

	if 'race' in actions and 'race' not in built_models:
		models['race'] = build_model('Race')
		
	#---------------------------------

	resp_objects = []
	
	disable_option = False if len(img_paths) > 1 else True
	
	global_pbar = tqdm(range(0,len(img_paths)), desc='Analyzing', disable = disable_option)
	
	for j in global_pbar:
		img_path = img_paths[j]

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

def detectFace(img_path, detector_backend = 'mtcnn'):
	
	"""
	This function applies pre-processing stages of a face recognition pipeline including detection and alignment	
	
	Parameters:
		img_path: exact image path, numpy array or base64 encoded image
		
		detector_backend (string): face detection backends are mtcnn, opencv, ssd or dlib
	
	Returns:
		deteced and aligned face in numpy format
	"""
	
	functions.initialize_detector(detector_backend = detector_backend)
	
	img = functions.preprocess_face(img = img_path, detector_backend = detector_backend)[0] #preprocess_face returns (1, 224, 224, 3)
	return img[:, :, ::-1] #bgr to rgb
	
#---------------------------
#main

functions.initializeFolder()
