#include <Python.h>

// Simple C function that just returns "Hello from C!"
static PyObject* hello(PyObject* self, PyObject* args) {
    return PyUnicode_FromString("Hello from C!");
}

// Method definition
static PyMethodDef module_methods[] = {
    {"hello", hello, METH_NOARGS, "Returns a greeting from C"},
    {NULL, NULL, 0, NULL}
};

// Module definition
static struct PyModuleDef module_definition = {
    PyModuleDef_HEAD_INIT,
    "dummy_c_module",
    "A dummy C extension module",
    -1,
    module_methods
};

// Module initialization
PyMODINIT_FUNC PyInit_dummy_c_module(void) {
    return PyModule_Create(&module_definition);
}