# -*- encoding: utf-8 -*-
import collections
import inspect

from six import string_types

DEFAULT_CONTEXT = 'default'

INJECT_ARGS = '_inject_args'
INJECT_KWARGS = '_inject_kwargs'


class InjectionPoint(object):
    def __init__(self, member=None, name=None, type=object, context=DEFAULT_CONTEXT):
        self.context = context
        self.name = name
        self.member = member
        self.type = type


class CDIContainer(object):
    def register_instance(self, instance, product_type=None, context=DEFAULT_CONTEXT):
        raise NotImplementedError()

    def register_producer(self, producer, produce_type=object, context=DEFAULT_CONTEXT):
        raise NotImplementedError()

    def get_producer(self, produce_type=object, context=DEFAULT_CONTEXT):
        raise NotImplementedError()

    def sub_container(self, *args, **kwargs):
        raise NotImplementedError()

    def resolve(self, injection_point, **kwargs):
        raise NotImplementedError()

    def produce(self, produce_type, context=DEFAULT_CONTEXT):
        raise NotImplementedError()

    def call(self, function, *args, **kwargs):
        raise NotImplementedError()


def resolve_forward_reference(reference_name, scope):
    return eval(reference_name, scope.__globals__, scope.__globals__)


def get_di_args(obj):
    di_args = getattr(obj, INJECT_ARGS, [])
    forward_references = [(index, value) for index, value in enumerate(di_args) if isinstance(value[0], string_types)]
    for index, value in forward_references:
        di_args[index] = (resolve_forward_reference(value[0], obj), value[1],)
    return di_args


def get_di_kwargs(obj):
    di_kwargs = getattr(obj, INJECT_KWARGS, {})
    forward_references = dict([
        (k, (resolve_forward_reference(v[0], obj), v[1]))
        for k, v in di_kwargs.items()
        if isinstance(v[0], string_types)
    ])
    di_kwargs.update(forward_references)
    return di_kwargs


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

    def resolve(self, injection_point, kwargs=None):
        if kwargs and injection_point.name in kwargs:
            return kwargs[injection_point.name]
        producer = self.get_producer(injection_point.type, injection_point.context)
        return self.call(producer, injection_point=injection_point)

    def produce(self, produce_type, context=DEFAULT_CONTEXT):
        producer = self.get_producer(produce_type, context)
        return self.call(producer)

    def _resolve_di_args(self, member, di_args, args):
        injection_points = map(lambda kv: InjectionPoint(member, kv[0], *kv[1]), zip(range(len(di_args)), di_args))
        inject_args = list(map(lambda ij: self.resolve(ij), injection_points)) + list(args)
        return inject_args

    def _resolve_di_kwargs(self, member, di_kwargs, kwargs):
        injection_points = map(lambda kv: InjectionPoint(member, kv[0], *kv[1]), di_kwargs.items())
        inject_kwargs = dict(map(lambda ij: (ij.name, self.resolve(ij, kwargs)), injection_points))
        return inject_kwargs

    def call(self, function, *args, **kwargs):
        di_args = get_di_args(function)
        di_kwargs = get_di_kwargs(function)
        inject_args = self._resolve_di_args(function, di_args, args)
        inject_kwargs = self._resolve_di_kwargs(function, di_kwargs, kwargs)
        return function(*inject_args, **inject_kwargs)


DEFAULT_CONTAINER = PyCDIContainer()


class CDIDecorator(object):
    def __init__(self, _container=DEFAULT_CONTAINER):
        self.container = _container

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()


def prepare_injector_argument(arg, default_type, default_context):
    if isinstance(arg, type):
        return arg, default_context
    elif isinstance(arg, string_types):
        return default_type, arg
    elif isinstance(arg, tuple):
        return arg
    else:
        raise Exception()


class Inject(CDIDecorator):
    def __init__(self, *args, **kwargs):
        super(Inject, self).__init__(kwargs.pop('_container', DEFAULT_CONTAINER))
        self.context = kwargs.pop('_context', DEFAULT_CONTEXT)
        self.override = kwargs.pop('_override', False)
        self.name_as_context = kwargs.pop('_name_as_context', False)
        self.args = args
        self.kwargs = kwargs

    def __call__(self, to_inject):
        if isinstance(to_inject, type):
            annotations = getattr(to_inject.__init__, '__annotations__', {})
        else:
            annotations = getattr(to_inject, '__annotations__', {})
        parameters = dict(filter(lambda item: item[0] is not 'return', annotations.items()))
        inject_args = [] if self.override else list(getattr(to_inject, INJECT_ARGS, []))
        inject_args += [prepare_injector_argument(t, object, self.context, ) for t in self.args]
        inject_kwargs = {} if self.override else dict(getattr(to_inject, INJECT_KWARGS, {}))
        keys = set(parameters.keys()) | set(self.kwargs.keys())
        inject_kwargs.update(dict(
            [(k, prepare_injector_argument(
                self.kwargs.get(k, k if self.name_as_context else self.context),
                parameters.get(k, object),
                k if self.name_as_context else self.context)
              ) for k in keys]
        ))
        setattr(to_inject, INJECT_ARGS, inject_args)
        setattr(to_inject, INJECT_KWARGS, inject_kwargs)
        return to_inject


class Producer(CDIDecorator):
    def __init__(self, produce_type=None, _context=DEFAULT_CONTEXT, _container=DEFAULT_CONTAINER):
        super(Producer, self).__init__(_container)
        self.produce_type = produce_type
        self.context = _context

    def __call__(self, producer):
        annotations = getattr(producer, '__annotations__', {})
        produce_type = annotations.get('return', self.produce_type or object)
        self.container.register_producer(producer, produce_type, self.context)
        return producer
