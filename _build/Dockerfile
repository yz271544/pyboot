#FROM --platform=$TARGETPLATFORM python:3-slim-buster
FROM python:3.6-slim

COPY ./_build/requirements.txt /home
RUN pip install -r /home/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN apt-get update && apt-get install libgomp1

ENV PYTHONPATH "/home/work"

WORKDIR /home/work
COPY ./pyboot /home/work/pyboot

ENTRYPOINT ["python", "pyboot/brun/main.py"]
