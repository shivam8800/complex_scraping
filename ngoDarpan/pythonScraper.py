# Import newly installed selenium package
import csv
import threading
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import multiprocessing
from multiprocessing import Process

print("Number of cpu : ", multiprocessing.cpu_count())


def scraped_new_page(next_page):
    print("next page     ", next_page)
    # open up new chrome
    driver_two = webdriver.Chrome(
        executable_path="/usr/local/bin/chromedriver", options=options)
    # going to one link
    driver_two.get(next_page)

    def getNextUrl(previousUrl, pageNo):
        url_subelement_list = previousUrl.split("/")
        url_subelement_list = url_subelement_list[:-1]
        url_subelement_list.append(pageNo)
        return "/".join(url_subelement_list)

    paginated_urls = []

    try:
        last_page = driver_two.find_element_by_xpath(
            "/html/body/div[9]/div[1]/div[3]/div/div/div[2]/ul/li[14]/a").get_attribute('data-ci-pagination-page')
    except:
        html_list = driver_two.find_element_by_class_name('pagination')
        items = html_list.find_elements_by_tag_name("li")
        for item in items:
            text = item.text
            if text != "" and text != " " and text != ">":
                paginated_urls.append(getNextUrl(next_page, text))

    if len(paginated_urls) == 0:
        for j in range(1, int(last_page) + 1):
            paginated_urls.append(getNextUrl(
                next_page, str(j)))

    with open('ngoDarpan.csv', 'a') as csvfile:
        fieldnames = ['Ngo_name', 'City', "E_mail", "State",
                      "FCRA_Registration_no", "Mobile_No", "FCRA_Available", "Copy_of_Pan_Card", "Copy_of_Registration_Certificate", "State_of_Registration", "Operational_Area_District", "Type_of_NGO", "Address", "Act_name", "City_of_Registration", "Date_of_Registration", "Registration_No", "Telephone", "Key_Issues", "Registered_With", "Unique_Id", "Operational_Area_States", "Website_Url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # scraped all data of a link including paginated pages
        scraped_paginated_pages(paginated_urls, driver_two, writer)
        driver_two.close()


def scraped_paginated_pages(paginated_urls, driver_two, writer):
    for url in paginated_urls:

        # for opening new url
        driver_two.get(url)
        # sleep because we need to load full page
        sleep(5)
        # scraped all data of a paginated page
        scraped_one_paginated_page(driver_two, url, writer)


def scraped_one_paginated_page(driver_two, url, writer):
    for i in range(1, 11):
        # when page is loaded get the element
        try:
            clickable_link = driver_two.find_element_by_xpath(
                "/html/body/div[9]/div[1]/div[3]/div/div/div[2]/table/tbody/tr[" + str(i) + "]/td[2]/a")

            # click on that element
            clickable_link.click()

            # for opening modal we need to wait
            sleep(3)

            # getting all data which we require
            ngo_details = {
                "Ngo_name": driver_two.find_element_by_id('ngo_name_title').text,
                "Unique_Id": driver_two.find_element_by_xpath('//*[@id="UniqueID"]').text,
                "Registered_With": driver_two.find_element_by_xpath('//*[@id="reg_with"]').text,
                "Type_of_NGO": driver_two.find_element_by_xpath('//*[@id="ngo_type"]').text,
                "Registration_No": driver_two.find_element_by_xpath('//*[@id="ngo_regno"]').text,
                "Copy_of_Registration_Certificate": driver_two.find_element_by_xpath('//*[@id="rc_upload"]').text,
                "Copy_of_Pan_Card": driver_two.find_element_by_xpath('//*[@id="pc_upload"]').text,
                "Act_name": driver_two.find_element_by_xpath('//*[@id="ngo_act_name"]').text,
                "City_of_Registration": driver_two.find_element_by_xpath('//*[@id="ngo_city_p"]').text,
                "State_of_Registration": driver_two.find_element_by_xpath('//*[@id="ngo_state_p"]').text,
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
            # finally get all data of a ngo
            print(ngo_details, "    ", url)

            writer.writerow(ngo_details)
            # closing modal box
            closing_link = driver_two.find_element_by_xpath(
                '//*[@id="ngo_info_modal"]/div[2]/div/div[1]/button')
            closing_link.click()
            sleep(2)
        except:
            pass


if __name__ == "__main__":  # confirms that the code is under main function
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.

    driver = webdriver.Chrome(
        executable_path="/usr/local/bin/chromedriver", options=options)

    # going to url
    driver.get("https://ngodarpan.gov.in/index.php/home/statewise_membersPAV")

    # getting all links of second page
    second_links = [
        driver.find_element_by_xpath(
            '//*[@id="frm_griev"]/table[2]/tbody/tr[2]/td/table/tbody/tr[5]/td/ol/li['
            + str(i) + ']/a').get_attribute('href') for i in range(1, 37)
    ]

    procs = []
    proc = Process(
        target=scraped_new_page)  # instantiating without any argument
    procs.append(proc)
    proc.start()

    # instantiating process with arguments
    for next_page in second_links:
        # print(name)
        proc = Process(target=scraped_new_page, args=(next_page, ))
        procs.append(proc)
        proc.start()

    # complete the processes
    for proc in procs:
        proc.join()

    driver.close()