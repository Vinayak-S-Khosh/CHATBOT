import torch
import json
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

# Test services query
query = "What services do you offer?"
print("=" * 80)
print(f"Query: {query}")
print("=" * 80)

sentence = tokenize(query)
X = bag_of_words(sentence, all_words)
X = X.reshape(1, X.shape[0])
X = torch.from_numpy(X).to(device)

output = model(X)
_, predicted = torch.max(output, dim=1)
tag = tags[predicted.item()]

probs = torch.softmax(output, dim=1)
confidence = probs[0][predicted.item()].item()

print(f"\nIntent: {tag}")
print(f"Confidence: {confidence:.2%}")
print("\n" + "=" * 80)
print("RESPONSES:")
print("=" * 80)

for intent in intents['intents']:
    if tag == intent["tag"]:
        for i, response in enumerate(intent['responses'], 1):
            print(f"\n--- Response {i} ---")
            print(response)
            print()

print("=" * 80)
