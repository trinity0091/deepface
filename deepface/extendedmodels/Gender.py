#from basemodels import VGGFace
from deepface.basemodels import VGGFace

import os
from pathlib import Path
import gdown
import numpy as np
from keras.models import Model, Sequential
from keras.layers import Convolution2D, Flatten, Activation

def loadModel():
	
	model = VGGFace.baseModel()
	
	#--------------------------
	
	classes = 2
	base_model_output = Sequential()
	base_model_output = Convolution2D(classes, (1, 1), name='predictions')(model.layers[-4].output)
	base_model_output = Flatten()(base_model_output)
	base_model_output = Activation('softmax')(base_model_output)
	
	#--------------------------

	gender_model = Model(inputs=model.input, outputs=base_model_output)
	
	#--------------------------
	
	#load weights
	
	
	
	gender_model.load_weights('gender_model_weights.h5')
	
	return gender_model
	
	#--------------------------
