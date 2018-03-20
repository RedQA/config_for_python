#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import antenna
# from kazoo.recipe.cache import TreeCache
import json
import logging
import time

from cache import TreeCache

logger = logging.getLogger(__name__)


class ConfigCenterClient:
    def __init__(self, service_name, kazoo_client, path):
        self.service_path = '/{}/{}'.format(path, service_name)
        self.started = False
        self.client = kazoo_client

    def start(self):
        if self.started:
            return
        self.started = True
        #若使用kazoo 2.4.0版本可直接使用其内置的TreeCache即可:此处使用2.2.1版本kazoo,所以将2.4.0中TreeCache手动引入文件中
        self.tree_cache = TreeCache(self.client, self.service_path)
        self.tree_cache.start()

    def close(self):
        self.tree_cache.close()

    def _config(self, name):
        node_path = '{}/{}'.format(self.service_path, name)
        node = self.tree_cache.get_data(node_path)
        config_item = json.loads(node[1])
        return config_item['value']

    def config(self, name, default_value):
        try:
            return self._config(name)
        except Exception as e:
            logging.error('fail to get config from tree cache with error=%s', e)
            return default_value
