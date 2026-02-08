"""Entry-point module for agenticai-foundations-to-advanced."""

import logging

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the program.

    Log an informational message via the logging system.
    """
    logger.info("Hello from agenticai-foundations-to-advanced!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
