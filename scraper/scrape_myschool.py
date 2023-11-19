from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import undetected_chromedriver as uc


def scrape_my_school(page_url):
    options = uc.ChromeOptions()
    options.headless = False
    driver = uc.Chrome(use_subprocess=True, options=options)

    driver.get(page_url)
    wait = WebDriverWait(driver, 100)  # Explicit wait
    scholarships = []
    result = []

    try:
        scholarship_details = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'jet-listing-grid__item')))

        for detail in scholarship_details:
            try:
                element = detail.find_element(By.CLASS_NAME, 'elementor-heading-title')
                text = element.text
                link = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            except NoSuchElementException:
                text, link = 'Title Not Found', 'Link Not Found'

            try:
                deadline_element = detail.find_element(By.CLASS_NAME, 'jet-listing-dynamic-field__content')
                deadline_text = deadline_element.text
            except NoSuchElementException:
                deadline_text = 'Deadline Not Found'

            scholarships.append((text, link, deadline_text))

        # Visit each scholarship link
        for scholarship in scholarships:
            scholarship_url = scholarship[1]
            driver.get(scholarship_url)
            try:
                # Find and get the URL from the specified element
                education_link = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'a.elementor-button.elementor-button-link.elementor-size-md')))
                education_url = education_link.get_attribute('href')
                result.append((scholarship[0], scholarship[1], scholarship[2], education_url))
            except TimeoutException:
                result.append((scholarship[0], scholarship[1], scholarship[2], 'URL Not Found'))

    except TimeoutException:
        print("Timed out waiting for page to load")

    driver.quit()  # Don't forget to close the driver
    return result


# Test the function
print(scrape_my_school("https://myschoolscholarships.org/level-of-study/certificate/"))
