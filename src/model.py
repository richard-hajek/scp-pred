import transformers as ppb
import warnings
from src import load
import torch

CHECKPOINT_SEC = 60
UNCASED = True
LARGE_BERT = True
EPOCHS_TRAIN = 3
LEARN_RATE = 5e-5
EVAL_MODE = True

warnings.filterwarnings('ignore')


def get_model():
    if not LARGE_BERT:
        if UNCASED:
            """
            12-layer, 768-hidden, 12-heads, 110M parameters.
            Trained on lower-cased Stanford QA dataset.
            """
            model_class, tokenizer_class, pretrained_weights = (
            ppb.BertForQuestionAnswering, ppb.BertTokenizer, 'bert-base-uncased')
        else:
            """ 	
            12-layer, 768-hidden, 12-heads, 110M parameters.
            Trained on cased Stanford QA dataset.
            """
            model_class, tokenizer_class, pretrained_weights = (
            ppb.BertForQuestionAnswering, ppb.BertTokenizer, 'bert-base-cased')
    else:
        if UNCASED:
            """
            24-layer, 1024-hidden, 16-heads, 340M parameters.
            Trained on lower-cased Stanford QA dataset.
            """
            model_class, tokenizer_class, pretrained_weights = (
            ppb.BertForQuestionAnswering, ppb.BertTokenizer, 'bert-large-uncased-whole-word-masking-finetuned-squad')
        else:
            """ 	
            24-layer, 1024-hidden, 16-heads, 340M parameters.
            Trained on cased Stanford QA dataset.
            """
            model_class, tokenizer_class, pretrained_weights = (
            ppb.BertModel, ppb.BertTokenizer, 'bert-large-cased-whole-word-masking-finetuned-squad')

    tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
    model = model_class.from_pretrained(pretrained_weights)
    return model, tokenizer


# Put the model in feed-forward mode / evaluation
if __name__ == "__main__":
    load.ask_question("What is SCP-515")
