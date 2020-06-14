## SPI

This module provides a Python interface to the Socrates API.

### Install

```bash
pip install git+https://github.com/jyro-io/spi@0.1.0#egg=spi-0.1.0
```

### Usage

```python
import socrates_python_interface as spi
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