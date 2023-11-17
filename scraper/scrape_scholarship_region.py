from scraper.scraper import initialize_webdriver
from selenium.webdriver.common.by import By


def scrape_undergrad():
    driver_instance = initialize_webdriver()
    scholarship_openings = driver_instance.find_elements(By.CSS_SELECTOR, '.tdb_module_loop.td_module_wrap.td-animation-stack.td-cpt-post')
    for scholarship in scholarship_openings:
        scholarship_title_element = scholarship.find_element(By.CLASS_NAME, 'entry-title')
        scholarship_title = scholarship_title_element.text

        # Find the <a> tag within the title element and get its href attribute
        scholarship_link_element = scholarship_title_element.find_element(By.TAG_NAME, 'a')
        scholarship_page_url = scholarship_link_element.get_attribute('href')

        print(scholarship_title, scholarship_page_url)

    driver_instance.quit()