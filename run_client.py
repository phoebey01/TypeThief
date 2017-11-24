# run_client

import argparse

import config
from typethief.client import Client


def parse_args():
    parser = argparse.ArgumentParser(description='Run TypeThief client')
    parser.add_argument(
        '-c',
        '--config',
        help='Configuration',
        default='prod',
    )
    parser.add_argument(
        '-i',
        '--ip',
        help='Server ip',
        default=None,
    )
    parser.add_argument(
        '-p',
        '--port',
        help='Server port',
        default=None,
    )

    args = parser.parse_args()
    if args.config not in config.CONFIGS:
        parser.error('"{}" is not a valid configuration'.format(args.config))
    conf = config.CONFIGS[args.config]
    if not args.ip:
        args.ip = conf.SERVER_ADDRESS
    if not args.port:
        args.port = conf.SERVER_PORT

    return args


def main():
    args = parse_args()
    cli = Client(args.ip, args.port)
    cli.run()


if __name__ == '__main__':
    main()