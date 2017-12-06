# run_client

import argparse

import config
from typethief.client import Client


def parse_args():
    parser = argparse.ArgumentParser(description='Run TypeThief client')
    parser.add_argument(
        '--config',
        help='Configuration',
        default='prod',
    )
    parser.add_argument(
        '--host',
        help='Server host',
        default=None,
    )
    parser.add_argument(
        '--port',
        help='Server port',
        default=None,
    )

    args = parser.parse_args()
    if args.config not in config.CONFIGS:
        parser.error('"{}" is not a valid configuration'.format(args.config))
    conf = config.CONFIGS[args.config]
    if not args.host:
        args.host = conf.SERVER_HOST
    if not args.port:
        args.port = conf.SERVER_PORT

    return args


def main():
    args = parse_args()
    cli = Client(args.host, args.port)
    cli.run()


if __name__ == '__main__':
    main()