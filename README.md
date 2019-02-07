# Automated-facebook-events-scraping

Automated scraping of facebook events info and images inside Kathmandu, Bhaktapur and Lalitpur, Nepal using beautifulsoup and selenium through eventScrape.py. A csv file with events info and a folder with images will be created as output in the script's directory

## General requirements

- Python >=3.6
- pip

## Installation

### 0. (Optional) Setup venv

```bash
python -m venv ./.venv/fb-events
source .venv/fb-events/bin/activate
```

### 1. Step-by-step setup:

Install python requirements and download geckodriver:

```bash
pip install -r requirements.txt
```

Download and setup geckodriver with `setup.sh`. E.g.,

```
sh setup.sh -v 32 -s macos
```

**_NOTE_**: MacOS is uneffected by specified version

Next step is system specific:

**[MacOS/Linux]**

Copy geckodriver to `/usr/bin`:

```bash
cp ./geckodriver /usr/bin/
```

**[Windows]**

Set your path variable to `geckodriver.exe` as it is described [here](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/)

## Usage

Start script `eventSceape.py` by specifying `year` and `month`. E.g.,

```bash
python eventScrape.py --year=2019 --month=1
```

Script work in background by default. To use it in foreground add argument `--visible`.

```bash
python eventScrape.py --year=2019 --month=1 --visible
```
