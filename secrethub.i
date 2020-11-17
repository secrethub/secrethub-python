%module SecretHub

%{
#include "datetime.h"
PyObject *py_uuid = NULL;
%}

%init %{
    py_uuid = PyImport_ImportModule("uuid");
%}

%typemap (out) cgoTime CreatedAt {
    PyDateTime_IMPORT;
    double doubleValue = (int)$1;
    PyObject *floatObj = PyFloat_FromDouble(doubleValue);
    PyObject *timeTuple = Py_BuildValue("(O)", floatObj);
    $result = PyDateTime_FromTimestamp(timeTuple);
}

%typemap(out) uuid {
    PyObject *uuid_ctor = PyObject_GetAttrString(py_uuid, "UUID");
    PyObject *str = PyUnicode_DecodeUTF8($1, strlen($1), NULL);
    $result = PyObject_CallFunctionObjArgs(uuid_ctor, str, NULL);
    Py_DECREF(str);
}

%include secrethub-xgo/secrethub.i

%pythoncode %{
import os

def ExportEnv(self, env):
    for key, value in env.items():
        os.environ[key] = value
Client.ExportEnv = ExportEnv
%}
