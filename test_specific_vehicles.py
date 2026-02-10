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

# Test queries for different vehicle types
test_queries = [
    # ATM/Cash queries
    ("is mobile ATM available", "cash_atm_vehicles"),
    ("Do you build cash vans", "cash_atm_vehicles"),
    ("RBI compliant vehicle", "cash_atm_vehicles"),
    
    # Medical queries
    ("Is there an ICU ambulance service?", "medical_vehicles"),
    ("Do you build ambulances", "medical_vehicles"),
    
    # Campaign queries
    ("Election campaign vehicle", "campaign_vehicles"),
    ("Political van", "campaign_vehicles"),
    
    # Business queries
    ("Food truck", "mobile_business_vehicles"),
    ("Mobile supermarket", "mobile_business_vehicles"),
]

print("=" * 80)
print("TESTING SPECIFIC VEHICLE TYPE QUERIES")
print("=" * 80)

correct = 0
total = len(test_queries)

for query, expected_intent in test_queries:
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
            response = intent['responses'][0]
            break
    
    # Check if correct
    is_correct = tag == expected_intent
    if is_correct:
        correct += 1
        status = "✅ CORRECT"
    else:
        status = f"❌ WRONG (Expected: {expected_intent})"
    
    # Color code confidence
    if confidence > 0.80:
        conf_status = "✅ HIGH"
    elif confidence > 0.60:
        conf_status = "⚠️  MEDIUM"
    else:
        conf_status = "❌ LOW"
    
    print(f"\n{'='*80}")
    print(f"Query: '{query}'")
    print(f"Expected: {expected_intent}")
    print(f"Got: {tag} {status}")
    print(f"Confidence: {confidence:.2%} {conf_status}")
    print(f"\nResponse Preview:\n{response[:200]}...")

print("\n" + "=" * 80)
print(f"Accuracy: {correct}/{total} = {(correct/total)*100:.1f}%")
print("=" * 80)
