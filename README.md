# Automated-facebook-events-scraping
Automated scraping of facebook events info and images using beautifulsoup and selenium through eventScrape.py. A csv file with events info and a folder with images will be created as output in the script's directory

Instructions:--
Download geckodriver for firefox from https://github.com/mozilla/geckodriver/releases

-- For Windows: Set your path variable to geckodriver.exe folder similarly as https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/

-- For Linux or Mac: copy geckodriver to the Automated-facebook-events-scraping folder

-- run eventScrape.py --year="YEAR VALUE" --month="MONTH VALUE" for extracting events from any month of any year

-- For Example: If events of january, 2019 is to be fetched, run eventScrape.py --year=2019 --month=1

-- By default program runs in browser's headless mode albeit, if you want to inspect in foreground mode:

-- run with argument --visible


