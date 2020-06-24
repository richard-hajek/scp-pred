import logging
from threading import Thread
from json import JSONDecoder
from src import load
from src import model as m
import json

questions = [
    "What is SCP-%NUM%?",
    "Who created SCP-%NUM%?",
    "IS SCP-%NUM% hostile?",
    "How big is SCP-%NUM%?",
    "How tall is SCP-%NUM%?"
]

SCPs = [i + 101 for i in range(100)]

results = []

print("Preparing model...")
model, tokenizer = m.get_model()

def question_worker(question, scp):
    question = question.replace("%NUM%", str(scp))
    # print("Asking " + question)
    result, answer = load.ask_question(question)
    # print("Answer: " + answer)
    global results
    results += [{"scp": scp, "question": question, "answer": answer}]
    return result == load.QuestionResults.OK


threads = []

i = 0
total = len(SCPs) * len(questions)

print("Starting threads")
for scp in SCPs:
    for question in questions:
        question_worker(question, scp)
        i += 1
        print("Progress: " + str(float(i) / float(total)))

with open("results/alpha_test_run.json", "w") as f:
    json.dump(results, f, indent=4)
