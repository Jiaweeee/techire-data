import sys
import logging
from data_processor.services import InfoExtractionService, JobIndexService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def print_usage():
    print("Usage: python -m data_processor.main [extract|index]")
    print("  extract  - Start the InfoExtractionService")
    print("  index    - Start the JobIndexService")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1].lower()
    
    if command == "extract":
        service = InfoExtractionService()
        logger.info("Starting InfoExtractionService...")
    elif command == "index":
        service = JobIndexService()
        logger.info("Starting JobIndexService...")
    else:
        logger.error(f"Error: Unknown command '{command}'")
        print_usage()
        sys.exit(1)

    service.run()