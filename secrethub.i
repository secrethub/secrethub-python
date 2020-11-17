%module secrethub

%{
#include "datetime.h"
PyObject *py_uuid = NULL;
PyObject *py_json = NULL;
%}

%init %{
    py_uuid = PyImport_ImportModule("uuid");
    py_json = PyImport_ImportModule("json");
    PyDateTime_IMPORT;
%}

%typemap (out) cgoTime CreatedAt {
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

%typemap(out) char* ResolveEnv {
    PyObject *json_loads = PyObject_GetAttrString(py_json, "loads");
    PyObject *str = PyUnicode_DecodeUTF8($1, strlen($1), NULL);
    $result = PyObject_CallFunctionObjArgs(json_loads, str, NULL);
    Py_DECREF(str);
}

%rename("%(undercase)s", %$ismember, %$not "match$name"="Client") "";

%include secrethub-xgo/secrethub.i

%pythoncode %{
import os

def export_env(self, env):
    for key, value in env.items():
        os.environ[key] = value
Client.export_env = export_env
%}
