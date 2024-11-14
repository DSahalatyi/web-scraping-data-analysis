import logging
import re
import time

import scrapy
from scrapy.shell import inspect_response
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scrape_service.items import VacancyItem

EXP_RANGE = {
    "0-1": "junior",
    "1-3": "strong_junior",
    "3-5": "middle",
    "5plus": "senior",
}

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class PythonSpider(scrapy.Spider):
    name = "python"
    allowed_domains = ["jobs.dou.ua"]

    def start_requests(self):
        base_url = "https://jobs.dou.ua/vacancies/?category=Python"
        headers = {"User-Agent": "Mozilla/5.0"}

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 10)

        for year_rage, exp_title in EXP_RANGE.items():
            url = base_url + f"&exp={year_rage}"

            driver.get(url)

            try:
                more_button = driver.find_element(By.CSS_SELECTOR, ".more-btn a")
            except NoSuchElementException:
                pass
            else:
                while more_button and more_button.is_displayed():
                    wait.until(EC.element_to_be_clickable(more_button))
                    more_button.click()
                    time.sleep(0.5)

            vacancies = None

            try:
                vacancies = driver.find_elements(By.CSS_SELECTOR, ".l-vacancy a.vt")
            except NoSuchElementException:
                self.log(f"No vacancies found at {url}")
            else:
                self.log(f"Found {len(vacancies)} {exp_title} vacancies")

            for vacancy in vacancies:
                yield scrapy.Request(
                    url=vacancy.get_attribute("href"),
                    headers=headers,
                    callback=self.parse,
                    cb_kwargs={"exp_title": exp_title},
                )

    def parse(self, response, exp_title=None):
        # inspect_response(response, self)
        item = VacancyItem()
        item["experience"] = exp_title
        item["title"] = response.css("h1.g-h2::text").get()
        location = response.css(".place::text").get()
        item["url"] = response.url
        item["location"] = location.strip() if location else None
        salary = response.css(".salary::text").get()
        item["salary"] = salary.replace("\xa0", " ").strip() if salary else None
        item["location"] = response.css(".place::text").get().replace("&nbsp", "").strip()
        item["company"] = response.css(".b-compinfo div.info div.l-n a::text").get()
        item["company_url"] = response.css(".b-compinfo div.info div.l-n a").attrib["href"]
        description = response.css('.b-typo.vacancy-section').xpath('string()').get()
        description = re.sub(r'[\n\t\xa0]', ' ', description)
        description = re.sub(r'\s+', ' ', description)
        description = re.sub(r'[^\w\s,]', '', description)
        description = description.strip()
        item["description"] = description

        yield item
