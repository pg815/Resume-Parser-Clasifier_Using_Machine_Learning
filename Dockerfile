FROM python:3.7.5
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python3 -m spacy download en_core_web_sm
ENTRYPOINT [ "python" ]
CMD [ "server.py" ]

