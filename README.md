# Kalapuraparambil Automobiles AI Chatbot

## Project Description:
An AI-based chatbot for Kalapuraparambil Automobiles that provides instant customer support for vehicle customization services. The chatbot is trained using automotive industry-specific datasets and uses a feed-forward neural network. Natural Language Toolkit (NLTK) is used for tokenization, stemming, and bag-of-words creation. The chatbot answers queries about custom caravans, Force modifications, luxury interiors, and special-purpose vehicles.

## Tools:
1. Programming Language: Python
2. Dataset Format: JSON
3. Machine Learning Library: PyTorch
4. Natural Language Toolkit (NLTK)

## Project Details:
* **Dataset**: "kalapuraparambil_intents.json" file contains the automobile industry-specific dataset. Every intent has a specific tag like 'caravan', 'force_urbania', 'services', etc. Each tag has patterns that invoke that particular intent, with contextual responses about vehicle customization services.
* **Data/Text Preprocessing**: "nltk_utils.py" file preprocess the dataset using Natural Language Toolkit (NLTK). Tokenize method takes a phrase and return a list of words from 
the phrase. Stemming method stems each words i.e. "organisation" is stemmed as "organ". Bag of word method returns a boolean list that provides information on whether a given 
list of tokenized sentence's words are available on a given list of words or not.
* **Model**: "model.py" file uses PyTorch library to build a feed-forword neural network model with 1 hiddel layer. ReLU is used as an activation function. Width and depth of 
the model are also provided.
* **Training**: "train.py" file trains the model. First, it preprocess the dataset using "nltk_util.py" methods. Later, hyperparameters like number of epochs, learning rate etc
are determined here. Based on the hyperparameters model is trained on CPU or GPU (depending on the availability) using PyTorch. Training progress and results are shown in
console. After training state of the model is saved on "data.pth" file. 
* **Web Application**: "app.py" is the Flask-based web application with a modern Kimi-style interface. Features include: sidebar chat history, session management, confidence-based responses, quick reply suggestions, and beautifully formatted messages. Accessible via browser at http://127.0.0.1:5000

## Instructions to run the codes: 
1. Install python environment (e.g. conda or venv) 
2. Install pytorch according to your environment from https://pytorch.org 
3. Install nltk by running the command "pip install nltk" in the terminal 
4. Uncomment "# nltk.download('punkt') " once, for first time running nltk_utils.py.  

## Reference: 
1. https://www.nltk.org 
2. https://pytorch.org
3. https://python-engineer.com

## Youtube unlisted video link:
* Kalapuraparambil Automobiles: https://kalapuraparambil.com
