from enum import Enum

import regex as re
import torch

from src import model as m


class QuestionResults(Enum):
    OK = 1
    NO_REF_FOUND = 2


class SCPPagePart(Enum):
    HEADER = 1
    OBJECT_CLASS = 2
    CONTAINMENT = 3
    DESCRIPTION = 4
    OTHER = 5


def ask_question(question, model_=None, tokenizer_=None):
    print("Question:", question)
    reference = find_reference_scp_universal(question)
    print("Reference:\n", reference)

    if reference is None or len(reference) == 0:
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
    log(question, reference, answer)
    return QuestionResults.OK, answer


def recreate_answer(tokens, start, end):
    answer = tokens[start]
    for i in range(start + 1, end + 1):
        if tokens[i][0:2] == '##':
            answer += tokens[i][2:]
        else:
            answer += ' ' + tokens[i]
    return answer


def find_reference_scp_universal(question):
    extractor = re.compile(r'SCP-?([0-9]+)+', re.IGNORECASE)
    match = extractor.search(question)

    if match is None:
        return None

    scp = match.group(1)
    return find_reference_scp(scp)


def find_reference_scp(num):
    with open(f"wiki/scp-{num}.txt") as f:
        file = f.read()

    ref = extract_part(file, SCPPagePart.OBJECT_CLASS) + "\n"
    ref += extract_part(file, SCPPagePart.DESCRIPTION)
    ref = strip_formatting(ref)

    # Cap words
    ref = ' '.join(ref.split(' ')[:200])

    return ref


page_part_extraction_regexs = {
    SCPPagePart.HEADER: r'\*\*Item #:\*\*.*(\n.*)*\*\*Object Class(.*)',
    SCPPagePart.OBJECT_CLASS: r'\*\*Object Class(.*)',
    SCPPagePart.CONTAINMENT: r'\*\*Special Containment Procedures:\*\*.*(\n[^\*]*)*',
    SCPPagePart.DESCRIPTION: r'\*\*Description:\*\*.*(\n[^\*]*)*',
    SCPPagePart.OTHER: r'',
}


def extract_part(scp_page, part):
    extractor = re.compile(page_part_extraction_regexs[part], re.IGNORECASE)
    match = extractor.search(scp_page)

    if match is None:
        print(f"Failed to extract {part} from {scp_page}!")

    return match.group(0)


def strip_formatting(scp_page):
    # Remove title line
    scp_page = re.sub(r'title:SCP-[1-9]*', '', scp_page)

    # Remove all [[>]] ... [[\>]] sections
    scp_page = re.sub(r'\[\[\>\]\](\n.*)*\[\[\/>]]', '', scp_page, re.DOTALL)

    # Remove all [[div]] ... [[/div]] sections
    scp_page = re.sub(r'\[\[div(.*)(\n.*)*\[\[\/div\]\]', '', scp_page, re.DOTALL)

    # Remove formatting **, +++
    scp_page = re.sub(r'\*\*', '', scp_page)
    scp_page = re.sub(r'\+\+\+', '', scp_page)

    # Collapse newlines
    scp_page = '\n'.join(filter(None, scp_page.split('\n')))
    return scp_page


def log(question, reference, answer):
    import json

    try:
        with open('log/log.json') as f:
            json.load(f)
    except:
        with open('log/log.json', 'w') as f:
            f.write("[]")

    with open('log/log.json') as f:
        log = json.load(f)

    log += [{
        "question": question,
        "answer": answer,
        "reference": reference
    }]

    with open('log/log.json', 'w') as f:
        json.dump(log, f, indent=4)
