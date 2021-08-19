#FROM --platform=$TARGETPLATFORM python:3-slim-buster
FROM python:3.6-slim

COPY ./_build/requirements.txt /home
RUN pip install -r /home/requirements.txt

ENV PYTHONPATH "/home/work"

WORKDIR /home/work
COPY ./pyboot /home/work

CMD ["python", "brun/main.py"]
ENTRYPOINT ["sh", "-c"]
