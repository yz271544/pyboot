FROM tensorflow/tensorflow:1.15.4

RUN apt update \
  && apt install -y libgl1-mesa-glx

COPY ./_build/tensorflow.requirements.txt /home
RUN pip install -r /home/tensorflow.requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN apt-get update && apt-get install libgomp1

ENV PYTHONPATH "/home/work"

WORKDIR /home/work
COPY ./pyboot /home/work/pyboot

ENTRYPOINT ["python", "pyboot/brun/main.py"]
