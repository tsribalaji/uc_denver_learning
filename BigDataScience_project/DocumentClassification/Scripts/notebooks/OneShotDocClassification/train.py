import sys
import numpy as np
import pandas as pd
import pickle
import os
import cv2
import time
from sklearn.utils import shuffle
import numpy.random as rng
import matplotlib.pyplot as plt
# %matplotlib inline

from model import SiameseModel


class TrainModel:
    def __init__(self):
        self.save_path = r"C:\Users\sriba\Documents\Python Scripts\Siamese\OneShotDocClassification"
        self.evaluate_every = 2000  # interval for evaluating on one-shot tasks
        self.batch_size = 32
        self.n_iter = 20000  # No. of training iterations
        self.N_way = 20  # how many classes for testing one-shot tasks
        self.n_val = 250  # how many one-shot tasks to validate on
        self.best = -1
        self.input_shape = (124, 124, 3)
        self.model_path = './weights_vgg_test/'
        self.get_trainset_data()
        self.get_testset_data()
        model_obj = SiameseModel()
        self.model = model_obj.get_model(self.input_shape)

    def get_trainset_data(self):
        with open(os.path.join(self.save_path, "dataset/train_124.pickle"), "rb") as f:
            (self.Xtrain, self.train_classes) = pickle.load(f)

            print("Training alphabets: \n")
            print(list(self.train_classes.keys()))
            print(self.Xtrain.shape)

    def get_testset_data(self):
        with open(os.path.join(self.save_path, "dataset/val_124.pickle"), "rb") as f:
            (self.Xval, self.val_classes) = pickle.load(f)

        print("Validation alphabets:", end="\n\n")
        print(list(self.val_classes.keys()))

    def get_batch(self, batch_size, s="train"):
        """Create batch of n pairs, half same class, half different class"""
        if s == 'train':
            X = self.Xtrain
            categories = self.train_classes
        else:
            X = self.Xval
            categories = self.val_classes
        # print(X.shape)
        n_classes, n_examples, w, h, channel = X.shape

        # randomly sample several classes to use in the batch
        categories = rng.choice(n_classes, size=(batch_size,), replace=False)

        # initialize 2 empty arrays for the input image batch
        pairs = [np.zeros((batch_size, h, w, 3)) for i in range(2)]

        # initialize vector for the targets
        targets = np.zeros((batch_size,))

        # make one half of it '1's, so 2nd half of batch has same class
        targets[batch_size // 2:] = 1
        for i in range(batch_size):
            # print("here")
            category = categories[i]
            idx_1 = rng.randint(0, n_examples)
            pairs[0][i, :, :, :] = X[category, idx_1].reshape(w, h, 3)
            idx_2 = rng.randint(0, n_examples)

            # pick images of same class for 1st half, different for 2nd
            if i >= batch_size // 2:
                category_2 = category
            else:
                # add a random number to the category modulo n classes to ensure 2nd image has a different category
                category_2 = (category + rng.randint(1, n_classes)) % n_classes

            pairs[1][i, :, :, :] = X[category_2, idx_2].reshape(w, h, 3)

        return pairs, targets

    def generate(self, batch_size, s="train"):
        """a generator for batches, so model.fit_generator can be used. """
        while True:
            pairs, targets = self.get_batch(batch_size, s)
            yield (pairs, targets)

    def make_oneshot_task(self, N, s="val", language=None):
        """Create pairs of test image, support set for testing N way one-shot learning. """
        if s == 'train':
            X = self.Xtrain
            categories = self.train_classes
        else:
            X = self.Xval
            categories = self.val_classes
        n_classes, n_examples, w, h, ch = X.shape

        indices = rng.randint(0, n_examples, size=(N,))
        if language is not None:  # if language is specified, select characters for that language
            low, high = categories[language]
            if N > high - low:
                raise ValueError("This language ({}) has less than {} letters".format(language, N))
            categories = rng.choice(range(low, high), size=(N,), replace=False)

        else:  # if no language specified just pick a bunch of random letters
            categories = rng.choice(range(n_classes), size=(N,), replace=False)
        true_category = categories[0]
        ex1, ex2 = rng.choice(n_examples, size=(2,))
        test_image = np.asarray([X[true_category, ex1, :, :]] * N).reshape(N, w, h, 3)
        support_set = X[categories, indices, :, :]
        support_set[0, :, :] = X[true_category, ex2]
        support_set = support_set.reshape(N, w, h, 3)
        targets = np.zeros((N,))
        targets[0] = 1
        targets, test_image, support_set = shuffle(targets, test_image, support_set)
        pairs = [test_image, support_set]

        return pairs, targets

    def test_oneshot(self, model, N, k, s="val", verbose=0):
        """Test average N way oneshot learning accuracy of a siamese neural net over k one-shot tasks"""
        n_correct = 0
        if verbose:
            print("Evaluating model on {} random {} way one-shot learning tasks ... \n".format(k, N))
        for i in range(k):
            inputs, targets = self.make_oneshot_task(N, s)
            probs = self.model.predict(inputs)
            if np.argmax(probs) == np.argmax(targets):
                n_correct += 1
        percent_correct = (100.0 * n_correct / k)
        if verbose:
            print("Got an average of {}% {} way one-shot learning accuracy \n".format(percent_correct, N))
        return percent_correct

    def nearest_neighbour_correct(self, pairs, targets):
        """returns 1 if nearest neighbour gets the correct answer for a one-shot task
            given by (pairs, targets)"""
        L2_distances = np.zeros_like(targets)
        for i in range(len(targets)):
            L2_distances[i] = np.sum(np.sqrt(pairs[0][i] ** 2 - pairs[1][i] ** 2))
        if np.argmin(L2_distances) == np.argmax(targets):
            return 1
        return 0

    def test_nn_accuracy(self, N_ways, n_trials):
        """Returns accuracy of NN approach """
        print("Evaluating nearest neighbour on {} unique {} way one-shot learning tasks ...".format(n_trials, N_ways))

        n_right = 0

        for i in range(n_trials):
            pairs, targets = self.make_oneshot_task(N_ways, "val")
            correct = self.nearest_neighbour_correct(pairs, targets)
            n_right += correct
        return 100.0 * n_right / n_trials

    def train_siamese_network(self):
        # Hyper parameters
        loss_dic = {}
        val_acc_dic = {}
        print("Starting training process!")
        print("-------------------------------------")
        t_start = time.time()
        for i in range(1, self.n_iter + 1):
            (inputs, targets) = self.get_batch(self.batch_size)
            #print('Here')
            loss = self.model.train_on_batch(inputs, targets)
            loss_dic[i] = loss
            if i % self.evaluate_every == 0:
                print("\n ------------- \n")
                print("Time for {0} iterations: {1} mins".format(i, (time.time() - t_start) / 60.0))
                print("Train Loss: {0}".format(loss))
                val_acc = self.test_oneshot(self.model, self.N_way, self.n_val, verbose=True)
                val_acc_dic[i] = val_acc
                # model.save_weights(os.path.join(model_path, 'weights.{}.h5'.format(i)))
                self.model.save(os.path.join(self.model_path, 'weights.{}.h5'.format(i)))
                if val_acc >= self.best:
                    print("Current best: {0}, previous best: {1}".format(val_acc, self.best))
                    self.best = val_acc

    def test_siamese_network(self):
        ways = np.arange(1, 20, 2)
        resume = False
        trials = 50
        val_accs, train_accs, nn_accs = [], [], []
        for N in ways:
            val_accs.append(self.test_oneshot(self.model, N, trials, "val", verbose=True))
            train_accs.append(self.test_oneshot(self.model, N, trials, "train", verbose=True))
            nn_acc = self.test_nn_accuracy(N, trials)
            nn_accs.append(nn_acc)
            print("NN Accuracy = ", nn_acc)
            print("----------------------------------------------------------")


if __name__ == "__main__":
    train_model = TrainModel()
    train_model.train_siamese_network()
    train_model.test_siamese_network()
