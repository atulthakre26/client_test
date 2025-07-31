import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Fixture to launch and quit browser
@pytest.fixture(scope="function")
def setup():
    driver = webdriver.Chrome()
    driver.get("https://client.aceint.ai/auth/signin")
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)
    yield driver, wait
    driver.quit()

# Reusable function to sign in
def sign_in(driver, wait, email, password):
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/form/div[1]/input"))).send_keys(email)
    driver.find_element(By.XPATH, "/html/body/div/div/div/form/div[2]/div[1]/input").send_keys(password)
    driver.find_element(By.XPATH, "/html/body/div/div/div/form/button").click()
    wait.until(EC.url_contains("client.aceint.ai"))

# Test 1: Login validation
def test_valid_signin(setup):
    """Test login with valid email and password"""
    driver, wait = setup
    sign_in(driver, wait, "atulthakre511@gmail.com", "987654321")
    assert "AceInt" in driver.title

# Test 2: Open Positions UI validation
def test_open_positions_ui(setup):
    """Test the presence of 'Open Positions' and UI elements after login"""
    driver, wait = setup
    sign_in(driver, wait, "atulthakre511@gmail.com", "987654321")

    heading = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Open Positions')]")))
    assert heading.is_displayed()

    apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Apply']")))
    assert apply_button.is_displayed()

# Test 3: Apply flow (Upload resume, agree terms, start interview)
def test_apply_button_click(setup):
    """Test the full apply process including upload, agreement, and starting interview"""
    driver, wait = setup
    sign_in(driver, wait, "atulthakre511@gmail.com", "987654321")

    # Click the Apply button
    apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Apply']")))
    apply_button.click()

    # Upload Resume (assuming input[type='file'] is used)
    upload_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
    upload_input.send_keys(r"C:\Users\HP\Downloads\Jaishri_Resume...pdf")  # Change path to your local resume

    # Agree to Terms
    
    agree_checkbox_label = wait.until(EC.element_to_be_clickable((
    By.XPATH, "/html/body/div[3]/div[2]/form/div[2]/div/div/label/button"
    )))
    agree_checkbox_label.click()  # will toggle the checkbox
    time.sleep(3)




    # Click Start Interview
    start_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Start Interview')]")))
    start_button.click()

    # Final Assertion (URL or modal opened)
    assert "interview" in driver.current_url or "round" in driver.page_source.lower()
