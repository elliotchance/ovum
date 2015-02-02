# ovum

Package Manager for Python.

`ovum` uses the *every repository is a package* mantra and works with PyPI and any GitHub repository without the need for those developers to define their module explicitly.

Modules are managed locally (inside your package) and so every package can have totally different requirements.

It is based off PHP's [composer](https://getcomposer.org).

Installation
------------

...

TL;DR (Quick Start)
-------------------

* Require a package (this is the same thing from PyPI or GitHub):

```
ovum require pypi:1pass
ovum require github:georgebrock/1pass
```

Some packages are only required for development (not production):

```
ovum require-dev pypi:mock
```

You may also specify versions:

```
ovum require pypi:1pass ">=0.2" # minimum version
ovum require pypi:1pass 0.1.7   # exact (not recommended)
```

* Install all your dependencies:

```
ovum install
```

* Use it!

```
# always need this first
import ovum

# packages from GitHub use vendor prefix
from georgebrock.1pass.onepassword import Keychain

# PyPI packages can still be used the old fasioned way
from onepassword import Keychain
```

Dependencies
------------

### Adding Dependencies

Your application/module dependencies are managed in a `ovum.yml` file:

```
require:
- math
require-dev:
- mock: >1
```

### Installing/Updating Dependencies

```
ovum install
```

From time to time you will want to update your dependencies:

```
ovum update
```