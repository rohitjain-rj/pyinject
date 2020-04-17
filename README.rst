This project provides support for dependency injection for Python projects.

Usage:

* Use ``@pyinject.object_registry.register_instance()`` class level decorator, to register an instance of a class. You can pass the ``for_type`` for interface, which this class implements. All dependencies and fixed arguments can be passed in ``dependencies`` and ``arguments`` parameters respectively.

* If you're registering multiple class, against same interface, you can pass ``pyinject.object_registry.NamedType`` to ``for_type`` argument, by giving specific name to this class implementation, along with interface name.

* On a function, use ``@pyinject.object_registry.inject`` decorator, to inject specific type of dependency.

* Also, in order to fetch the registered instance at any point in the code, you can use ``pyinject.object_registry.locate_instance()`` function, by passing required interface name, or ``NamedType``, if you're implementing multiple classes for a given interface.


E.g.:


.. code-block:: python

    @abc.abstractclass
    class MyInterface(object):
        @abc.abstractmethod
        def print_class_name(self):
            pass

    @register_instance(for_type=MyInterface)
    class MyClass(MyInterface):
        def __init__(self):
            pass

        def print_class_name(self):
            print(self.__class__.__name__)

    @register_instance(dependencies=[MyInterface])
    class ClassNamePrinter(object):
        def __init__(self, class_to_print_name):
            class_to_print_name.print_class_name()

        def print_class_name(self):
            self.class_to_print_name.print_class_name()


    object_registry.finalize_object_graph()

    object_registry.locate_instance(ClassNamePrinter).print_class_name()

