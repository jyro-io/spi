import spi
import sys
import argparse


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
            verify=False
        )
    except spi.SocratesConnectError as err:
        print('failed to connect to socrates: ' + str(err))
        sys.exit(1)

    status, response = s.get_raw_data(
        name='stocks-nasdaq-intraday',
        key='TSLA',
        start="2020-03-16T08:00:00",
        end="2020-03-20T16:00:00"
    )
    if status is False:
        s.log(
            level=3,
            procedure='tests',
            input='test_input',
            message='failed to get raw data: ' + str(response)
        )
        sys.exit(1)

    status, response = s.get_thread_iteration_set(name='stocks-triangle-nasdaq')
    if status is False:
        s.log(
            level=3,
            procedure='tests',
            input='test_input',
            message='failed to get thread iteration set: ' + str(response)
        )
        sys.exit(1)

    status, response = s.get_unreviewed_index_records(module='scraper', name='stocks-triangle-nasdaq')
    if status is False:
        s.log(
            level=3,
            procedure='tests',
            input='test_input',
            message='failed to get unreviewed index records: ' + str(response)
        )
        sys.exit(1)
    else:
        si_record = response[0]['_id']

    print('passed all tests')
    sys.exit(0)
