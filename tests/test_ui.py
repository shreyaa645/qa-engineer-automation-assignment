import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.iamdave.ai"


@pytest.fixture(scope="function")
def driver():
    """Setup and teardown for Chrome WebDriver per test function."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")

    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.implicitly_wait(5)

    yield browser

    # Teardown
    browser.quit()


class TestIamDaveUI:
    """Automated UI test suite for www.iamdave.ai."""

    def test_homepage_loads_and_title_verified(self, driver):
        """TC01: Verify homepage loads successfully with expected title and brand logo."""
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 15)

        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        assert "Dave" in driver.title, f"Unexpected page title: {driver.title}"

        logo = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "header img, nav img, a[href*='iamdave'] img"))
        )
        assert logo.is_displayed(), "Brand logo is not visible on the homepage."

    def test_homepage_hero_heading_and_cta_presence(self, driver):
        """TC02: Verify primary hero heading (H1) and interactive CTA button exist."""
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 15)

        hero_heading = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
        assert len(hero_heading.text.strip()) > 0, "Hero H1 heading text is empty."

        cta_elements = driver.find_elements(By.CSS_SELECTOR, "a[href], button")
        visible_ctas = [el for el in cta_elements if el.is_displayed()]
        assert len(visible_ctas) > 0, "No visible interactive buttons or links found on homepage."

    def test_navigation_flow_to_subpage(self, driver):
        """TC03: Test clicking a navigation link and verifying URL/content transition."""
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 15)

        initial_url = driver.current_url

        nav_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "header a[href], nav a[href]")))
        target_link = None
        for link in nav_links:
            href = link.get_attribute("href") or ""
            if link.is_displayed() and "iamdave.ai" in href and href.rstrip("/") != initial_url.rstrip("/"):
                target_link = link
                break

        assert target_link is not None, "No internal navigation link found in header."

        driver.execute_script("arguments[0].click();", target_link)
        wait.until(EC.url_changes(initial_url))

        assert driver.current_url != initial_url, "URL did not change after clicking navigation link."
        assert "iamdave.ai" in driver.current_url

    def test_input_field_or_contact_form_interaction(self, driver):
        """TC04: Locate an input field (e.g., email/contact/newsletter) and verify user text entry."""
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 15)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='email'], input[type='text'], textarea")
        visible_inputs = [inp for inp in inputs if inp.is_displayed() and inp.is_enabled()]

        if not visible_inputs:
            contact_links = driver.find_elements(
                By.XPATH, "//a[contains(translate(., 'CONTACTDEMO', 'contactdemo'), 'contact') or contains(translate(., 'CONTACTDEMO', 'contactdemo'), 'demo')]"
            )
            for link in contact_links:
                if link.is_displayed():
                    driver.execute_script("arguments[0].click();", link)
                    break

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input, textarea")))
            inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='email'], input[type='text'], textarea")
            visible_inputs = [inp for inp in inputs if inp.is_displayed() and inp.is_enabled()]

        assert len(visible_inputs) > 0, "No interactive input field found on homepage or contact page."

        sample_input = visible_inputs[0]
        test_value = "qa.test@example.com" if sample_input.get_attribute("type") == "email" else "QA Automation Test"
        sample_input.clear()
        sample_input.send_keys(test_value)

        assert sample_input.get_attribute("value") == test_value, "Input field did not retain typed value."