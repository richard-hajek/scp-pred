FROM python:3.7.8-stretch

WORKDIR /

RUN git clone --recursive https://github.com/richard-hajek/scp-pred.git

WORKDIR /scp-pred

RUN pip install -r requirements.txt && \
	python -m spacy download en_core_web_sm


CMD "python" "-m" "src.web"
