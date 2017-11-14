# run_client

import argparse

import config
from typethief.client.gamewindow import GameWindow
from typethief.client.socketclient import SocketClient


ENVS = {
    'dev': config.DevelopmentConfig,
    'stage': config.StagingConfig,
    'prod': config.ProductionConfig,
    'test': config.TestingConfig,
}


def parse_args():
    parser = argparse.ArgumentParser(description='Run TypeThief client')
    parser.add_argument(
        '-c',
        '--config',
        help='Configuration',
        default='prod',
    )

    args = parser.parse_args()
    if args.config not in ENVS:
        parser.error('"{}" is not a valid configuration'.format(args.config))

    return args


def main():
    args = parse_args()
    conf = ENVS[args.config]
    sc = SocketClient(conf.SERVER_ADDRESS, conf.SERVER_PORT)
    gw = GameWindow()
    gw.run()


if __name__ == '__main__':
    main()