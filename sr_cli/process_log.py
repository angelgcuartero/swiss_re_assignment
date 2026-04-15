import logging
import os

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__ )


def process_log_files(
    input_files, output_file, calculate_mfip=False, calculate_lfip=False, calculate_eps=False, calculate_bytes=False
):
    # Placeholder for the actual implementation of log file processing
    log.info("Hello from swiss-re-assignment!")
    for file in input_files:
        log.debug(f"Input file: {file}")
    log.debug(f"Output file: {output_file}")
    log.debug(f"Most frequent IP flag: {calculate_mfip}")
    log.debug(f"Least frequent IP flag: {calculate_lfip}")
    log.debug(f"Events per second flag: {calculate_eps}")
    log.debug(f"Total bytes exchanged flag: {calculate_bytes}")
