from retrying import retry
from utils.logger import logger


@retry(stop_max_attempt_number=3, wait_fixed=2000)
def retryable_get(driver, url, title):
    driver.get(url)
    if '#google_vignette' in driver.current_url:
        logger.warning(f"Detected ad overlay on {title}, retrying...")
        raise Exception("Ad overlay detected")
