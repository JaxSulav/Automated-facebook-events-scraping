import csv
import urllib.request
import re
import os
#import shutil
import argparse
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import date
from pandas.tseries.offsets import MonthEnd
from multiprocessing import Pool


def make_image_directory():
    images_path = './Output/' + images_folder_name
    os.makedirs(images_path)
    return

###################### link fetching functions ################################

def auto_login():
    browser.find_element_by_id("email").send_keys('wabalabadubdub18@gmail.com')
    browser.find_element_by_id("pass").send_keys('rickc137')
    browser.find_element_by_id("loginbutton").click()
    return


def scroll_to_page_end():
    global browser
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(5)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    return


def fetch_page_links():
    i = 1
    while True:
        try:
            link_path = '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div/div/div[2]/ul/li[' + str(
                i) + ']/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[1]/a'

            page = browser.find_element_by_xpath(link_path)
            link_url = page.get_attribute('href')[0:48]
            print("loop:  " + str(i))
            i = i + 1
            print("Fetching event: " + page.text)
            queueList.append(link_url)
            print("queue length: " + str(len(queueList)))
        except:
            break
    return


def fetch_links_from_each_city():
    bhaktapur_button = browser.find_element_by_xpath("//*[text()='Bhaktapur, Nepal']")
    bhaktapur_button.click()
    scroll_to_page_end()
    fetch_page_links()

    kathmandu_button = browser.find_element_by_xpath("//*[text()='Kathmandu, Nepal']")
    kathmandu_button.click()
    scroll_to_page_end()
    fetch_page_links()

    lalitpur_button = browser.find_element_by_xpath("//*[text()='Lalitpur, Nepal']")
    lalitpur_button.click()
    scroll_to_page_end()
    fetch_page_links()

    return

###################### link collecting function ################################

def links_collection():
    global browser
    print("Working in background..........................")
    print("This may take some time depending on the internet consistency")

    for single_date in daterange:
        event_date = single_date.strftime("%Y-%m-%d")

        link = 'https://www.facebook.com/events/discovery/?suggestion_token=%7B%22city%22%3A%22205246402885806%22%2C%22time%22%3A%22%7B%5C%22start%5C%22%3A%5C%22' + str(
            event_date) + '%5C%22%2C%5C%22end%5C%22%3A%5C%22' + str(
            event_date) + '%5C%22%7D%22%2C%22timezone%22%3A%22Asia%2FKathmandu%22%7D&acontext=%7B%22ref%22%3A110%2C%22ref_dashboard_filter%22%3A%22upcoming%22%2C%22source%22%3A2%2C%22source_dashboard_filter%22%3A%22discovery%22%2C%22action_history%22%3A%22[%7B%5C%22surface%5C%22%3A%5C%22dashboard%5C%22%2C%5C%22mechanism%5C%22%3A%5C%22main_list%5C%22%2C%5C%22extra_data%5C%22%3A%7B%5C%22dashboard_filter%5C%22%3A%5C%22upcoming%5C%22%7D%7D%2C%7B%5C%22surface%5C%22%3A%5C%22discover_filter_list%5C%22%2C%5C%22mechanism%5C%22%3A%5C%22surface%5C%22%2C%5C%22extra_data%5C%22%3A%7B%5C%22dashboard_filter%5C%22%3A%5C%22discovery%5C%22%7D%7D%2C%7B%5C%22surface%5C%22%3A%5C%22discover_filter_list%5C%22%2C%5C%22mechanism%5C%22%3A%5C%22surface%5C%22%2C%5C%22extra_data%5C%22%3A%7B%5C%22dashboard_filter%5C%22%3A%5C%22discovery%5C%22%7D%7D%2C%7B%5C%22surface%5C%22%3A%5C%22discover_filter_list%5C%22%2C%5C%22mechanism%5C%22%3A%5C%22surface%5C%22%2C%5C%22extra_data%5C%22%3A%7B%5C%22dashboard_filter%5C%22%3A%5C%22discovery%5C%22%7D%7D%2C%7B%5C%22surface%5C%22%3A%5C%22discover_filter_list%5C%22%2C%5C%22mechanism%5C%22%3A%5C%22surface%5C%22%2C%5C%22extra_data%5C%22%3A%7B%5C%22dashboard_filter%5C%22%3A%5C%22discovery%5C%22%7D%7D%2C%7B%5C%22surface%5C%22%3A%5C%22discover_filter_list%5C%22%2C%5C%22mechanism%5C%22%3A%5C%22surface%5C%22%2C%5C%22extra_data%5C%22%3A%7B%5C%22dashboard_filter%5C%22%3A%5C%22discovery%5C%22%7D%7D%2C%7B%5C%22surface%5C%22%3A%5C%22discover_filter_list%5C%22%2C%5C%22mechanism%5C%22%3A%5C%22surface%5C%22%2C%5C%22extra_data%5C%22%3A%7B%5C%22dashboard_filter%5C%22%3A%5C%22discovery%5C%22%7D%7D%2C%7B%5C%22surface%5C%22%3A%5C%22discover_filter_list%5C%22%2C%5C%22mechanism%5C%22%3A%5C%22surface%5C%22%2C%5C%22extra_data%5C%22%3A%7B%5C%22dashboard_filter%5C%22%3A%5C%22discovery%5C%22%7D%7D%2C%7B%5C%22surface%5C%22%3A%5C%22discover_filter_list%5C%22%2C%5C%22mechanism%5C%22%3A%5C%22surface%5C%22%2C%5C%22extra_data%5C%22%3A%7B%5C%22dashboard_filter%5C%22%3A%5C%22discovery%5C%22%7D%7D]%22%2C%22has_source%22%3Atrue%7D'
        options = Options()
        options.set_preference("dom.webnotifications.enabled", False)  # eliminating popup notification
        if args.visible:
            pass
        else:
            print("RUNNING IN BACKGROUND")
            options.add_argument('-headless')
        browser = webdriver.Firefox(options=options)
        browser.get(link)
        auto_login()

        # browser.implicitly_wait(10)
        fetch_links_from_each_city()

        browser.quit()
    return


############################ scraping functions ################################


def get_date():
    global soup, e_year_span, e_date
    # get year
    try:
        e_year_span = browser.find_element_by_xpath('//*[@id="title_subtitle"]/span')
        e_year = e_year_span.get_attribute('aria-label')[-4:]
    except:
        e_year = str(provided_year)

    # get month
    try:
        e_month = soup.find('span', attrs={'class': '_5a4-'}).text
    except:
        month_fetch = browser.find_element_by_xpath(
            '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div/div[1]/div[2]/div[3]/div/div[2]/div/div[1]/div/div[1]').text
        e_month = month_fetch[month_fetch.index(','):8]

    # get day
    try:
        e_day = soup.find('span', attrs={'class': '_5a4z'}).text
    except:
        date_fetch = browser.find_element_by_xpath(
            '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div/div[1]/div[2]/div[3]/div/div[2]/div/div[1]/div/div[1]').text
        e_day = date_fetch[-2:]

    e_date = e_year + " " + e_month + " " + e_day
    return


def get_location():
    global e_location
    try:
        e_location = browser.find_element_by_xpath(
            '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[3]/div/div/div[2]/div/ul/li[2]/div[1]/table/tbody/tr/td[2]/div/div[1]/div/div[2]/div').text
    except:
        try:
            e_location = browser.find_element_by_xpath(
                '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div/div[2]/div/ul/li[2]/div[1]/table/tbody/tr/td[2]/div/div[1]/div/div[2]/div').text
        except:
            try:
                e_location = browser.find_element_by_xpath(
                    '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div/div[2]/div/ul/li[2]/a/table/tbody/tr/td[2]/div/div/div[2]/div/div').text
            except:
                e_location = "n/a"
                # print("n/a.. " + current_link)
    return


def get_weekday():
    try:
        global e_year_span, e_weekday
        dum_list = e_year_span.get_attribute('aria-label')
        e_weekday = e_year_span.get_attribute('aria-label')[0:dum_list.index(',')]
    except:
        e_weekday = "n/a"
    return


def get_people():
    global e_people
    try:
        e_people = browser.find_element_by_class_name('_5z74').text
    except:
        e_people = "n/a"
        pass
    return


def get_host():
    global e_host
    try:
        e_host_sel = browser.find_element_by_xpath(
            '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[3]/div/div/div[1]/div[2]/div[1]/div/div/div/div/div')
        e_host = e_host_sel.get_attribute('content')
    except:
        e_host_sel = soup.find_all('a', attrs={'href': re.compile("^https://")})
        e_host = e_host_sel[2].text
    return


def get_event_name():
    global e_name
    e_name = soup.find('h1', {'id': 'seo_h1_tag'}).text


def get_time():
    global e_time
    e_time = browser.find_element_by_class_name('_2ycp').text
    return


###################### crawling function ################################


def crawl_links(current_link):
    with open(csv_path, 'a+', newline='') as f:  # opens the events-(timestamo).csv files in append mode
        global geckodriver, csv_writer1, soup, browser
        csv_writer1 = csv.writer(f)
        options = webdriver.FirefoxOptions()
        if args.visible:
            pass
        else:
            print("RUNNING IN BACKGROUND")
            options.add_argument('-headless')
        browser = webdriver.Firefox(executable_path=geckodriver, options=options)
        try:
            print("crawling on: " + current_link)
                # using selenium
            browser.get(current_link)
            r = urllib.request.urlopen(current_link).read()
                # using beautifulsoup
            soup = BeautifulSoup(r, 'lxml')

            get_event_name()
            get_date()
            get_location()
            get_weekday()
            get_time()
            get_people()
            get_event_name()
            get_host()

            write_in_csv()
            #print("writting in CSV........")
            save_image()
            browser.quit()
            #print(".....Done")

        except:
            browser.quit()  # if the links are not found in a page, close the browser while passing

    return

##################### write in csv function ################################

def write_in_csv():
    global csv_writer1, e_date, e_weekday, e_name, e_host, e_location, e_time, e_people
    csv_writer1.writerow(
        [e_date, e_weekday, e_name, e_host, e_location, e_time,
         e_people])
    return

#################### save image function ################################


def save_image():
    try:
        if soup.find('img', attrs={'class': 'scaledImageFitWidth'}):
            image = soup.find('img', attrs={'class': 'scaledImageFitWidth'})
        else:
            image = soup.find('img', attrs={'class': 'scaledImageFitHeight'})

        img = image['src']

        create_img = open(os.path.join(image_path, e_name + ".jpeg"), 'wb')
        create_img.write(urllib.request.urlopen(img).read())
        create_img.close()
    except Exception as exc:
        pass
        print(exc)
    return

####################################################################################################### START #########################################################################################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year")
    parser.add_argument("--month")
    parser.add_argument("--visible", action="store_true")


queueList = [] #queuing links
geckodriver = './geckodriver'  # firefox driver
args = parser.parse_args()
provided_year = int(args.year)
provided_month= int(args.month)

start_date = date(provided_year, provided_month, 1)
end_date = start_date + MonthEnd(0)
daterange = pd.date_range(start_date, end_date)

timestamp = str(time.time())

images_folder_name = 'Images_collected - ' + timestamp
image_path = './Output/' + images_folder_name
csv_name = 'events ' + timestamp + '.csv'
csv_path = './Output/' + csv_name

make_image_directory()
links_collection()

queueSet = set(queueList)  # convert queue list to set
# queueSetList = list(queueSet)
print("Number of links in set: " + str(len(queueSet)))

with open(csv_path, 'w', newline='') as e:  # creates events-(timestamp).csv in write mode
    csv_writer = csv.writer(e)
    csv_writer.writerow(['Date', 'Day', 'Event Name', 'Host', 'Location', 'Time', 'Interested/Going'])  # write first row
    print("initiating Scraping..........................................................")
    p = Pool(6)  # creates pool of n process at a time
    p.map(crawl_links, queueSet)  # maps the function crawl_links with queueSet argument
    # p.terminate()
    # p.join()

print("Congratulations!! events stored in " + str(csv_name) + " file in your script's directory")
print("Images can be found in " + images_folder_name + " in your script's directory :)")
