import torch
import json
import numpy as np
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

# Load model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('kalapuraparambil_intents.json', 'r', encoding='utf-8') as json_data:
    intents = json.load(json_data)

FILE = "kalapuraparambil_data.pth"
data = torch.load(FILE, map_location=torch.device('cpu'))

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

def test_query_detailed(query):
    sentence = tokenize(query)
    X = bag_of_words(sentence, all_words)
    X_tensor = X.reshape(1, X.shape[0])
    X_tensor = torch.from_numpy(X_tensor).to(device)

    output = model(X_tensor)
    probs = torch.softmax(output, dim=1)
    
    # Get top 5 predictions
    top5_probs, top5_indices = torch.topk(probs[0], 5)
    
    print(f"\nQuery: '{query}'")
    print(f"Tokens: {sentence}")
    print(f"Bag of words sum: {X.sum()}")
    print(f"\nTop 5 predictions:")
    for i, (prob, idx) in enumerate(zip(top5_probs, top5_indices), 1):
        tag = tags[idx.item()]
        print(f"  {i}. {tag}: {prob.item():.2%}")
    
    return tags[top5_indices[0].item()], top5_probs[0].item()

# Test problematic queries
print("=" * 70)
print("DETAILED CHATBOT ANALYSIS")
print("=" * 70)

queries_to_test = [
    "Hello",
    "Hi",
    "Hey",
    "Good morning",
    "What services do you offer",
    "Tell me about Force Urbania",
    "I need a caravan",
    "How much",
    "Contact",
    "xyz abc random"
]

for query in queries_to_test:
    tag, confidence = test_query_detailed(query)

print("\n" + "=" * 70)
