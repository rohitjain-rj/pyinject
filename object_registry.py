import functools
import os


instances = dict()
event_handlers = dict()
instances_to_register = []
event_handlers_to_register = dict()


class NamedType(object):
    def __init__(self, type, name=None):
        self.type = type
        self.name = name


def locate_instance(clazz):
    if isinstance(clazz, NamedType):
        lookup = (clazz.type, clazz.name)
    else:
        lookup = clazz
    return instances.get(lookup)


def register_instance(for_type=None, dependencies=None, arguments=None):
    def register(cls):
        instance_type = for_type
        if not instance_type:
            instance_type = cls
        instances_to_register.append((instance_type, cls, dependencies, arguments))
        return cls

    return register


def get_event_handler(event_type):
    return event_handlers.get(event_type)


def register_event_handler(event_type):
    def register(cls):
        event_handlers_to_register[event_type] = cls
        return cls

    return register


def finalize_object_graph():
    for instance_to_register in instances_to_register:
        instance_type, cls, dependencies, arguments = instance_to_register
        args = []
        if dependencies:
            for d in dependencies:
                args.append(locate_instance(d))

        if arguments:
            for arg in arguments:
                args.append(arg)

        instance = cls(*args)
        if isinstance(instance_type, NamedType):
            instances[(instance_type.type, instance_type.name)] = instance
        else:
            instances[instance_type] = instance

    for event_type, cls in event_handlers_to_register.items():
        event_handlers[event_type] = locate_instance(cls)


def inject(**services_to_inject):
    """
    :return:
    """

    def real_decorator(func):
        def wrapper(*args, **kwargs):
            """
            Wrapper
            :param args:
            :param kwargs:
            :return:
            """
            try:

                dependencies = dict()
                for service_name, service_class in services_to_inject.items():
                    dependencies[service_name] = locate_instance(service_class)
                r_val = func(*args, **kwargs, **dependencies)
                return r_val
            except Exception as e:
                raise e

        return functools.update_wrapper(wrapper, func)

    return real_decorator
