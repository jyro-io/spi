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