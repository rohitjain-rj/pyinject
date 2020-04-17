from .named_type import NamedType

instances = dict()
instances_to_register = []


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


