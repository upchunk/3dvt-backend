# -*- coding: utf-8 -*-
"""
Created on Tue May 24 23:04:32 2022

@author: artak
"""

import tensorflow
from train import get_model
from simple_unet_model import simple_unet_model  # Use normal unet model
from keras.utils import normalize
import cv2
import numpy as np
from matplotlib import pyplot as plt
import skimage
import skimage.transform
import PIL


#######################################################################
# Predict on a few images
model = simple_unet_model(448, 448, 1)
# Trained for 50 epochs and then additional 100
model.load_weights('model_tesis_epoch20_sz448.hdf5')
# model.load_weights('mitochondria_gpu_tf1.4.hdf5')  #Trained for 50 epochs


test_img_other = cv2.imread('dataset/tes-1-448.tif', 0)
#test_img_other = cv2.imread('data/test_images/img8.tif', 0)
test_img_other_norm = np.expand_dims(
    normalize(np.array(test_img_other), axis=1), 2)
test_img_other_norm = test_img_other_norm[:, :, 0][:, :, None]
test_img_other_input = np.expand_dims(test_img_other_norm, 0)

# Predict and threshold for values above 0.5 probability
# Change the probability threshold to low value (e.g. 0.05) for watershed demo.
prediction_other = (model.predict(test_img_other_input)
                    [0, :, :, 0] > 0.5).astype(np.uint8)


img_tes2 = PIL.Image.open('dataset/tes-1-448.tif')
image_sequence = img_tes2.getdata()
image_array = np.array(image_sequence)
in_img = skimage.transform.resize(
    image_array, (448, 448, 1), mode='constant', preserve_range=True)

in_img = tensorflow.keras.preprocessing.image.img_to_array(img_tes2)
in_img = skimage.transform.resize(
    in_img, (448, 448, 1), mode='constant', preserve_range=True)
test2 = in_img / 255.0
img1 = test2.squeeze()
prediction1 = model.predict(np.expand_dims(test2, 0))
img3 = prediction1.squeeze()
img4 = np.ma.masked_where(img3 == 0, img3)

plt.imshow(test_img_other, cmap='gray', interpolation='none')
plt.imshow(prediction_other, cmap='jet', interpolation='none', alpha=0.7)
plt.axis('off')
# plt.show()
plt.savefig("test.png",  bbox_inches='tight', pad_inches=0)
