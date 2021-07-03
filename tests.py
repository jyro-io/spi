import spi
import sys
import argparse
import simdjson
from datetime import datetime


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='integration test script')
    parser.add_argument('--protocol', help='http/s', default='http')
    parser.add_argument('--host', help='host for socrates', default='localhost')
    parser.add_argument('--username', help='username for socrates', required=True)
    parser.add_argument('--password', help='password for socrates', required=True)
    args = parser.parse_args()

    try:
        s = spi.Socrates(
            protocol=args.protocol,
            host=args.host,
            username=args.username,
            password=args.password,
            verify=False,
            timeout=5
        )
    except spi.SocratesConnectError as err:
        print('failed to connect to socrates: ' + str(err))
        sys.exit(1)

    timestamp_format = '%Y-%m-%d %H:%M:%S.%f'

    push_before = datetime.now()
    status, response = s.push_raw_data(
        name='test',
        records=simdjson.dumps([
            {
                "test_key": "integration",
                "timestamp": datetime.now().strftime(timestamp_format)
            }
        ])
    )
    if status is False:
        s.log(
            level='ERROR',
            app='test',
            procedure='s.push_raw_data',
            detail=response,
            message='failed to push raw data (str)'
        )
        sys.exit(1)
    status, response = s.push_raw_data(
        name='test',
        records=[
            {
                "test_key": "integration",
                "timestamp": datetime.now().strftime(timestamp_format)
            }
        ]
    )
    if status is False:
        s.log(
            level='ERROR',
            app='test',
            procedure='s.push_raw_data',
            detail=response,
            message='failed to push raw data (list)'
        )
        sys.exit(1)
    push_after = datetime.now()

    status, response = s.get_raw_data(
        name='test',
        key='integration',
        start=push_before.strftime(timestamp_format),
        end=push_after.strftime(timestamp_format)
    )
    if status is False:
        s.log(
            level='ERROR',
            app='test',
            procedure='s.get_raw_data',
            detail=response,
            message='failed to get raw data'
        )
        sys.exit(1)

    status, response = s.get_iteration_set(name='test')
    if status is False:
        s.log(
            level='ERROR',
            app='test',
            procedure='s.get_iteration_set',
            detail=response,
            message='failed to get iteration set'
        )
        sys.exit(1)

    status, response = s.get_unreviewed_index_records(module='scraper', name='test')
    if status is False:
        s.log(
            level='ERROR',
            app='test',
            procedure='s.get_unreviewed_index_records',
            detail=response,
            message='failed to get unreviewed index records'
        )
        sys.exit(1)
    else:
        si_record = simdjson.loads(response['get_unreviewed_index_records'])[0]['_id']

    print('passed all tests')
    sys.exit(0)
