from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os


class Build():

    def __init__(self, character_class, character_advanced_class):
        self.character_class = character_class
        self.character_advanced_class = character_advanced_class

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def set_skills(self, skills):
        self.skills = skills

    def get_skills(self):
        return self.skills

    def set_image_url(self, image_url):
        self.image_url = image_url

    def get_image_url(self):
        return self.image_url

    def search_builds(self):
        driver_path = f"{os.getcwd()}/WebDriver/chromedriver.exe"
        service = Service(driver_path)

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = webdriver.Chrome(service=service, options=options)
        url = f"https://lost-ark.maxroll.gg/build-guides#classes=[{self.character_class}]&classes=[{self.character_advanced_class}]"
        driver.get(url)
        sleep(3)

        soup = BeautifulSoup(driver.page_source, 'lxml')
        driver.close()
        builds_html = soup.find('div', {'id': 'filter-results'}
                                ).findChildren('a', recursive=False)

        lst_builds = []
        for build_html in builds_html:
            build = Build(self.character_class, self.character_advanced_class)
            name = build_html.find('h2').text
            build_url = build_html['href']

            build.set_name(name)
            build.set_url(build_url)
            build.set_image_url(build_html.find('img')['src'])
            lst_builds.append(build)

        return lst_builds
