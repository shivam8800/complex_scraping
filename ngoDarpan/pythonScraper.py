# Import newly installed selenium package
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from time import sleep


# Now create an 'instance' of driver
# with downloaded  webdriver path
driver = webdriver.Chrome(
    executable_path="/usr/local/bin/chromedriver")
# A new Chrome (or other browser) window should open up

# going to url
driver.get("https://ngodarpan.gov.in/index.php/home/statewise_membersPAV")

# getting all links of second page
second_links = [driver.find_element_by_xpath(
    '//*[@id="frm_griev"]/table[2]/tbody/tr[2]/td/table/tbody/tr[5]/td/ol/li[' + str(i) + ']/a').get_attribute('href') for i in range(1, 37)]


# open up new chrome
driver_two = webdriver.Chrome(
    executable_path="/usr/local/bin/chromedriver")

# going to one link
driver_two.get(second_links[0])

# sleep because we need to load full page
sleep(5)


for i in range(1, 11):
    # when page is loaded get the element
    clickable_link = driver_two.find_element_by_xpath(
        "/html/body/div[9]/div[1]/div[3]/div/div/div[2]/table/tbody/tr[" + str(i) + "]/td[2]/a")

    # click on that element
    clickable_link.click()

    # for opening modal we need to wait
    sleep(3)

    # getting all data which we require
    ngo_details = {
        "Unique_Id": driver_two.find_element_by_xpath('//*[@id="UniqueID"]').text,
        "Registered_With": driver_two.find_element_by_xpath('//*[@id="reg_with"]').text,
        "Type_of_NGO": driver_two.find_element_by_xpath('//*[@id="ngo_type"]').text,
        "Registration_No": driver_two.find_element_by_xpath('//*[@id="ngo_regno"]').text,
        "Copy_of_Registration_Certificate": driver_two.find_element_by_xpath('//*[@id="rc_upload"]').text,
        "Copy_of_Pan_Card": driver_two.find_element_by_xpath('//*[@id="pc_upload"]').text,
        "Act_name": driver_two.find_element_by_xpath('//*[@id="ngo_act_name"]').text,
        "City_of_Registration": driver_two.find_element_by_xpath('//*[@id="ngo_city_p"]').text,
        "State of Registration": driver_two.find_element_by_xpath('//*[@id="ngo_state_p"]').text,
        "Date_of_Registration": driver_two.find_element_by_xpath('//*[@id="ngo_reg_date"]').text,
        "Key_Issues": driver_two.find_element_by_xpath('//*[@id="key_issues"]').text,
        "Operational_Area_States": driver_two.find_element_by_xpath('//*[@id="operational_states"]').text,
        "Operational_Area_District": driver_two.find_element_by_xpath('//*[@id="operational_district"]').text,
        "FCRA_Available": driver_two.find_element_by_xpath('//*[@id="FCRA_details"]').text,
        "FCRA_Registration_no": driver_two.find_element_by_xpath('//*[@id="FCRA_reg_no"]').text,
        "Address": driver_two.find_element_by_xpath('//*[@id="address"]').text,
        "City": driver_two.find_element_by_xpath('//*[@id="city"]').text,
        "State": driver_two.find_element_by_xpath('//*[@id="state_p_ngo"]').text,
        "Telephone": driver_two.find_element_by_xpath('//*[@id="phone_n"]').text,
        "Mobile_No": driver_two.find_element_by_xpath('//*[@id="mobile_n"]').text,
        "Website_Url": driver_two.find_element_by_xpath('//*[@id="ngo_web_url"]').text,
        "E_mail": driver_two.find_element_by_xpath('//*[@id="email_n"]').text
    }

    # for getting all data successfully we need to wait
    sleep(3)
    print " --------  "
    # finally get all data of a ngo
    print ngo_details

    # closing modal box
    closing_link = driver_two.find_element_by_xpath(
        '//*[@id="ngo_info_modal"]/div[2]/div/div[1]/button')
    closing_link.click()
    # sleep again
    sleep(2)
