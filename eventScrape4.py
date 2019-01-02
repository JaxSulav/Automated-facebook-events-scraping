import csv
import urllib.request
import re
import os
import shutil
import argparse
from bs4 import BeautifulSoup
from selenium import webdriver

def anyEvent():
    with open('events.csv', 'w', newline='') as e:  # open csv in write mode
        csv_writer = csv.writer(e)
        csv_writer.writerow(['Date', 'Day', 'Event Name', 'Host', 'Location', 'Time', 'Interested/Going'])

        for i in range(10000):
            options.add_argument('-headless')
            browser = webdriver.Firefox(executable_path=geckodriver, options=options)
            try:

                s1 = queue[0]
                print("loop no: " + str(i))

                if s1 not in visited:  # if current link is not already visited
                    print("crawling on: " + s1)

                    # using selenium
                    browser.get(s1)

                    e_y = browser.find_element_by_xpath('//*[@id="title_subtitle"]/span')
                    e_year = e_y.get_attribute('aria-label')[-4:]
                    dum_list = e_y.get_attribute('aria-label')
                    e_weekday = e_y.get_attribute('aria-label')[0:dum_list.index(',')]

                    e_time = browser.find_element_by_class_name('_2ycp').text
                    e_people = browser.find_element_by_class_name('_5z74').text
                    e_location = browser.find_element_by_xpath(
                        '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[3]/div/div/div[2]/div/ul/li[2]/div[1]/table/tbody/tr/td[2]/div/div[1]/div/div[2]/div').text

                    try:
                        link_webobject = browser.find_element_by_xpath(
                            '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[1]/div/div/div[1]/div/div[4]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[1]/a')
                        # xpath(//*[@id="u_0_2x"]/a) didn't work. Also id kept changing in certain pages
                        link_append = link_webobject.get_attribute('href')[0:48]
                        queue.append(link_append)
                    except:
                        pass

                    try:
                        link_webobject1 = browser.find_element_by_xpath(
                            '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[1]/div/div/div[1]/div/div[4]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/a')
                        link_append1 = link_webobject1.get_attribute('href')[0:48]
                        queue.append(link_append1)
                    except:
                        pass

                    try:
                        link_webobject2 = browser.find_element_by_xpath(
                            '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[1]/div/div/div[1]/div/div[4]/div/div[2]/div[3]/div/div[2]/div/div[2]/div[1]/a')
                        link_append2 = link_webobject2.get_attribute('href')[0:48]
                        queue.append(link_append2)
                    except:
                        pass

                    try:
                        link_webobject3 = browser.find_element_by_xpath(
                            '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[1]/div/div/div[1]/div/div[4]/div/div[2]/div[4]/div/div[2]/div/div[2]/div[1]/a')
                        link_append3 = link_webobject3.get_attribute('href')[0:48]
                        queue.append(link_append3)
                    except:
                        pass

                    try:
                        link_webobject4 = browser.find_element_by_xpath(
                            '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[1]/div/div/div[1]/div/div[4]/div/div[2]/div[5]/div/div[2]/div/div[2]/div[1]/a')
                        link_append4 = link_webobject4.get_attribute('href')[0:48]
                        queue.append(link_append4)
                    except:
                        pass

                    try:
                        link_webobject5 = browser.find_element_by_xpath(
                            '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[1]/div/div/div[1]/div/div[4]/div/div[2]/div[6]/div/div[2]/div/div[2]/div[1]/a')
                        link_append5 = link_webobject5.get_attribute('href')[0:48]
                        queue.append(link_append5)
                    except:
                        pass

                    # using beautifulsoup and requests

                    r = urllib.request.urlopen(s1).read()

                    soup = BeautifulSoup(r, 'lxml')

                    e_name = soup.find('h1', {'id': 'seo_h1_tag'}).text

                    if soup.find('img', attrs={'class': 'scaledImageFitWidth'}):
                        image = soup.find('img', attrs={'class': 'scaledImageFitWidth'})
                    else:
                        image = soup.find('img', attrs={'class': 'scaledImageFitHeight'})

                    img = image['src']

                    create_img = open(os.path.join('Images_collected', e_name + ".jpeg"), 'wb')
                    create_img.write(urllib.request.urlopen(img).read())
                    create_img.close()

                    e_month = soup.find('span', attrs={'class': '_5a4-'}).text
                    e_date = soup.find('span', attrs={'class': '_5a4z'}).text

                    e_host_sel = soup.find_all('a', attrs={'href': re.compile("^https://")})
                    e_host = e_host_sel[2].text

                    csv_writer.writerow(
                        [e_month + " " + e_date + ", " + e_year, e_weekday, e_name, e_host, e_location, e_time,
                         e_people])

                    visited.append(s1)

                    browser.quit()
                    del queue[0]  # remove 1st element from queue
                    print("...Done")
                    print("crawled: " + str(len(visited)) + "    |   " + "Queue: " + str(len(queue)) + '\n')

                else:
                    print("Already crawled: " + s1)
                    print("crawled: " + str(len(visited)) + "    |   " + "Queue: " + str(len(queue)) + '\n')
                    del queue[0]
                    browser.quit()
                    pass

            except:
                del queue[0]
                browser.quit()  # if the links are not found in a page, close the browser while passing
                pass

            if int(len(visited)) == n1:
                break
            else:
                pass

    return

def janEvent():
    with open('events_JAN.csv', 'w', newline='') as e:  # open csv in write mode
        csv_writer = csv.writer(e)
        csv_writer.writerow(['Date', 'Day', 'Event Name', 'Host', 'Location', 'Time', 'Interested/Going'])

        for i in range(10000):
            options.add_argument('-headless')
            browser = webdriver.Firefox(executable_path=geckodriver, options=options)
            try:
                s1 = queue[0]
                print("loop no: " + str(i))

                if s1 not in visited:  # if current link is not already visited
                    print("crawling on: " + s1)

                    # using selenium
                    browser.get(s1)

                    e_y = browser.find_element_by_xpath('//*[@id="title_subtitle"]/span')
                    e_year = e_y.get_attribute('aria-label')[-4:]
                    year = int(e_year)

                    e_location = browser.find_element_by_xpath(
                        '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div[3]/div/div/div[2]/div/ul/li[2]/div[1]/table/tbody/tr/td[2]/div/div[1]/div/div[2]/div').text

                    try:
                        link_webobject = browser.find_element_by_xpath(
                            '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[1]/div/div/div[1]/div/div[4]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[1]/a')
                        # xpath(//*[@id="u_0_2x"]/a) didn't work. Also id kept changing in certain pages
                        link_append = link_webobject.get_attribute('href')[0:48]
                        queue.append(link_append)
                    except:
                        pass

                    try:
                        link_webobject1 = browser.find_element_by_xpath(
                            '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[1]/div/div/div[1]/div/div[4]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/a')
                        link_append1 = link_webobject1.get_attribute('href')[0:48]
                        queue.append(link_append1)
                    except:
                        pass

                    try:
                        link_webobject2 = browser.find_element_by_xpath(
                            '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[1]/div/div/div[1]/div/div[4]/div/div[2]/div[3]/div/div[2]/div/div[2]/div[1]/a')
                        link_append2 = link_webobject2.get_attribute('href')[0:48]
                        queue.append(link_append2)
                    except:
                        pass

                    try:
                        link_webobject3 = browser.find_element_by_xpath(
                            '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[1]/div/div/div[1]/div/div[4]/div/div[2]/div[4]/div/div[2]/div/div[2]/div[1]/a')
                        link_append3 = link_webobject3.get_attribute('href')[0:48]
                        queue.append(link_append3)
                    except:
                        pass

                    try:
                        link_webobject4 = browser.find_element_by_xpath(
                            '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[1]/div/div/div[1]/div/div[4]/div/div[2]/div[5]/div/div[2]/div/div[2]/div[1]/a')
                        link_append4 = link_webobject4.get_attribute('href')[0:48]
                        queue.append(link_append4)
                    except:
                        pass

                    try:
                        link_webobject5 = browser.find_element_by_xpath(
                            '/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[1]/div/div/div[1]/div/div[4]/div/div[2]/div[6]/div/div[2]/div/div[2]/div[1]/a')
                        link_append5 = link_webobject5.get_attribute('href')[0:48]
                        queue.append(link_append5)
                    except:
                        pass

                    # using beautifulsoup and requests

                    r = urllib.request.urlopen(s1).read()

                    soup = BeautifulSoup(r, 'lxml')

                    e_month = soup.find('span', attrs={'class': '_5a4-'}).text

                    if 'Kathmandu' in e_location or 'Bhaktapur' in e_location or 'Lalitpur' in e_location:
                        if year == 2019 and e_month == 'JAN':
                            dum_list = e_y.get_attribute('aria-label')
                            e_weekday = e_y.get_attribute('aria-label')[0:dum_list.index(',')]

                            e_time = browser.find_element_by_class_name('_2ycp').text
                            e_people = browser.find_element_by_class_name('_5z74').text

                            e_name = soup.find('h1', {'id': 'seo_h1_tag'}).text

                            if soup.find('img', attrs={'class': 'scaledImageFitWidth'}):
                                image = soup.find('img', attrs={'class': 'scaledImageFitWidth'})
                            else:
                                image = soup.find('img', attrs={'class': 'scaledImageFitHeight'})

                            img = image['src']

                            create_img = open(os.path.join('Images_collected_JAN', e_name + ".jpeg"), 'wb')
                            create_img.write(urllib.request.urlopen(img).read())
                            create_img.close()

                            e_date = soup.find('span', attrs={'class': '_5a4z'}).text

                            e_place = soup.find('a', attrs={'id': 'u_0_16'})

                            e_host_sel = soup.find_all('a', attrs={'href': re.compile("^https://")})
                            e_host = e_host_sel[2].text

                            csv_writer.writerow(
                                [e_month + " " + e_date + ", " + e_year, e_weekday, e_name, e_host, e_location, e_time,
                                 e_people])

                            jan.append(s1)
                            print("(JAN, 2019|inside valley) written in csv: --------- " + str(len(jan)))
                        else:
                            print("not in JAN, 2019")
                            pass
                    else:
                        print("not in Valley")
                        pass

                    visited.append(s1)

                    browser.quit()
                    del queue[0]  # remove 1st element of queue
                    print("...Done")
                    print("crawled: " + str(len(visited)) + "    |   " + "Queue: " + str(len(queue)) + '\n')

                else:
                    print("Already crawled: " + s1)
                    print("crawled: " + str(len(visited)) + "    |   " + "Queue: " + str(len(queue)) + '\n')
                    del queue[0]
                    browser.quit()
                    pass

            except:
                try:
                    del queue[0]
                except:
                    pass
                browser.quit()  # if the links are not found in a page, close the browser while passing
                pass

    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inp")
args = parser.parse_args()

geckodriver = '/usr/bin/geckodriver'  # firefox driver
options = webdriver.FirefoxOptions()

if args.inp == 'any':
    n1 = int(input("Enter numbers of events you want to extract: "))
        # creating Images_collected directory if not already created and remove and create dir if already there
    if os.path.exists('Images_collected'):
        shutil.rmtree('./Images_collected')
        os.makedirs('Images_collected')
    else:
        os.makedirs('Images_collected')

elif args.inp == 'jan':
    jan = []
    if os.path.exists('Images_collected_JAN'):
        shutil.rmtree('./Images_collected_JAN')
        os.makedirs('Images_collected_JAN')
    else:
        os.makedirs('Images_collected_JAN')

else:
    print("Forgot the args??!!")

base_url = input("Paste base url to start with:")
queue = []   # queuing links
visited = []  # listing crawled list
queue.append(base_url)




if args.inp == 'any':
    anyEvent()
    links = set(visited)
    f = open("crawled_urls", "w+")
    for link in sorted(links):
        f.write(link + '\n')

    print("Congratulations!! " + str(n1) + " events stored in events.csv file in your script's directory")
    print("Also!! check the scraped urls in crawled_urls.txt file in your script's directory")
    print("Images can be found in local directory :)")

elif args.inp == 'jan':
    janEvent()
    links = set(jan)
    f = open("crawled_urls_JAN", "w+")
    for link in sorted(links):
        f.write(link + '\n')

    print("Congratulations!! " + str(len(jan)) + " events stored in events_JAN.csv file in your script's directory")
    print("Also!! check the scraped urls in crawled_urls_JAN.txt file in your script's directory")
    print("Images can be found in local directory :)")

else:
    print("Forgot the args??!!")



