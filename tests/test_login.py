import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture()
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


def test_successful_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")

    driver.find_element(By.ID, "username").send_keys("tomsmith")

    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    flash_message = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.success"))
    )

    assert "You logged into a secure area!" in flash_message.text

    logout_button = driver.find_element(By.CSS_SELECTOR, "a.button.secondary.radius")
    assert logout_button.is_displayed(), "Кнопка Logout не отображается"
