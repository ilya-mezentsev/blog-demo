from dataclasses import dataclass

import argparse


__all__ = [
    'cli_arguments',
]


@dataclass
class CLIArgs:
    config_path: str
    logging_level: str


def cli_arguments() -> CLIArgs:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--config-path',
        type=str,
        help='Path to config file',
    )

    parser.add_argument(
        '--logging-level',
        type=str,
        help='Logging level',
    )

    args = parser.parse_args()

    return CLIArgs(
        config_path=args.config_path,
        logging_level=args.logging_level,
    )
