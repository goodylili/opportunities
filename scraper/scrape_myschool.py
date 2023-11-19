from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from utils.logger import log_error
from utils.utilities import retryable_get
from scraper.scraper import initialize_webdriver


# Setting up logging


def scrape_my_school(ms_page_url):
    driver_instance = initialize_webdriver()

    retryable_get(driver_instance, ms_page_url, "Main Scholarship Page")

    wait = WebDriverWait(driver_instance, 10)  # Explicit wait

    scholarships = []
    results = []

    try:
        scholarship_details = wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'jet-listing-grid__item')))

        for detail in scholarship_details:
            try:
                element = detail.find_element(By.CLASS_NAME, 'elementor-heading-title')
                title = element.text
                scholarship_page_url = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
                deadline_element = detail.find_element(By.CLASS_NAME, 'jet-listing-dynamic-field__content')
                deadline_text = deadline_element.text
                print(title, scholarship_page_url, deadline_text)
            except NoSuchElementException:
                title, scholarship_page_url, deadline_text = 'Title Not Found', 'Link Not Found', 'Deadline Not Found'

            scholarships.append((title, scholarship_page_url, deadline_text))
    except TimeoutException as e:
        log_error(e, "Timed out waiting for page to load")

    for title, scholarship_page_url, deadline_text in scholarships:
        # Check if the scholarship_page_url is a valid URL
        if not scholarship_page_url or not scholarship_page_url.startswith("http"):
            print(f"Invalid URL for {title}: {scholarship_page_url}")
            continue
        retryable_get(driver_instance, scholarship_page_url, title)

        try:
            link_element = wait.until(ec.presence_of_element_located((
                By.XPATH, "//span[contains(text(), 'Apply For This Scholarship')]/ancestor::a"
            )))
            application_link_url = link_element.get_attribute('href')
            print(title, application_link_url, deadline_text)
            results.append((title, application_link_url, deadline_text))
            # Removed the break statement to allow the loop to continue
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
            log_error(e, f"Couldn't find the required elements for {title}.")

    driver_instance.quit()
    return results


# Test the function
print(scrape_my_school("https://myschoolscholarships.org/level-of-study/masters/"))
