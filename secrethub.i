%module SecretHub

%{
#include "datetime.h"
%}

%typemap (varin) cgoTime {}

%typemap (out) cgoTime CreatedAt {
    PyDateTime_IMPORT;
    double doubleValue = (int)$1;
    PyObject *floatObj = PyFloat_FromDouble(doubleValue);
    PyObject *timeTuple = Py_BuildValue("(O)", floatObj);
    $result = PyDateTime_FromTimestamp(timeTuple);
}

%include secrethub-xgo/secrethub.i

%pythoncode %{
import os

def ExportEnv(self, env):
    for key, value in env.items():
        os.environ[key] = value
Client.ExportEnv = ExportEnv
%}
