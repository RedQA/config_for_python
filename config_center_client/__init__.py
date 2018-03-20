#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kazoo.client import KazooClient
from client import ConfigCenterClient
from threading import Lock

__config_client = None
__kazoo_client = None
__service_name = None
__my_lock = Lock()


def register_myself(service_name):
    global __service_name
    __service_name = service_name


def stop_config_client():
    if __config_client is not None:
        __config_client.close()
    if __kazoo_client is not None:
        __kazoo_client.stop()
        __kazoo_client.close()


def config(name, default_value):
    global __config_client, __kazoo_client, __my_lock
    if __kazoo_client is None:
        __my_lock.acquire()
        if __kazoo_client is None:
            __kazoo_client = KazooClient(hosts='localhost:2181')   #此处可按实际需要替换成相应地址,或者写入配置文件中读取
            __kazoo_client.start()
            __config_client = ConfigCenterClient(__service_name, __kazoo_client, '/config')
            __config_client.start()
        __my_lock.release()
    return __config_client.config(name, default_value)
