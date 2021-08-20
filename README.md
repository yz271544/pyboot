# pyboot

English | [Chinese](README_zh.md)

The original purpose of this project was to call scientific computing models on the edge for edge computing scenarios.

## Architecture

![arch](images/edge-model-arch.png)

![htop](images/htop-subprocess-thread.png)

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
```yaml
---
app_name: pyboot
description: pyboot for edge calc
edge:
  - name: telm_temperature # subscirbe_name: sub_process_{name}_{instance}
    instance: 1
    # input data from mqtt broker
    pre_broker: 192.168.241.1
    pre_port: 1883
    pre_topic: /gridsum/test/telm/in/m1
    pre_qos: 0
    # edge model config path: {package_full_name}.{py_module_file_name}.{func_name}
    edge_mode: pyboot.modules.gridsum.science.industry.telemetry.telm_temperature
    # input data from mqtt broker
    post_broker: 192.168.241.1
    post_port: 1883
    post_topic: /gridsum/test/telm/out/m1
    post_qos: 0


```
## Start run
```shell
pip install -r /home/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

export PYTHONPATH=$PYTHONPATH:`pwd`:'pwd'/pyboot

python pyboot/brun/main.py
```
## check the performance
You can send get request to the `http://localhost:5888/queue_size_metrics`.
To obtain whether the performance of service message processing is blocked, 
if the value of pre_queue and post_queue is greater than 0, it means that the current service has a performance backlog. 
You can adjust the number of service instances or edge model threads to improve efficiency. 
However, post_queue generally writes messages to mqtt , When the pressure is high, 
there may still be some instantaneous backlogs;


## docker
Provides a Makefile file, which can be used to easily generate docker images through the make images command. 
Currently, python:3.6-slim is used as the basic image;

## TODO

- [x] Persistence framework integration
- [x] Integration testing for some edge models
- [x] Integrate with kubernetes and kubeedge, and write related yaml resource files;
- [ ] ...