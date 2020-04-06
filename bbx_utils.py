from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


def switch_frame(driver, mother_menu, child_menu, frame_name):

    driver.switch_to.default_content()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, mother_menu)))
    driver.find_element_by_css_selector(child_menu).click()
    WebDriverWait(driver, 5).until(
        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, frame_name)))


def getOriAdd(sep, index, source):

    lists = source.split(sep)
    return lists[index]