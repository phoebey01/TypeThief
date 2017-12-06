# run_server.py

import argparse

from config import CONFIGS
from typethief.server import Server


def parse_args():
    parser = argparse.ArgumentParser(description='Typethief server')
    parser.add_argument(
        '--config',
        help='Configuration',
        default='prod',
    )
    parser.add_argument(
        '--host',
        help='Server host address',
        default=None,
    )
    parser.add_argument(
        '--port',
        help='Server port address',
        type=int,
        default=None,
    )

    args = parser.parse_args()
    if args.config not in CONFIGS:
        parser.error('--config must be test, dev, stage, or prod')
    return args


def main():
    args = parse_args()
    srv = Server(CONFIGS[args.config], host=args.host, port=args.port)
    srv.run()


if __name__ == '__main__':
    main()
