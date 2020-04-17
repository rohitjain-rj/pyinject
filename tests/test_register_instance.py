import abc
import pyinject
from pyinject import autoinject, autoargs


class MyInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def print_class_name(self):
        pass


@pyinject.register_instance(for_type=MyInterface)
class MyClass(MyInterface):
    def __init__(self):
        pass

    def print_class_name(self):
        print(self.__class__.__name__)


@pyinject.register_instance()
class ClassNamePrinter(object):
    @autoinject  # executed first, binds the dependencies with the init parameters
    @autoargs  # executed after init parameters are already binded, and sets the instance attributes, with same init
    # param name
    def __init__(self, class_to_print_name: MyInterface):
        pass

    def print_class_name(self):
        self.class_to_print_name.print_class_name()


def test_all_instances_registered():
    pyinject.finalize_object_graph()
    assert pyinject.locate_instance(ClassNamePrinter) is not None
    assert pyinject.locate_instance(MyInterface) is not None
    assert pyinject.locate_instance(MyClass) is None


def test_dependency_injected():
    @pyinject.register_instance()
    class TestClass(object):
        @autoinject
        @autoargs
        def __init__(self, class_to_print_name: MyInterface):
            pass

    pyinject.finalize_object_graph()
    my_class = pyinject.locate_instance(TestClass)

    assert isinstance(my_class.class_to_print_name, MyInterface)
