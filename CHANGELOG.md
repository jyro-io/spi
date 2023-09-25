### 3.5.4

* refactor api parameter

### 3.5.0

* add get_longest_metric_period()

### 3.4.0

* add get_predictive_model()

### 3.3.0

* add get_ohlc_interval()

### 3.2.0

* mongodb

### 3.1.3

* mongodb replicaset connection

### 3.1.2

* update test defaults
* cleanup

### 3.1.1

* 4 -> 2 spaces

### 3.1.0

* updating get_raw_data() interface

### 3.0.0

* improved error handling
* removing self.log()

### 2.1.0

* removing retry logic

### 2.0.5

* bugfix: TypeError: log() takes 0 positional arguments but 1 was given

### 2.0.4

* removing app field from logging

### 2.0.3

* removing hostname emission in self.log

### 2.0.2

* host -> node

### 2.0.1

* fixed bug in self.get_unreviewed_index_records

### 2.0.0

* changed logging interface and implementation
* fixing various problems
* fixing tests

### 1.15.0

* adding logging

### 1.14.0

* adding level field to logging
* adding app field to logging

### 1.13.0

* removing level field from logging
* adding JSON dump to detail field

### 1.12.0

* updating log() interface

### 1.11.3

* fixing requirement pytprint package metadata problem

### 1.11.2

* adding urllib3, pysimdjson to setup.py dependencies

### 1.11.1

* adding urllib3 to imports :(

### 1.11.0

* adding urllib3.exceptions.MaxRetryError to try catch

### 1.10.0

* updating get_unreviewed_index_records endpoint to scrapeindex

### 1.9.0

* implementing retry mechanisms

### 1.8.0

* changing get_iteration_set interface to request against the `socrates.archimedes.datasource` module

### 1.6.1

* updating tests to match new socrates behavior

### 1.6.0

* changing `[UNDEFINED]` tag to an empty string `''`

### 1.4.1

* bumping version to match Socrates API, since this spi is the test interface

### 0.4.1

* bugfix: spi.get_iteration_set was not working correctly

### 0.4.0

* Added CHANGELOG.md
* Added spi.push_raw_data()