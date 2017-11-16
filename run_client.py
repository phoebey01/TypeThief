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

    args = parser.parse_args()
    if args.config not in config.CONFIGS:
        parser.error('"{}" is not a valid configuration'.format(args.config))

    return args


def main():
    args = parse_args()
    conf = config.CONFIGS[args.config]
    cli = Client(conf.SERVER_ADDRESS, conf.SERVER_PORT)
    cli.run()


if __name__ == '__main__':
    main()