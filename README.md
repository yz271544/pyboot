# pyboot

English | [Chinese](README_zh.md)

The original purpose of this project was to call scientific computing models on the edge for edge computing scenarios.

## Architecture

![arch](images/edge-model-arch.png)

![htop](images/pyboot-tensorflow.png)

## Features
### 1. starter
The system components can be expanded through the implementation of Starter. 
At present, the system provides several components for configuration, multi-process processing, and webserver. 
Finally, the system interrupts and stop signals are uniformly accepted to call the Stop function of `HookStarter` 
to recover all resources and stop the service.

1. `BaseConfStarter`:
   Provide the relevant parameters of a unified custom configuration for the entire system. 
   The relevant configuration information can be expanded by modifying the `config.yaml` and `config.py` files, 
   and the system built-in parameters are provided by the `settings.py` file;
2. `ProcessorStarter`:
   Provides multi-process and multi-threaded call functions for edge model calls. 
   The default overall call logic of an edge model will be extended to an independent sub-process, 
   and for a model call, its data transmission and reception and model call, 
   then Use more in the multithreading of this child process;
3. `TornadoServer` or `FlaskStarter`:
   Provides a unified web service for the main process, 
   currently provides two optional frameworks based on `Flask` and `Tornado`;
4. `HookStarter`:
   The `Stop` functions of all integrated components are registered and managed uniformly, 
   and the resources can be recycled in order by priority, and finally the operation of the entire service is stopped;
### 2. boot
The boot program that the system starts, loads each Starter configured in brun/__init__.py, 
and executes the Init, Setup, and Start functions of all Starter components in turn when boot.Starter() is called. 
The penultimate Starter should be It is a component with blocking function (such as FlaskStarter, TornadoStarter), 
the last one should be HookStarter;

## Configuration
v1
```yaml
# mqtt broker resources configuration
mqtts:
  - name: b1
    broker: tcp://192.168.241.1:1883
    qos: 0
    retain: false
  - name: b2
    broker: tcp://192.168.241.1:1883
    qos: 0
    retain: false
# rules configuration
rules:
  # subprocess 1
    # input data from mqtt broker
  - sub:
      name: b1
      clientId: 5555
      topic: /gridsum/test/telm/in/thend_threshold_test
    # output data from mqtt broker
    pub:
      name: b1
      clientId: 6666
      timeout: 10s
      topic: /gridsum/test/telm/out/thend_threshold_test
  # subprocess 2
  - sub:
      name: b1
      clientId: 7777
      topic: /gridsum/test/telm/in/thend_multivar_test
    pub:
      name: b1
      clientId: 8888
      timeout: 10s
      topic: /gridsum/test/telm/out/thend_multivar_test
funcs:
  - model_address: http://10.200.60.18:22122/group1/M00/00/0F/Ch1hQF-NYuyAHmhzAAHaYnbCrrs964.zip
    model_md5: pZ4DJ+YhYM9ppHD+VhLi+A==
    # edge model config path: pyboot/modules/gridsum/science/{modelName}
    # edge model reference function entry name for importlib: pyboot.modules.gridsum.science.{modelName}.index.index(event, context)
    modelName: thend_threshold_zd
    deviceName: 设备3
    pointName: OPC温度

```

v3 
```yaml
expose:
- desc: monitor the container
  name: monitor
  outPort: 38080
  protocolPort: http://:8080
funcs:
- devices:
  - deviceName: "三厂-pyboot测试设备1"
    deviceAttr:
    - attrExpression: == data_to_dict['deviceInfo']['deviceName']
      attrName: deviceName
      attrValue: 三厂-pyboot测试设备1
    - attrExpression: in data_to_dict['telemetry']
      attrName: pointName
      attrValue: pyboot1
  modelAddress: http://10.200.60.18:9000/group1/M00/49/04/Csg8EmGdnIyAVJdVAAHaY0adxNc829.zip
  modelMd5: pZ4DJ+YhYM9ppHD+VhLi+A==
  modelName: industry
- devices:
  - deviceName: "三厂-pyboot测试设备2"
    deviceAttr:
    - attrExpression: == data_to_dict['deviceInfo']['deviceName']
      attrName: deviceName
      attrValue: 三厂-pyboot测试设备2
    - attrExpression: in data_to_dict['telemetry']
      attrName: pointName
      attrValue: pyboot2
  modelAddress: http://10.200.60.18:9000/group1/M00/49/04/Csg8EmGdnIyAVJdVAAHaY0adxNc829.zip
  modelMd5: pZ4DJ+YhYM9ppHD+VhLi+A==
  modelName: test
mqtts:
- broker: tcp://192.168.241.1:1883
  name: mosquitto-20336454-5413-4e2f-b52e-b945291359c7
  retain: false
rules:
- pub:
    clientId: ef2712a2-926d-4388-92d0-60470ab2613d
    name: mosquitto-20336454-5413-4e2f-b52e-b945291359c7
    timeout: 100
    topic: cloud/edge-pyboot-e060ff31-1644570929743-e54d4620-8b1a-11ec-9969-df2a36238047
  sub:
    clientId: ae03af75-13f5-4cf9-9145-0fea4e6ff1e4
    name: mosquitto-20336454-5413-4e2f-b52e-b945291359c7
    topic: cloud/edge-data-access-a60c2306-1644570929743-e54d4620-8b1a-11ec-9969-df2a36238047

```
## Start run
```shell
pip install -r /home/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

export PYTHONPATH=$PYTHONPATH:`pwd`:'pwd'/pyboot

python pyboot/brun/main.py

# If you want to customize the incoming configuration file, you can pass in parameters. If you don’t pass it, 
# the configuration file of pyboot/conf/config.yaml will be used by default.
python pyboot/brun/main.py --config pyboot/conf/config.yaml

# If you want the program to automatically download and decompress the model file (currently supports .zip), 
# you need to declare environment variables
export DOWNLOAD_MODEL=True
```
## check the performance
You can send get request to the `http://localhost:5888/queue_size_metrics`.
To obtain whether the performance of service message processing is blocked, 
if the value of pre_queue and post_queue is greater than 0, it means that the current service has a performance backlog. 
You can adjust the number of service instances or edge model threads to improve efficiency. 
However, post_queue generally writes messages to mqtt , When the pressure is high, 
there may still be some instantaneous backlogs;

![performance](images/performance-check-block.png)

## test
1. Install the docker environment locally and download the data generator image:
```shell
export GOFAKE_IMAGE_TAG=v6.5.0-7-g4224d58
# Pull image
docker pull docker.gridsumdissector.com/kubeedge/gofakeit-server@${GOFAKE_IMAGE_TAG}
# run
docker run -itd -p 18080:8080 --restart always --name gofaker docker.gridsumdissector.com/kubeedge/gofakeit-server:${GOFAKE_IMAGE_TAG}

```

2. Install the mqtt middleware mosquitto locally
```shell
yum install mosquitto -y
```

3. Download the message forwarding program
```shell
# Download the message forwarding program
mkdir $HOME/benthos/bin -p
cd $HOME/benthos/bin
curl --noproxy "*" -X GET -u domainAccount:domainAccountPassword -O http://repository.gridsum.com/repository/cps/pkg/tools/benthos/x86_64/v3.49.0-3-g84709014/linux/amd64/bin/benthos
chmod +x benthos

# Download the transfer program configuration file
mkdir $HOME/benthos/conf -p
cd $HOME/benthos/conf
## Test model 1-pure python function
curl --noproxy "*" -X GET -u 域账号:域账号密码 -O http://repository.gridsum.com/repository/cps/pkg/tools/benthos/x86_64/v3.49.0-3-g84709014/linux/amd64/conf/http_mqtt_for_pyboot.yaml
## Test model 2-load the pickle model file
curl --noproxy "*" -X GET -u 域账号:域账号密码 -O http://repository.gridsum.com/repository/cps/pkg/tools/benthos/x86_64/v3.49.0-3-g84709014/linux/amd64/conf/http_json_mqtt_for_pyboot.yaml

```
4. Start the message transfer program
```shell
cd $HOME/benthos/bin
## Run the data required by the transfer model 1 to the local mosquitto: topic=/gridsum/test/telm/in/m1
./benthos -c ../conf/http_mqtt_for_pyboot.yaml
## Run the data required by the transfer model 2 to the local mosquitto: topic=/gridsum/test/telm/in/m_test
./benthos -c ../conf/http_json_mqtt_for_pyboot.yaml
```
5. Data format can be observed through mqttbox after startup
- Model 1 transfer data
![Model 1 transfer data](images/1.http_mqtt_for_pyboot.png)
- Model 2 transfer data
![Model 2 transfer data](images/2.http_json_mqtt_for_pyboot.png)

6. At this moment, you can go to the pyboot project and start `brun/main.py` to test the model
- Model 1 running results
![Model 1 running results](images/out/m1_out.png)
- Model 2 running results
![Model 2 running results](images/out/m2_out.png)

7. The qos parameters per unit time in the configuration file can be adjusted for performance testing
```yaml
rate_limit_resources:
  - label: foobar
    local:
      count: 1
      interval: 6s
```
- View the backlog of data processing through the interface to help understand model performance:
![Model running performance](images/out/queue_size_metrics.png)

## docker
Provides a Makefile file, which can be used to easily generate docker images through the make images command. 
Currently, python:3.6-slim is used as the basic image;
```shell
docker run --name pyboot-local-test -itd -v /lyndon/iProject/pypath/config/goboot.yml:/etc/edge/goboot.yml -e DOWNLOAD_MODEL="True" docker.gridsumdissector.com/kubeedge/pyboot:v1.0.2 --config /etc/edge/goboot.yml

## docker buildx build
docker buildx build --platform=linux/arm64 -t docker.gridsumdissector.com/kubeedge/pyboot:v3.0.0-3-g423bd55 -f _build/Dockerfile-arm64 . --load
```

## TODO

- [x] Persistence framework integration
- [x] Integration testing for some edge models
- [x] Integrate with kubernetes and kubeedge, and write related yaml resource files;
- [ ] ...