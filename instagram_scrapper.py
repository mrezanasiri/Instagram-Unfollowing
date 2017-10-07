# Calvin Lui
# Instagram List Scrapper
# Based on HTML Structure of Instagram's Website as of 10/5/2017

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass

def setup_account(driver):
    username = input("Username: ")
    password = getpass.getpass("Password: ")  # only works in terminal
    # password = input("Password:")
    print()

    print("Penetrating Website...")
    driver.get("https://www.instagram.com/accounts/login/")

    driver.find_element_by_xpath("//div/input[@name='username']").send_keys(username)
    driver.find_element_by_xpath("//div/input[@name='password']").send_keys(password)
    driver.find_element_by_xpath("//span/button").click()

    # (enable to) give time for two-step verification
    # time.sleep(30)

    # give time for web page to load
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "logged-in")))

    print("Ready to Scrape!")
    print()

    return username

def scrape_list(driver, list_name, username):
    print("Entering Account Page...")
    driver.get("https://www.instagram.com/" + username)

    print("Entering " + str.upper(list_name) + " List...")
    driver.find_element_by_partial_link_text(list_name).click()

    # give time for followers list to load
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "_gs38e")))

    xpath = "/html/body/div[4]"
    followHTML = driver.find_element_by_xpath(xpath)

    if list_name == "followers":
        spanPath = '//li[2]/a/span'
    else:
        spanPath = '//li[3]/a/span'

    followCount = int(driver.find_element_by_xpath(spanPath).text)
    print("Count:", followCount)

    # scroll to gain access to entire list
    followBox = driver.find_element_by_class_name("_gs38e")
    for i in range(int(followCount / 10)):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followBox)
        time.sleep(0.5)

    print("Scraping " + str.upper(list_name) + " List...")
    followHTML = followHTML.get_attribute('outerHTML')

    print("Done Collecting Information!")
    print()

    return str(followHTML)
