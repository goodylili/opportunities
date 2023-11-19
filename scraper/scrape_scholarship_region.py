from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import undetected_chromedriver as uc
from utils.logger import log_error
from utils.utilities import retryable_get


def scrape_scholarship_region(sr_page_url):
    options = uc.ChromeOptions()
    options.headless = False
    driver_instance = uc.Chrome(use_subprocess=True, options=options)
    wait = WebDriverWait(driver_instance, 10)  # Adjusted wait time to a more reasonable duration

    driver_instance.get(sr_page_url)

    scholarships = []
    results = []
    try:
        scholarship_openings = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '.tdb_module_loop.td_module_wrap.td-animation-stack.td-cpt-post')))
        for scholarship in scholarship_openings:
            title = scholarship.find_element(By.CLASS_NAME, 'entry-title').text
            page_url = scholarship.find_element(By.CLASS_NAME, 'entry-title').find_element(By.TAG_NAME,
                                                                                           'a').get_attribute('href')
            scholarships.append((title, page_url))

        for title, page_url in scholarships:
            try:
                retryable_get(driver_instance, page_url, title)

                try:
                    deadline_text = wait.until(
                        EC.presence_of_element_located((By.XPATH, "//h4[contains(text(), 'Deadline')]"))).text
                    original_scholarship = wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, '.elementor-button.elementor-button-link.elementor-size-md')))
                    original_scholarship_url = original_scholarship.get_attribute('href')

                    results.append((title, original_scholarship_url, deadline_text))
                except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
                    log_error(e, f"Couldn't find the required elements for {title}")

            except Exception as e:
                log_error(e, f"Retry failed for {title}")

    except Exception as e:
        log_error(e, "Error occurred while fetching scholarship listings")
    finally:
        driver_instance.quit()

    return results
