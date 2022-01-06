# Transfer Learning Approach for Scanned Document Classification
Sribalaji Thirunavukkarasu

April 1st 2021:
1. Added initial model notebooks files 


# Demo 
I have committed web appilcation under folder Demo. For running the demo, please install the packages given in requirement.txt under the demo folder. 
Since the trained weights are large in size, I have uploaded the weights to google drive and place the link under Demo --> WebApp --> Weights --> triplet --> weights download link.txt, please download and place under the same folder and same name. Please run the classifierApp.py file to launch the web applicaiton. 

For demo purpose, I have extracted the embedding from model and store it as pickle file under data folder. 
Embedding category which current model can classify:

Classes part of training data. 
  - Ad 
  - Email
  - Letter

Model Unseen new data
  - Passport
  - Driving License
  - USA Visa image. 

# Samples
For above mentioned classes, I have copied few samples for testing the web application, which I will be using in Demo video. 

# Notebooks
This folder has the various notebook files which I used to play around training the model.

# Weights:
Please download the weights from the link for executing demo and test file
 - Siamese_VGG16 - Triplet Loss Demo (File - Demo/classifierApp.py) 
     - https://drive.google.com/file/d/17e6Kd9sp8UNLj2ZCxmuY8L_sWil0w-ga/view?usp=sharing
 - One Shot Siamese_VGG16 (File - notebooks/OneShot_Classification_Demo.ipynb) 
     - https://drive.google.com/file/d/10dY121_84Pc8D_AK2ek5p5ksEfPBu8to/view?usp=sharing

# Requirement.Txt 
  - Demo/requirements.txt

Reference links: 
  - https://www.cs.utoronto.ca/~gkoch/files/msc-thesis.pdf
  - https://www.cs.cmu.edu/~rsalakhu/papers/oneshot1.pdf
  - https://github.com/tensorfreitas/Siamese-Networks-for-One-Shot-Learning
  - https://github.com/hlamba28/One-Shot-Learning-with-Siamese-Networks
  - https://towardsdatascience.com/one-shot-learning-with-siamese-networks-using-keras-17f34e75bb3d
  - https://sorenbouma.github.io/blog/oneshot/




