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

print("=" * 60)
print("CHATBOT DIAGNOSTIC TEST")
print("=" * 60)
print(f"Model Info:")
print(f"  - Input size: {input_size}")
print(f"  - Hidden size: {hidden_size}")
print(f"  - Output size (intents): {output_size}")
print(f"  - Total words in vocabulary: {len(all_words)}")
print("=" * 60)

# Test queries
test_queries = [
    "Hello",
    "What services do you offer?",
    "Tell me about caravans",
    "How much does it cost?",
    "I want to modify my Force Urbania",
    "Contact information",
    "Where are you located?",
    "What are your working hours?",
    "Show me your portfolio",
    "I need help",
    "random nonsense xyz abc"
]

print("\nTesting chatbot with common queries:\n")

for query in test_queries:
    sentence = tokenize(query)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    confidence = probs[0][predicted.item()].item()
    
    # Get response
    for intent in intents['intents']:
        if tag == intent["tag"]:
            response = intent['responses'][0]  # Get first response
            break
    
    # Color code confidence
    if confidence > 0.80:
        conf_status = "✅ HIGH"
    elif confidence > 0.60:
        conf_status = "⚠️  MEDIUM"
    elif confidence > 0.40:
        conf_status = "❌ LOW"
    else:
        conf_status = "🔴 VERY LOW"
    
    print(f"Query: '{query}'")
    print(f"  Intent: {tag}")
    print(f"  Confidence: {confidence:.2%} {conf_status}")
    print(f"  Response: {response[:100]}...")
    print()

print("=" * 60)
print("Test complete! The chatbot should now be working better.")
print("=" * 60)
