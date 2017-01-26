from .core import DEFAULT_CONTAINER, DEFAULT_CONTEXT


def new(clazz, context=DEFAULT_CONTEXT):
    return DEFAULT_CONTAINER.produce(clazz, context)


def call(function, *args, **kwargs):
    return DEFAULT_CONTAINER.call(function, *args, **kwargs)
