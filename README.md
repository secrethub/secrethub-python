<hr/>
<p align="center">
  <sub><img src="https://1password.com/img/logo-v1.svg" alt="1Password" width="20" /></sub> <b>SecretHub has joined 1Password!</b> Find out more on the <a href="https://secrethub.io/blog/secrethub-joins-1password/">SecretHub blog</a>. 🎉
</p>
<hr/>

# SecretHub Client for Python <sup>[BETA](#beta)</a></sup>

This repository provides a Python client for the SecretHub Secrets Management API. 

> [SecretHub](https://secrethub.io) is a secrets management tool that works for every engineer and allows you to securely provision passwords and keys throughout your entire stack with just a few lines of code.

## Table of Contents
 - [Installation](#installation)
 - [Usage](#usage)
 - [Getting help](#getting-help)
 - [BETA](#beta)
 - [Developing](#developing)

## Installation

To install the SecretHub package from PyPi, run the following command:

```bash
python -m pip install secrethub
```

The package supports Linux, Windows (32 and 64 bit) and MacOS.
It is built for CPython versions 3.5 and above.

Make sure you have created a SecretHub account and set up a credential on your system before using the library. See the [Credential](#credential) section for more info. 

> Note that passphrase protected credentials are not supported by the Python client.

## Usage
Before doing any calls to the library, you need to import the `secrethub` package and create a client:
```python
import secrethub
client = secrethub.Client()
```

After you have your client, you can call the following methods:

### `read_string(path)`
Retrieve a secret value as a string.
```python
secret = client.read_string("path/to/secret")
```

### `read(path)`
Retrieve a secret, including all its metadata.
```python
secret = client.read("path/to/secret");
```
The returned object is of the `secrethub.SecretVersion` type and it represents a version of a secret with the sensitive value stored in the `data` field.
It provides the following fields:
  - secret_version_id
  - secret
  - version
  - data
  - created_at
  - status

### `exists(path)`
Check if a secret exists at `path`.
```python
secret_exists = client.exists("path/to/secret")
```

### `write(path, secret)`
Write a secret value to a given `path`.
```python
client.write("path/to/secret", "secret_value")
```

### `remove(path)`
Delete the secret found at `path`.
```python
client.remove("path/to/secret")
```

### `resolve(ref)`
Resolve a secret reference tag of the format `secrethub://<path>` and return the corresponding secret value. If `ref` is not a valid reference tag, it returns otherwise it returns `ref` unchanged.
```python
resolved_ref = client.resolve("secrethub://path/to/secret")
```

### `resolve_env()`
Return a dictionary containing the OS environment with all secret references (`secrethub://<path>`) replaced by their corresponding secret values.

#### Example

```python
os.environ['MY_SECRET'] = 'secrethub://path/to/secret'
os.environ['OTHER_VARIABLE'] = 'some other value'

resolved_env = client.resolve_env()

print(resolved_env)
# Prints all environment variables with any secret references resolved to their corresponding value
# {
#    'MY_SECRET': 'the value of the secret stored at path/to/secret',
#    'OTHER_VARIABLE': 'some other value'
# }

```

### `export_env(env)`
Adds the environment variables defined in the `env` dictionary to the environment of the process.
If any of them are already present in the environment, they will be overwritten.

This method can be used together with `resolve_env` to resolve all environment variables with secret references and set them to their corresponding secret value. Note that we recommend you use `client.resolve_env()` for most cases, but if your code reads its configuration from the environment and cannot be adapted to use the result of `client.resolve_env()` directly you can use it together with `export_env()`. 

#### Example

```python
os.environ['MY_SECRET'] = 'secrethub://path/to/secret'

client.export_env(client.resolve_env());

print("secret: " + os.environ['MY_SECRET']);
# Prints the value of the secret stored at path/to/secret.
```

### Exceptions
Any error encountered by the SecretHub client will be thrown as a `RuntimeError` with the full error message as an associated string value.
```python
try:
    client.read('path/to/secret')
except Exception as e:
    print(e)
```

### Credential
To use the SecretHub Python client, you need to provide a credential for your __SecretHub__ account.
You can sign up for a free developer account [here](https://signup.secrethub.io/).

After signup, the credential is located at `$HOME/.secrethub/credential` by default.
`secrethub.Client()` automatically uses this credential.

You can also provide a credential through the `SECRETHUB_CREDENTIAL` environment variable.

## Getting Help

Come chat with us on [Discord](https://discord.gg/EQcE87s) or email us at [support@secrethub.io](mailto:support@secrethub.io)

## BETA
This project is currently in beta and we'd love your feedback! Check out the [issues](https://github.com/secrethub/secrethub-python/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) and feel free suggest cool ideas, use cases, or improvements.

Because it's still in beta, you can expect to see some changes introduced. Pull requests are very welcome.

For support, send us a message on [Discord](https://discord.gg/wcxV5RD) or send an email to support@secrethub.io

## Developing

Note that most of the code in this repository is automatically generated from the [SecretHub XGO project](https://github.com/secrethub/secrethub-xgo), which wraps the `secrethub-go` client with `cgo` exported functions so it can be called form other languages, e.g. C, C#, Python, Ruby, NodeJS, and Java. To generate the code [SWIG](http://www.swig.org/) is used. 

See the [SecretHub XGO repository](https://github.com/secrethub/secrethub-xgo) for more details.
