#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config_center_client import register_myself, config

#使用:先register再调用config获取值
register_myself('Test')
print config('config')

