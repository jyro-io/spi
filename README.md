## Socrates for Python

### Install

#### Stable

```bash
pip install git+https://github.com/jyro-io/spi@0.4.1#egg=spi-0.4.1
```

#### Dev

```bash
pip install git+https://github.com/jyro-io/spi.git@master#egg=spi-dev
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
    print('failed to connect to socrates: ' + str(err))
    sys.exit(1)

status, response = socrates.get_configuration(api='archimedes', key='some_config_key')
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

status, response = socrates.get_definition(api='archimedes', module='datasource', name='some_datasource_name')
if status is True:
    dd = response
    status, response = spi.connect_to_mongo(
        host=dd['host'],
        username=dd['username'],
        password=dd['password'],
        database=dd['database']
    )
    if status is True:
        ds = response
        ds['database']['collection'].find({})
```

See [tests.py](tests.py) for more examples.