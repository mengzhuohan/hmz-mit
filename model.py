import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
import numpy as np
import cv2

inputs = tf.keras.layers.Input(shape=[28, 28])
flatten = keras.layers.Flatten()
#加载模型h5文件
base_model = load_model("./keras_save/model.h5")
base_model.trainable = False
model = keras.Sequential([
    inputs,
    flatten,
    base_model
])
probability_model  = tf.keras.Sequential([model,tf.keras.layers.Softmax()])

def predict_img(img_data):
	shape = img_data.shape
	if len(shape) == 3:
		img_data = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
		
	img_data = cv2.resize(img_data,(28,28),interpolation=cv2.INTER_NEAREST)
	img_data = img_data / 255.0
	img_data = img_data.reshape((-1,28,28))
	predictions = probability_model.predict(img_data)
	predict_label = np.argmax(predictions[0])
	return predict_label