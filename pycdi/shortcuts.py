from typing import Type, Callable

from pycdi.api import DEFAULT_CONTEXT
from .core import DEFAULT_CONTAINER


def new(clazz: Type, context: str = DEFAULT_CONTEXT):
    return DEFAULT_CONTAINER.produce(clazz, context)


def call(function: Callable, *args, **kwargs):
    return DEFAULT_CONTAINER.call(function, *args, **kwargs)
