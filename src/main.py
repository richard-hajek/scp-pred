from src import load
from src import model as m

print("Preparing model...")
model, tokenizer = m.get_model()
#model, tokenizer = None, None

if __name__ == "__main__":
    load.ask_question("What is SCP-555", model, tokenizer)
    print("\n")
    load.ask_question("Who created SCP-173", model, tokenizer)
    print("\n")
    load.ask_question("What is object class of SCP-222", model, tokenizer)
    print("\n")