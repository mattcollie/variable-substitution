import os
import logging


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("I ran")
    logging.debug(f"ENV: {os.environ}")


if __name__ == '__main__':
    main()
