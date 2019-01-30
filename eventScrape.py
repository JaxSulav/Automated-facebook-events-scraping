import csv
import urllib.request
import re
import os
import shutil
import argparse
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import date
from pandas.tseries.offsets import MonthEnd
from multiprocessing import Pool


def links_gather():

    print("Working in background..........................")
    print("This may take some time depending on the internet consistency")
    for single_date in daterange:
        date = single_date.strftime("%Y-%m-%d")

        link = 'https://www.facebook.com/events/discovery/?suggestion_token=%7B%22city%22%3A%22205246402885806%22%2C%22time%22%3A%22%7B%5C%22start%5C%22%3A%5C%22' + str(
            date) + '%5C%22%2C%5C%22end%5C%22%3A%5C%22' + str(
            date) + '%5C%22%7D%22%2C%22timezone%22%3A%22Asia%2FKathmandu%22%7D&acontext=%7B%22ref%22%3A110%2C%22ref_dashboard_filter%22%3A%22upcoming%22%2C%22source%22%3A2%2C%22source_dashboard_filter%22%3A%22discovery%22%2C%22action_history%22%3A%22[%7B%5C%22surface%5C%22%3A%5C%22dashboard%5C%22%2C%5C%22mechanism%5C%22%3A%5C%22main_list%5C%22%2C%5C%22extra_data%5C%22%3A%7B%5C%22dashboard_filter%5C%22%3A%5C%22upcoming%5C%22%7D%7D%2C%7B%5C%22surface%5C%22%3A%5C%22discover_filter_list%5C%22%2C%5C%22mechanism%5C%22%3A%5C%22surface%5C%22%2C%5C%22extra_data%5C%22%3A%7B%5C%22dashboard_filter%5C%22%3A%5C%22discovery%5C%22%7D%7D%2C%7B%5C%22surface%5C%22%3A%5C%22discover_filter_list%5C%22%2C%5C%22mechanism%5C%22%3A%5C%22surface%5C%22%2C%5C%22extra_data%5C%22%3A%7B%5C%22dashboard_filter%5C%22%3A%5C%22discovery%5C%22%7D%7D%2C%7B%5C%22surface%5C%22%3A%5C%22discover_filter_list%5C%22%2C%5C%22mechanism%5C%22%3A%5C%22surface%5C%22%2C%5C%22extra_data%5C%22%3A%7B%5C%22dashboard_filter%5C%22%3A%5C%22discovery%5C%22%7D%7D%2C%7B%5C%22surface%5C%22%3A%5C%22discover_filter_list%5C%22%2C%5C%22mechanism%5C%22%3A%5C%22surface%5C%22%2C%5C%22extra_data%5C%22%3A%7B%5C%22dashboard_filter%5C%22%3A%5C%22discovery%5C%22%7D%7D%2C%7B%5C%22surface%5C%22%3A%5C%22discover_filter_list%5C%22%2C%5C%22mechanism%5C%22%3A%5C%22surface%5C%22%2C%5C%22extra_data%5C%22%3A%7B%5C%22dashboard_filter%5C%22%3A%5C%22discovery%5C%22%7D%7D%2C%7B%5C%22surface%5C%22%3A%5C%22discover_filter_list%5C%22%2C%5C%22mechanism%5C%22%3A%5C%22surface%5C%22%2C%5C%22extra_data%5C%22%3A%7B%5C%22dashboard_filter%5C%22%3A%5C%22discovery%5C%22%7D%7D%2C%7B%5C%22surface%5C%22%3A%5C%22discover_filter_list%5C%22%2C%5C%22mechanism%5C%22%3A%5C%22surface%5C%22%2C%5C%22extra_data%5C%22%3A%7B%5C%22dashboard_filter%5C%22%3A%5C%22discovery%5C%22%7D%7D%2C%7B%5C%22surface%5C%22%3A%5C%22discover_filter_list%5C%22%2C%5C%22mechanism%5C%22%3A%5C%22surface%5C%22%2C%5C%22extra_data%5C%22%3A%7B%5C%22dashboard_filter%5C%22%3A%5C%22discovery%5C%22%7D%7D]%22%2C%22has_source%22%3Atrue%7D'
        options = Options()
        options.set_preference("dom.webnotifications.enabled", False)
        options.add_argument('-headless')
        browser = webdriver.Firefox(options=options)
        browser.get(link)
        browser.find_element_by_id("email").send_keys('wabalabadubdub18@gmail.com')
        browser.find_element_by_id("pass").send_keys('rickc137')
        browser.find_element_by_id("loginbutton").click()

        def fetch():
            i = 1
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

            while True:

                try:
                    path = '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div/div/div[2]/ul/li[' + str(
                        i) + ']/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[1]/a'

                    page = browser.find_element_by_xpath(path)
                    link = page.get_attribute('href')[0:48]

                    print("loop:  " + str(i))
                    i = i + 1
                    print("Fetching event: " + page.text)
                    queue.append(link)
                    print("queue length: " + str(len(queue)))
                except:
                    break
            return

        # browser.implicitly_wait(10)
        a = browser.find_element_by_xpath("//*[text()='Bhaktapur, Nepal']")
        a.click()
        fetch()

        a = browser.find_element_by_xpath("//*[text()='Kathmandu, Nepal']")
        a.click()
        fetch()

        a = browser.find_element_by_xpath("//*[text()='Lalitpur, Nepal']")
        a.click()
        fetch()
        browser.quit()
    return

def crawl_links(s1):

    with open('events.csv', 'a+', newline='') as f:
        csv_writer1 = csv.writer(f)
        options.add_argument('-headless')
        browser = webdriver.Firefox(executable_path=geckodriver, options=options)
        try:
            print("crawling on: " + s1)

            # using selenium
            browser.get(s1)

            try:
                e_y = browser.find_element_by_xpath('//*[@id="title_subtitle"]/span')
                e_year = e_y.get_attribute('aria-label')[-4:]
            except:
                e_year = str(y)

            try:
                e_location = browser.find_element_by_xpath(
                    '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[3]/div/div/div[2]/div/ul/li[2]/div[1]/table/tbody/tr/td[2]/div/div[1]/div/div[2]/div').text
            except:
                try:
                    e_location = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div/div[2]/div/ul/li[2]/div[1]/table/tbody/tr/td[2]/div/div[1]/div/div[2]/div').text
                except:
                    try:
                        e_location = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div/div[2]/div/ul/li[2]/a/table/tbody/tr/td[2]/div/div/div[2]/div/div').text
                    except:
                        e_location = "n/a"
                        print("n/a.. " + s1)

            # using beautifulsoup and requests

            r = urllib.request.urlopen(s1).read()

            soup = BeautifulSoup(r, 'lxml')

            try:
                e_month = soup.find('span', attrs={'class': '_5a4-'}).text
            except:
                monthFetch = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div/div[1]/div[2]/div[3]/div/div[2]/div/div[1]/div/div[1]').text
                e_month = monthFetch[monthFetch.index(','):8]

            try:
                dum_list = e_y.get_attribute('aria-label')
                e_weekday = e_y.get_attribute('aria-label')[0:dum_list.index(',')]
            except:
                e_weekday = "n/a"

            e_time = browser.find_element_by_class_name('_2ycp').text
            try:
                e_people = browser.find_element_by_class_name('_5z74').text
            except:
                e_people = "n/a"
                pass

            e_name = soup.find('h1', {'id': 'seo_h1_tag'}).text

            try:
                e_date = soup.find('span', attrs={'class': '_5a4z'}).text
            except:
                dateFetch = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div/div[1]/div[2]/div[3]/div/div[2]/div/div[1]/div/div[1]').text
                e_date = dateFetch[-2:]

            try:
                e_host_sel = browser.find_element_by_xpath(
                    '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[3]/div/div/div[1]/div[2]/div[1]/div/div/div/div/div')
                e_host = e_host_sel.get_attribute('content')
            except:
                e_host_sel = soup.find_all('a', attrs={'href': re.compile("^https://")})
                e_host = e_host_sel[2].text

            csv_writer1.writerow(
                [e_year + " " + e_month + " " + e_date, e_weekday, e_name, e_host, e_location, e_time,
                 e_people])

            #print("writting in CSV........")

            try:
                if soup.find('img', attrs={'class': 'scaledImageFitWidth'}):
                    image = soup.find('img', attrs={'class': 'scaledImageFitWidth'})
                else:
                    image = soup.find('img', attrs={'class': 'scaledImageFitHeight'})

                img = image['src']

                create_img = open(os.path.join('Images_collected', e_name + ".jpeg"), 'wb')
                create_img.write(urllib.request.urlopen(img).read())
                create_img.close()
            except Exception as exc:
                print(exc)

            browser.quit()
            #print(".....Done")

        except:
            browser.quit()  # if the links are not found in a page, close the browser while passing

    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year")
    parser.add_argument("--month")
args = parser.parse_args()

y = int(args.year)
m = int(args.month)

a = date(y, m, 1)
b = a + MonthEnd(0)
daterange = pd.date_range(a, b)

os.system('chmod +x ./geckodriver')
geckodriver = './geckodriver'  # firefox driver
options = webdriver.FirefoxOptions()

if os.path.exists('Images_collected'):
    shutil.rmtree('./Images_collected')
    os.makedirs('Images_collected')
else:
    os.makedirs('Images_collected')

queue = [] #queuing links
links_gather()
queueSet = set(queue)
queueSetList = list(queueSet)
print("Number of links in set: " + str(len(queueSet)))

with open('events.csv', 'w', newline='') as e:
    csv_writer = csv.writer(e)
    csv_writer.writerow(['Date', 'Day', 'Event Name', 'Host', 'Time', 'Interested/Going'])
    j = 1
    print("initiating Scraping..........................................................")
    p = Pool(6)
    p.map(crawl_links, queueSetList)
    # p.terminate()
    # p.join()

print("Congratulations!! events stored in events.csv file in your script's directory")
print("Images can be found in local directory :)")
