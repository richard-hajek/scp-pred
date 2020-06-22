# Secure, Contain, Protect and LEARN

This is a DNN model which's goal is to understand, categorize and describe individuals, entities, locations, and objects that violate natural law. 

## Setup

Currently tested on Python 3.8

```shell script
git clone --recursive git@github.com:richard-hajek/scp-pred.git
cd scp-pred
python3 -m venv venv && source venv/bin/activate # Skip if you don't wanna use venv
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

then you can

```shell script
python -m src.main
```

## Example run:

```
Question: What is SCP-555
Answer:  a metal cylinder with rounded ends

Question: What is SCP-173
Answer:  title : scp - 173 item # : scp - 173

Question: What is object class of SCP-222
Answer:  euclid

Process finished with exit code 0
```

Question about SCP-173 is currently broken because reference is hard capped at 200 words first words of an article and that's just not gonna cut it every time.

## Thanks to

**Lada Nuzhna** ([@ladanuzhna](https://github.com/ladanuzhna)) for guidance and, not gonna lie, a big chunk of the source code. Check out her repo at [ladanuzhna/Question-Answering-BERT
](https://github.com/ladanuzhna/Question-Answering-BERT)