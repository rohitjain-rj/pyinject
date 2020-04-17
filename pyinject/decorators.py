import functools
import inspect
import types
from inspect import Parameter
from typing import get_type_hints

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


def autoinject(init):
    f = init
    bindings = infer_bindings(f)

    @functools.wraps(init)
    def wrapper(self, *args):
        dependencies = {}
        for binding, type in bindings.items():
            dependencies[binding] = locate_instance(type)

        init(self, *args, **dependencies)

    return wrapper


def infer_bindings(callable):
    spec = inspect.getfullargspec(callable)
    bindings = get_type_hints(callable)
    bindings.pop('return', None)
    if isinstance(callable, types.MethodType):
        self_name = spec.args[0]
        bindings.pop(self_name, None)
    return bindings


def autoargs(init):
    """
    Ref: https://stackoverflow.com/questions/3652851/what-is-the-best-way-to-do-automatic-attribute-assignment-in-python-and-is-it-a

    :param init:
    :return:
    """
    sig = inspect.signature(init)

    @functools.wraps(init)
    def wrapper(self, *args, **kwargs):
        values = sig.bind(self, *args, **kwargs)

        for k, p in sig.parameters.items():
            if k == 'self':
                continue

            if k in values.arguments:
                val = values.arguments[k]
                if p.kind in (Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY):
                    setattr(self, k, val)
                elif p.kind == Parameter.VAR_KEYWORD:
                    for k, v in values.arguments[k].items():
                        setattr(self, k, v)
            else:
                setattr(self, k, p.default)

        return init(self, *args, **kwargs)

    return wrapper


def populate_self(self):
    """
    Ref: https://stackoverflow.com/questions/28443527/python-decorator-to-automatically-define-init-variables

    Function to set instance attributes automatically using arguments passed to `__init__`.
    From __init__, call it like:

        populate_self(self)

    :param self:
    :return:
    """
    frame = inspect.getouterframes(inspect.currentframe())[1][0]
    for k, v in frame.f_locals.items():
        if k != 'self':
            setattr(self, k, v)
