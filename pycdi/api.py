from __future__ import annotations

from dataclasses import dataclass
from typing import Type

DEFAULT_CONTEXT = 'default'
INJECT_ARGS = '_inject_args'
INJECT_KWARGS = '_inject_kwargs'
INJECT_RETURN = '_inject_return'


@dataclass
class InjectionPoint(object):
    member: any = None
    name: str = None
    type: Type = object
    context: str = DEFAULT_CONTEXT
    multiple: bool = False

    @classmethod
    def make(cls, member=None, name=None, type: Type = object, context=DEFAULT_CONTEXT):
        multiple = isinstance(type, (tuple, list,))
        type = first(type) if multiple else type
        return cls(member, name, type, context, multiple)


class CDIContainer(object):
    def register_instance(self, instance, product_type=None, context=DEFAULT_CONTEXT, priority=None):
        raise NotImplementedError()

    def register_producer(self, producer, produce_type=object, context=DEFAULT_CONTEXT, priority=None):
        raise NotImplementedError()

    def get_producer(self, produce_type: Type = object, context=DEFAULT_CONTEXT):
        raise NotImplementedError()

    def get_producers(self, produce_type: Type = object, context=DEFAULT_CONTEXT):
        raise NotImplementedError()

    def sub_container(self, *args, **kwargs):
        raise NotImplementedError()

    def resolve(self, injection_point: InjectionPoint):
        raise NotImplementedError()

    def produce(self, produce_type, context=DEFAULT_CONTEXT):
        raise NotImplementedError()

    def call(self, function, *args, **kwargs):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()


def first(it):
    return it[0]


def last(it):
    return it[-1]