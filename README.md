# Secure, Contain, Protect and LEARN

This is a DNN model which's goal is to understand, categorize and describe individuals, entities, locations, and objects that violate natural law. The interface is reminiscent of the recently popular ChatGPT!

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

Question: Who created SCP-173
Answer:  origin is as of yet unknown . it is constructed from concrete and rebar with traces of krylon brand spray paint

Question: What is object class of SCP-222
Answer:  euclid

Process finished with exit code 0
```
