# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 19:04:30 2022

@author: artak
"""

# Library
import io
from keras.models import Model
from keras.layers import (
    Input,
    Conv2D,
    MaxPooling2D,
    concatenate,
    Conv2DTranspose,
    Dropout,
)
from keras.utils import normalize
import cv2
import numpy as np
from matplotlib import pyplot as plt
from django.core.files.images import ImageFile
from api.models import ImageData

# Arsitektur Deep Learning - Simple U-Net Model


def simple_unet_model(IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS):
    # Build the model
    inputs = Input((IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS))
    # s = Lambda(lambda x: x / 255)(inputs)   #No need for this if we normalize our inputs beforehand
    s = inputs

    # Contraction path
    c1 = Conv2D(
        16, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(s)
    # c1 = BatchNormalization()(c1)
    c1 = Conv2D(
        16, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c1)
    p1 = MaxPooling2D((2, 2))(c1)

    c2 = Conv2D(
        32, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(p1)
    c2 = Dropout(0.1)(c2)
    c2 = Conv2D(
        32, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c2)
    p2 = MaxPooling2D((2, 2))(c2)

    c3 = Conv2D(
        64, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(p2)
    c3 = Dropout(0.2)(c3)
    c3 = Conv2D(
        64, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c3)
    p3 = MaxPooling2D((2, 2))(c3)

    c4 = Conv2D(
        128, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(p3)
    c4 = Dropout(0.2)(c4)
    c4 = Conv2D(
        128, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c4)
    p4 = MaxPooling2D(pool_size=(2, 2))(c4)

    c5 = Conv2D(
        256, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(p4)
    c5 = Dropout(0.3)(c5)
    c5 = Conv2D(
        256, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c5)

    # Expansive path
    u6 = Conv2DTranspose(128, (2, 2), strides=(2, 2), padding="same")(c5)
    u6 = concatenate([u6, c4])
    c6 = Conv2D(
        128, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(u6)
    c6 = Dropout(0.2)(c6)
    c6 = Conv2D(
        128, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c6)

    u7 = Conv2DTranspose(64, (2, 2), strides=(2, 2), padding="same")(c6)
    u7 = concatenate([u7, c3])
    c7 = Conv2D(
        64, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(u7)
    c7 = Dropout(0.2)(c7)
    c7 = Conv2D(
        64, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c7)

    u8 = Conv2DTranspose(32, (2, 2), strides=(2, 2), padding="same")(c7)
    u8 = concatenate([u8, c2])
    c8 = Conv2D(
        32, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(u8)
    c8 = Dropout(0.1)(c8)
    c8 = Conv2D(
        32, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c8)

    u9 = Conv2DTranspose(16, (2, 2), strides=(2, 2), padding="same")(c8)
    u9 = concatenate([u9, c1], axis=3)
    c9 = Conv2D(
        16, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(u9)
    c9 = Dropout(0.1)(c9)
    c9 = Conv2D(
        16, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c9)

    outputs = Conv2D(1, (1, 1), activation="sigmoid")(c9)

    model = Model(inputs=[inputs], outputs=[outputs])
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    # model.summary()

    return model


# Input image config to model


def get_model():
    IMG_HEIGHT = 448
    IMG_WIDTH = 448
    IMG_CHANNELS = 1
    return simple_unet_model(IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS)


# Looping segmentation images on folder choosed


# ------------- MAIN FUNCTION ---------------------------------#
# Load Pretrained Model
model = get_model()
model.load_weights("api\\scripts\\model_tesis_epoch20_sz448.hdf5")


def segmentation(user, image, task=None):
    try:
        test_img_other = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    except:
        test_img_other = cv2.imdecode(
            np.fromstring(image.read(), np.uint8), cv2.IMREAD_GRAYSCALE
        )
    # test_img_other = cv2.cvtColor(test_img_other, cv2.COLOR_BGR2GRAY)
    test_img_other = test_img_other[50:400, 100:500]
    width = 448
    height = 448  # keep original height
    dim = (width, height)

    # RESIZE IMAGE (RESIZE DETEKSI BERDASARKAN TEPI STILL ON DEVELOP, INI MEMAKAI RESIZE DENGAN MENENTUKAN UKURAN)
    test_img_other = cv2.resize(test_img_other, dim, interpolation=cv2.INTER_AREA)
    test_img_other_norm2 = np.expand_dims(
        normalize(np.array(test_img_other), axis=1), 2
    )
    test_img_other_norm3 = np.resize(test_img_other_norm2, (448, 448, 1))
    test_img_other_norm = test_img_other_norm3[:, :, 0][:, :, None]
    test_img_other_input = np.expand_dims(test_img_other_norm, 0)

    # PREDIKSI SEGMENTASI
    # Predict and threshold for values above 0.5 probability. Change the probability threshold to low value (e.g. 0.05) for watershed demo.
    prediction_other = (model.predict(test_img_other_input)[0, :, :, 0] > 0.02).astype(
        np.uint8
    )
    plt.switch_backend("AGG")
    buffer2 = io.BytesIO()
    plt.axis("off")  # axis x,y dimatikan sementara
    plt.imshow(test_img_other, cmap="gray", interpolation="none")
    plt.savefig(buffer2, bbox_inches="tight", pad_inches=0)
    sources = ImageFile(buffer2, str(image))

    plt.imshow(prediction_other, cmap="jet", interpolation="none", alpha=0.7)

    # MENCARI LINGKARAN BESAR DAN MEMBERSIHKAN LAINNYA
    # ------- STILL ON DEVELOP -----

    # SAVE IMAGE HASIL SEGMENTASI
    buffer1 = io.BytesIO()
    plt.savefig(buffer1, bbox_inches="tight", pad_inches=0)
    content_file = ImageFile(buffer1, str(image))
    print("buffer1", content_file)
    try:
        results = ImageData.objects.create(user=user, task=task, images=sources)
        results["result"] = content_file
        results.save()
        buffer1.close()
        buffer2.close()
        return results
    except:
        buffer1.close()
        buffer2.close()
        raise Exception("Could not save image database")
