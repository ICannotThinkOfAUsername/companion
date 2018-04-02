from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException #perhaps I should just import them all?

try_to_reconnect = True

url_file_location = 'C:/ge/url.txt'
session_file_location = 'C:/ge/session.txt'
chrome_driver_location = 'C:/ge/chromedriver.exe'

global driver

def save_browser_info():
    global driver  # not technically needed but I feel like it might help readability.. *shrugs*

    url_file = open(url_file_location, 'w')
    url_file.write(driver.command_executor._url)
    url_file.close()

    session_file = open(session_file_location, 'w')
    session_file.write(driver.session_id)
    session_file.close()

def setup_browser():
    global driver

    if try_to_reconnect:
        try:
            url_file = open(url_file_location)
            old_url = url_file.read()
            # print(old_url)
            url_file.close()
        except:
            old_url = ''

        try:
            session_file = open(session_file_location)
            old_session_id = session_file.read()
            # print(old_session_id)
            session_file.close()
        except:
            old_session_id = ''

        create_new_browser = False

        if (old_session_id == '') or (old_url == ''):
            # print('at least one file is empty so we are creating a new browser')
            create_new_browser = True
        else:
            # print('both files have data so we are going to try to connect to an existing browser with that data')
            try:
                driver = webdriver.Remote(command_executor=old_url, desired_capabilities={})
                driver.close()
                driver.session_id = old_session_id
            except:
                # print('failed to connect to an old browser so we are creating a new browser')
                create_new_browser = True

        if create_new_browser:
            driver = webdriver.Chrome(executable_path=chrome_driver_location)
    else:
        driver = webdriver.Chrome(executable_path=chrome_driver_location)

def list_css_selector_i(selector_part_1, selector_part_2, max_num=8):
    '''
    loops through range(1, max_num + 1) adding str(i) inbetween the selector parts, & testing if the result of that is found as an element
    Each i found is added to a list, the list is eventually returned as the result of this method
    example output: [2, 3]
    example output: []
    '''
    result = list()

    for i in range(1, max_num + 1):
        try:
            css_selector = selector_part_1 + str(i) + selector_part_2
            elem = driver.find_element_by_css_selector(css_selector)
            result.append(i)
        except NoSuchElementException:
            pass

    return result