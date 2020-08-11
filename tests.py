import spi
import sys
import argparse
import simdjson
from datetime import datetime


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='integration test script')
    parser.add_argument('--log', type=int, help='logging threshold [0-4] (exception,info,warn,error,debug)', required=True)
    parser.add_argument('--username', help='username for socrates', required=True)
    parser.add_argument('--password', help='password for socrates', required=True)
    args = parser.parse_args()

    try:
        s = spi.Socrates(
            log_level=args.log,
            protocol='http',
            host='localhost',
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
            level=3,
            procedure='s.push_raw_data',
            input='test',
            message='failed to push raw data (str): ' + str(response)
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
            level=3,
            procedure='s.push_raw_data',
            input='test',
            message='failed to push raw data (list): ' + str(response)
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
            level=3,
            procedure='s.get_raw_data',
            input='test',
            message='failed to get raw data: ' + str(response)
        )
        sys.exit(1)

    status, response = s.get_iteration_set(name='triangle-nasdaq')
    if status is False:
        s.log(
            level=3,
            procedure='s.get_iteration_set',
            input='triangle-nasdaq',
            message='failed to get iteration set: ' + str(response)
        )
        sys.exit(1)

    status, response = s.get_unreviewed_index_records(module='scraper', name='triangle-nasdaq')
    if status is False:
        s.log(
            level=3,
            procedure='s.get_unreviewed_index_records',
            input='triangle-nasdaq',
            message='failed to get unreviewed index records: ' + str(response)
        )
        sys.exit(1)
    else:
        si_record = simdjson.loads(response['get_unreviewed_index_records'])[0]['_id']

    print('passed all tests')
    sys.exit(0)
