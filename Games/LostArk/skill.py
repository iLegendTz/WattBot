from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os


class Skill:
    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_level(self, level):
        self.level = level

    def get_level(self):
        return self.level

    def search_skills(self, url):
        driver_path = f"{os.getcwd()}/WebDriver/chromedriver.exe"
        service = Service(driver_path)

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        sleep(3)

        soup = BeautifulSoup(driver.page_source, 'lxml')
        driver.close()

        skills_html = soup.find_all('div', {'class', 'lap-SkillSlot'})[:8]

        lst_skills = []
        for skill_html in skills_html:
            skill = Skill()
            name = skill_html.find('div', {'class', 'lap-skill-name'}).text
            level = skill_html.find('div', {'class', 'lap-skill-level'}).text

            skill.set_name(name)
            skill.set_level(level)
            lst_skills.append(skill)

        return lst_skills
