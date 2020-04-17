import abc
from pyinject import object_registry

class MyInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def print_class_name(self):
        pass

@object_registry.register_instance(for_type=MyInterface)
class MyClass(MyInterface):
    def __init__(self):
        pass

    def print_class_name(self):
        print(self.__class__.__name__)

@object_registry.register_instance(dependencies=[MyInterface])
class ClassNamePrinter(object):
    def __init__(self, class_to_print_name):
        self.class_to_print_name = class_to_print_name

    def print_class_name(self):
        self.class_to_print_name.print_class_name()


def test_all_instances_registered():
    object_registry.finalize_object_graph()
    assert object_registry.locate_instance(ClassNamePrinter) is not None
    assert object_registry.locate_instance(MyInterface) is not None
    assert object_registry.locate_instance(MyClass) is None

def test_dependency_injected():
    @object_registry.register_instance(dependencies=[MyInterface])
    class TestClass(object):
        def __init__(self, class_to_print_name):
            self.class_to_print_name = class_to_print_name

    object_registry.finalize_object_graph()
    my_class = object_registry.locate_instance(TestClass)

    assert isinstance(my_class.class_to_print_name, MyInterface)

