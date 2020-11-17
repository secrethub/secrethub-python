%module SecretHub

%include secrethub-xgo/secrethub.i

%pythoncode %{
import os

def ExportEnv(self, env):
    for key, value in env.items():
        os.environ[key] = value
Client.ExportEnv = ExportEnv
%}
