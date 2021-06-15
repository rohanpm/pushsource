pushsource
==========
testin
A Python library for collecting content from various sources, used by
[release-engineering](https://github.com/release-engineering) publishing tools.

[![Build Status](https://travis-ci.org/release-engineering/pushsource.svg?branch=master)](https://travis-ci.org/release-engineering/pushsource)
[![Coverage Status](https://coveralls.io/repos/github/release-engineering/pushsource/badge.svg?branch=master)](https://coveralls.io/github/release-engineering/pushsource?branch=master)

- [Source](https://github.com/release-engineering/pushsource)
- [Documentation](https://release-engineering.github.io/pushsource/)
- [PyPI](https://pypi.org/project/pushsource)


Installation
------------

Install the `pushsource` package from PyPI.

```
pip install pushsource
```


Usage Example
-------------

```python
from pushsource import Source

# Get a source of content; sources and their parameters can be
# specified by URL. This source will use a couple of RPMs from
# Fedora koji as the content source.
source = Source.get('koji:https://koji.fedoraproject.org/kojihub?rpm=python3-3.7.5-2.fc31.x86_64.rpm,python3-3.7.5-2.fc31.src.rpm')

# Iterate over the content and do something with it:
for push_item in source:
    publish(push_item)
```

Development
-----------

Patches may be contributed via pull requests to
https://github.com/release-engineering/pushsource.

All changes must pass the automated test suite, along with various static
checks.

The [Black](https://black.readthedocs.io/) code style is enforced.
Enabling autoformatting via a pre-commit hook is recommended:

```
pip install -r requirements-dev.txt
pre-commit install
```

License
-------

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
