# -*- encoding: utf-8 -*-
import inspect
from six import string_types
import collections
import sys

python_version = sys.version_info.major

DEFAULT_CONTEXT = 'default'


class CDIContainer(object):
    def register_instance(self, instance, product_type=None, context=DEFAULT_CONTEXT):
        raise NotImplementedError()

    def register_producer(self, producer, produce_type=object, context=DEFAULT_CONTEXT):
        raise NotImplementedError()

    def get_producer(self, produce_type=object, context=DEFAULT_CONTEXT):
        raise NotImplementedError()

    def sub_container(self, *args, **kwargs):
        raise NotImplementedError()

    def produce(self, produce_type, context=DEFAULT_CONTEXT):
        raise NotImplementedError()

    def call(self, function, *args, **kwargs):
        raise NotImplementedError()


class PyCDIContainer(CDIContainer):
    def __init__(self, producers=None, parent=None):
        self.parent = parent
        self.producers = dict() if producers is None else producers
        self.register_instance(self)

    def register_instance(self, instance, produce_type=None, context=DEFAULT_CONTEXT):
        producer = (lambda *args, **kwargs: instance)
        produce_type = type(instance) if produce_type is None else produce_type
        self.register_producer(producer, produce_type, context)

    def register_producer(self, producer, produce_type=object, context=DEFAULT_CONTEXT):
        context_producers = self.producers.get(context, dict())
        context_producers[produce_type] = producer
        types = inspect.getmro(produce_type)
        for t in types:
            context_producers[t] = producer
        self.producers[context] = context_producers

    def get_producer(self, produce_type=object, context=DEFAULT_CONTEXT):
        context_producers = self.producers.get(context, dict())
        producer = context_producers.get(produce_type, False)
        if producer:
            return producer
        if self.parent is not None:
            return self.parent.get_producer(produce_type, context=context)
        else:
            return produce_type

    def sub_container(self, *args, **kwargs):
        container = PyCDIContainer(parent=self)
        for instance in args:
            container.register_instance(instance)
        for context, instances in kwargs.items():
            if isinstance(instances, string_types):
                instances = [instances]
            if not isinstance(instances, collections.Iterable):
                instances = [instances]
            for instance in instances:
                container.register_instance(instance, context=context)
        return container

    def produce(self, produce_type, context=DEFAULT_CONTEXT):
        producer = self.get_producer(produce_type, context)
        return self.call(producer)

    def call(self, function, *args, **kwargs):
        di_args = getattr(function, '_inject_args', [])
        di_kwargs = getattr(function, '_inject_kwargs', {})
        inject_args = list(map(lambda tc: self.produce(tc[0], tc[1]), di_args)) + list(args)
        inject_kwargs = dict(map(lambda kv: (kv[0], self.produce(*kv[1])), di_kwargs.items()))
        inject_kwargs.update(kwargs)
        return function(*inject_args, **inject_kwargs)


DEFAULT_CONTAINER = PyCDIContainer()


class CDIDecorator(object):
    def __init__(self, _container=DEFAULT_CONTAINER):
        self.container = _container

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()


class Py2Inject(CDIDecorator):
    def __init__(self, *args, **kwargs):
        super(Py2Inject, self).__init__(kwargs.pop('_container', DEFAULT_CONTAINER))
        self.context = kwargs.pop('_context', DEFAULT_CONTEXT)
        self.kwargs = kwargs
        self.args = args

    def __call__(self, to_inject):
        inject_args = getattr(to_inject, '_inject_args', [])
        inject_args += [(t, self.context,) for t in self.args]
        inject_kwargs = getattr(to_inject, '_inject_kwargs', {})
        inject_kwargs.update(dict([(k, (t, self.context)) for k, t in self.kwargs.items()]))
        setattr(to_inject, '_inject_args', inject_args)
        setattr(to_inject, '_inject_kwargs', inject_kwargs)
        return to_inject


class Py3Inject(CDIDecorator):
    def __init__(self, *args, **kwargs):
        super(Py3Inject, self).__init__(kwargs.pop('_container', DEFAULT_CONTAINER))
        self.context = kwargs.pop('_context', DEFAULT_CONTEXT)
        self.args = args
        self.kwargs = kwargs

    def __call__(self, to_inject):
        if isinstance(to_inject, type):
            annotations = to_inject.__init__.__annotations__
        else:
            annotations = to_inject.__annotations__
        parameters = filter(lambda item: item[0] is not 'return', annotations.items())
        inject_args = getattr(to_inject, '_inject_args', [])
        inject_args += [(t, self.context,) for t in self.args]
        inject_kwargs = getattr(to_inject, '_inject_kwargs', {})
        inject_kwargs.update(dict([(k, (t, self.kwargs.get(k, self.context))) for k, t in parameters]))
        setattr(to_inject, '_inject_args', inject_args)
        setattr(to_inject, '_inject_kwargs', inject_kwargs)
        return to_inject


if python_version == 3:
    Inject = Py3Inject
else:
    Inject = Py2Inject


class Py2Producer(CDIDecorator):
    def __init__(self, produce_type=object, _context=DEFAULT_CONTEXT, _container=DEFAULT_CONTAINER):
        super(Producer, self).__init__(_container)
        self.produce_type = produce_type
        self.context = _context

    def __call__(self, producer):
        self.container.register_producer(producer, self.produce_type, self.context)
        return producer


class Py3Producer(CDIDecorator):
    def __init__(self, produce_type=None, _context=DEFAULT_CONTEXT, _container=DEFAULT_CONTAINER):
        super(Producer, self).__init__(_container)
        self.produce_type = produce_type
        self.context = _context

    def __call__(self, producer):
        if self.produce_type is None:
            produce_type = producer.__annotations__.get('return', object)
        else:
            produce_type = self.produce_type
        self.container.register_producer(producer, produce_type, self.context)


if python_version == 3:
    Producer = Py3Producer
else:
    Producer = Py2Producer
