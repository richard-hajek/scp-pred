from src import load
from src import model as m

print("Preparing model...")
model, tokenizer = m.get_model()

load.ask_question("What is SCP-555", 555, model, tokenizer)
print("\n\n\n")
load.ask_question("What is SCP-173", 173, model, tokenizer)
print("\n\n\n")
load.ask_question("What is object class of SCP-222", 222, model, tokenizer)
print("\n\n\n")