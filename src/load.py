import torch
from src import model as m
import wikipedia
import time
from urllib.request import urlopen
from googlesearch import search
import en_core_web_sm
from enum import Enum
import regex as re


class QuestionResults(Enum):
    OK = 1
    NO_REF_FOUND = 2


def ask_question(question, scp, model_=None, tokenizer_=None):
    print("Question:", question)
    reference = find_reference_scp(scp)
    # print("Reference:\n", reference)

    if len(reference) == 0:
        return QuestionResults.NO_REF_FOUND, "[NO REF FOUND]"

    if model_ is None:
        model_, tokenizer_ = m.get_model()

    encoded = tokenizer_.encode_plus(question, reference)
    token_type_ids = encoded['token_type_ids']

    [start, end] = model_(torch.tensor([encoded['input_ids']]), token_type_ids=torch.tensor([token_type_ids]))
    answer_start = torch.argmax(start)
    answer_end = torch.argmax(end)
    answer__ = torch.max(start)
    end__ = torch.max(end)

    tokens = tokenizer_.convert_ids_to_tokens(encoded['input_ids'])

    answer = recreate_answer(tokens, answer_start, answer_end)

    print('Answer: ', answer)
    return QuestionResults.OK, answer


def recreate_answer(tokens, start, end):
    answer = tokens[start]
    for i in range(start + 1, end + 1):
        if tokens[i][0:2] == '##':
            answer += tokens[i][2:]
        else:
            answer += ' ' + tokens[i]
    return answer


def find_reference_scp(num):
    with open(f"wiki/scp-{num}.txt") as f:
        ref = f.read()

    # Remove all [[>]] ... [[\>]] sections
    ref = re.sub(r'\[\[\>\]\](\n.*)*\[\[\/>]]', '', ref, re.DOTALL)

    # Remove all [[div]] ... [[/div]] sections
    ref = re.sub(r'\[\[div(.*)(\n.*)*\[\[\/div\]\]', '', ref, re.DOTALL)

    # Remove formatting **, +++
    ref = re.sub(r'\*\*', '', ref)
    ref = re.sub(r'\+\+\+', '', ref)

    # Collapse newlines
    ref = '\n'.join(filter(None, ref.split('\n')))

    ref = ' '.join(ref.split(' ')[:200])

    return ref
