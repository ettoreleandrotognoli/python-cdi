# -*- encoding: utf-8 -*-
from .core import CDIDecorator, DEFAULT_CONTAINER
import random

class Singleton(CDIDecorator):

    def __init__(self,limit=1,container=DEFAULT_CONTAINER):
        super(Singleton,self).__init__(DEFAULT_CONTAINER)
        self.limit = limit

    def __call__(self,clazz):

        def producer():
            instance = getattr(clazz,'_instance',None)
            if instance is None:
                instance = [self.container.call(clazz) for i in range(self.limit)]
                setattr(clazz,'_instance',instance)
            return random.choice(instance)

        self.container.register_producer(producer,clazz)
        return clazz

