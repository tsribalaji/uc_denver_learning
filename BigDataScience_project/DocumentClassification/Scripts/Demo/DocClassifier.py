import os
import cv2
import pickle
import numpy as np
import base64
import tensorflow as tf


class TrainData:
    def __init__(self):
        self.model_path = ""
        self.target_shape = (96, 96)
        self.model = self.load_model(self.model_path)

    def load_model(self, path):
        model = tf.keras.models.load_model('./weights/triplet/twin_VGG_only_2.h5')
        return model

    def image_to_embedding(self, image):
        print(image.shape)
        image = cv2.resize(image, (96, 96))
        print(image.shape)
        #image = image.reshape(1, 96, 96, 3)
        #img = image[..., ::-1]
        #img = np.around(np.transpose(img, (0, 1, 2)) / 255.0, decimals=12)
        x_train = np.array([image])
        embedding = self.model.predict_on_batch(x_train)
        return embedding

    def extract_features(self, path):
        feature_map = {}
        for category in os.listdir(path):
            data = []
            for file in glob.glob(os.path.join(path, category) + '/*.jpg'):
                image_file = cv2.imread(os.path.join(path, category, file), 1)
                data.append(self.image_to_embedding(image_file))
            feature_map[category] = data
        return feature_map

    def save_features(self, features):
        pickle_out = open("feature_map.pickle", "wb")
        pickle.dump(features, pickle_out)
        pickle_out.close()

    def training(self, trainset_path):
        feature_map = self.extract_features(trainset_path)
        self.save_features(feature_map)
        return {"status": "completed"}


class Classifier:
    def __init__(self):
        self.storeDataPath = "./data/Doc_feature_map.pickle"
        self.knownData = self.loadStoredFeatureMap(self.storeDataPath)
        self.feature_extractor = TrainData()

    def loadStoredFeatureMap(self, path):
        pickle_file = open(path, "rb")
        feature_Map = pickle.load(pickle_file)
        return feature_Map

    def find_category(self, img):
        predictions = {}
        embedding_img = self.feature_extractor.image_to_embedding(img)
        for key in self.knownData:
            for data in self.knownData[key]:
                euclidean_distance = np.linalg.norm(embedding_img - data)
                if euclidean_distance < 700:
                    if key in predictions.keys():
                        predictions[key].append(euclidean_distance)
                    else:
                        predictions[key] = [euclidean_distance]
        for pred in predictions:
            predictions[pred] = min(val for (idx, val) in enumerate(predictions[pred]))
        if len(predictions) > 0:
            return min(predictions, key=predictions.get)
        else:
            return "Unknown Type - Given image is not closer to any trained images"
