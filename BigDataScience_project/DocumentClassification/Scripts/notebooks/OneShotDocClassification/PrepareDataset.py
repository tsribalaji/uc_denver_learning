import sys
import numpy as np
import pandas as pd
import pickle
import os
import cv2
import time
from sklearn.utils import shuffle
import numpy.random as rng

class PrepareDataset:
    def loadimgs(self,path,n = 0):
        '''
        path => Path of train directory or test directory
        '''
        X=[]
        y = []
        cat_dict = {}
        file_dict = {}
        curr_y = n
        for category in os.listdir(path):
            print("loading category: " + category)
            file_dict[category] = [curr_y,None]
            category_path = os.path.join(path,category)
            for filename in os.listdir(category_path):
                cat_dict[curr_y] = (category, filename)
                category_images=[]
                filename_path = os.path.join(category_path, filename)
                image_path = os.path.join(filename_path)
                image = cv2.imread(image_path)
                image = cv2.resize(image, (124, 124))
                category_images.append(image)
                y.append(curr_y)
                try:
                    X.append(np.stack(category_images))
                except ValueError as e:
                    print(e)
                    print("error - category_images:", category_images)
                curr_y += 1
                file_dict[category][1] = curr_y - 1
        y = np.vstack(y)
        X = np.stack(X)
        return X,y,file_dict
    
    def prepare_trainset(self,path, save_path):
        X,y,c=self.loadimgs(path)
        with open(os.path.join(save_path,"train_124.pickle"), "wb") as f:
            print('here')
            pickle.dump((X,c),f)

    def prepare_testset(self,path, save_path):
        Xval,yval,cval=self.loadimgs(path)
        with open(os.path.join(save_path,"val_124.pickle"), "wb") as f:
            pickle.dump((Xval,cval),f)
    
    def prepare_data(self):
        save_path = r'C:\Users\sriba\Documents\Python Scripts\Siamese\One-Shot\dataset'
        self.prepare_trainset(r"C:\Users\sriba\Documents\Python Scripts\Siamese\One-Shot\dataset/Balanced_train", save_path)
        self.prepare_testset(r'C:\Users\sriba\Documents\Python Scripts\Siamese\One-Shot\dataset/Balanced_test', save_path)

obj = PrepareDataset()
obj.prepare_data()
