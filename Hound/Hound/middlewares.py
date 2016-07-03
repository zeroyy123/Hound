# -*- coding: utf-8 -*-

import base64
import random
import logging
from Hound.settings import PROXIES


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        """overwrite method"""
        if 'proxy' in request.meta:
            return
        proxy = random.choice(PROXIES)
        request.meta['proxy'] = "http://%s" % proxy['ip_port']
        encoded_user_pass = base64.encodestring(proxy['user_pass'])
        request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        logging.info('[ProxyMiddleware] proxy:%s is used', proxy)