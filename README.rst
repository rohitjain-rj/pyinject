This project provides support for dependency injection for Python projects.

Usage:

* Use ``@pyinject.register_instance()`` class level decorator, to register an instance of a class. You can pass the ``for_type`` for interface, which this class implements.

* Use ``@pyinject.autoinject`` decorator on ``__init__`` function, to inject dependencies, based on type annotation

* If you're registering multiple class, against same interface, you can pass ``pyinject.NamedType`` to ``for_type`` argument, by giving specific name to this class implementation, along with interface name.

* On a function, use ``@pyinject.object_registry.inject`` decorator, to inject specific type of dependency.

* Also, in order to fetch the registered instance at any point in the code, you can use ``pyinject.locate_instance()`` function, by passing required interface name, or ``@pyinject.NamedType``, if you're implementing multiple classes for a given interface.


E.g.:


.. code-block:: python

    @abc.abstractclass
    class MyInterface(object):
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
        @autoinject
        def __init__(self, class_to_print_name: MyInterface):
            class_to_print_name.print_class_name()

        def print_class_name(self):
            self.class_to_print_name.print_class_name()


    pyinject.finalize_object_graph()

    pyinject.locate_instance(ClassNamePrinter).print_class_name()

