import functools

from .object_registry import locate_instance


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
