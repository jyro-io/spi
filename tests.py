import spi
import sys
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='integration test script')
    parser.add_argument('--log', type=int, help='logging threshold [0-4] (exception,info,warn,error,debug)', required=True)
    parser.add_argument('--protocol', help='[http,https]', required=True)
    parser.add_argument('--host', help='socrates', required=True)
    parser.add_argument('--no-verify', dest='no_verify', help='verify https', action='store_false')
    parser.add_argument('--username', help='username for socrates', required=True)
    parser.add_argument('--password', help='password for socrates', required=True)
    args = parser.parse_args()

    try:
        socrates = spi.Socrates(
            protocol=args.protocol,
            host=args.host,
            username=args.username,
            password=args.password,
            verify=args.no_verify
        )
    except spi.SocratesConnectError as err:
        spi.log(
            level=3,
            log_level=args.log,
            procedure='archimedes.scraper.run',
            input='test',
            message='failed to connect to socrates: ' + str(err)
        )
        sys.exit(1)

    status, response = socrates.get_thread_iteration_set(module='scraper', name='stocks-triangle-nasdaq')
    if status is False:
        spi.log(
            level=3,
            log_level=args.log,
            procedure='tests',
            input='test_input',
            message='failed to connect to socrates: ' + str(response)
        )
        sys.exit(1)

    print('passed all tests')
    sys.exit(0)
