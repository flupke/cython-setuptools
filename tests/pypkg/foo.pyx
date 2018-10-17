cdef extern from "foo.h":
    int foo()


def bar():
    print foo()
