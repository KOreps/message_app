# -*- coding:utf-8 -*-
import redis


class RedisCli(object):
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = redis.StrictRedis()
        return cls._instance
