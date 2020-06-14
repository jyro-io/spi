## SPI

This module provides a Python interface to the Socrates API.

### Install

#### Stable

```bash
pip install git+https://github.com/jyro-io/spi@0.1.6#egg=spi-0.1.6
```

#### Dev

```bash
pip install git+https://github.com/jyro-io/spi@master#egg=spi-dev
```

### Usage

```python
import spi
import sys

try:
    socrates = spi.Socrates(
        host='host',
        username='username',
        password='password',
        verify=True
    )
except spi.SocratesConnectError as err:
    print('failed to connect to socrates: ' + err)
    sys.exit(1)

status, response = spi.get_configuration_from_socrates(api='archimedes', key='classifier')
if status is False:
    spi.log(
        level=3,
        log_level=3,
        procedure='example.main',
        input=socrates.headers,
        message='failed to get config from socrates: ' + response
    )
    sys.exit(1)
config = response
```