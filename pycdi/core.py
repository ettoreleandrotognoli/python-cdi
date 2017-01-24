# -*- encoding: utf-8 -*-
import inspect
import random

DEFAULT_CONTEXT = 'default'

class Container(object):

    def __init__(self,*args,**kwargs):
        self.producers = dict()

    def register_producer(self,producer,produce_type=object,context=DEFAULT_CONTEXT):
        context_producers = self.producers.get(context,dict())
        context_producers[produce_type] = producer
        types = inspect.getmro(produce_type)
        for t in types:
            context_producers[t] = producer
        self.producers[context] = context_producers

    def get_producer(self,produce_type,context=DEFAULT_CONTEXT):
        context_producers = self.producers.get(context,dict())
        return context_producers.get(produce_type,produce_type)

    def produce(self,produce_type,context=DEFAULT_CONTEXT):
        producer = self.get_producer(produce_type,context)
        return self.call(producer)

    def call(self,function,*args,**kwargs):
        di_args = getattr(function,'_inject_args',[])
        di_kwargs = getattr(function,'_inject_kwargs',{})
        inject_args = map(lambda t,c: self.produce(t,c), di_args)
        inject_kwargs = dict(map(lambda kv: (kv[0],self.produce(*kv[1])),di_kwargs.items()))
        inject_kwargs.update(kwargs)
        return function(*inject_args,**inject_kwargs)


DEFAULT_CONTAINER = Container()

class CDIDecorator(object):

    def __init__(self,container=DEFAULT_CONTAINER):
        self.container = container


class Inject(CDIDecorator):
    def __init__(self,*args,**kwargs):
        super(Inject,self).__init__(kwargs.pop('container',DEFAULT_CONTAINER))
        self.context = kwargs.pop('context',DEFAULT_CONTEXT)
        self.kwargs = kwargs
        self.args = args

    def __call__(self,to_inject):
        inject_args = getattr(to_inject,'_inject_args',[])
        inject_args += [(t,self.context,) for t in self.args]
        inject_kwargs = getattr(to_inject,'_inject_kwargs',{})
        inject_kwargs.update(dict([ (k, (t,self.context)) for k,t in self.kwargs.items()]))
        setattr(to_inject,'_inject_args',inject_args)
        setattr(to_inject,'_inject_kwargs',inject_kwargs)
        return to_inject


class Producer(CDIDecorator):

    def __init__(self,produce_type=object,context=DEFAULT_CONTEXT,container=DEFAULT_CONTAINER):
        super(Producer,self).__init__(container)
        self.produce_type = produce_type
        self.context = context
        self.container = container

    def __call__(self, producer):
        self.container.register_producer(producer,self.produce_type,self.context)
        return producer

