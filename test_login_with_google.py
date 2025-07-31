import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="function")
def setup():
    driver = webdriver.Chrome()
    driver.get("https://client.aceint.ai/auth/signin")  # Change to your login URL
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)
    yield driver, wait
    driver.quit()


def test_google_login(setup):
    driver, wait = setup

    # Click on "Login with Google" button
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Google')]"))).click()

    # Switch to Google login window
    time.sleep(2)
    main_window = driver.current_window_handle
    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            break

    # Google Login Page
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))).send_keys("atulbootcoding26@gmail.com")
    driver.find_element(By.XPATH, "//*[@id='identifierNext']").click()

    # wait.until(EC.presence_of_element_located((By.NAME, "Passwd"))).send_keys("Bootcoding12!@")
    # driver.find_element(By.ID, "passwordNext").click()

    password_input = wait.until(EC.element_to_be_clickable((By.NAME, "Passwd")))
    password_input.clear()
    password_input.send_keys("Bootcoding12!@")


    # Wait and switch back to main window
    time.sleep(5)
    driver.switch_to.window(main_window)

    # Assert login success (customize according to your app dashboard)
    assert "dashboard" in driver.current_url.lower()
