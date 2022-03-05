from time import sleep
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class Skill:
    def set_name(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def set_level(self, level: int):
        self.level = level

    def get_level(self) -> int:
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
        skill_html: BeautifulSoup
        for skill_html in skills_html:
            skill = Skill()
            name = skill_html.find('div', {'class', 'lap-skill-name'}).text
            level = int(skill_html.find(
                'div', {'class', 'lap-skill-level'}).text)

            skill.set_name(name)
            skill.set_level(level)
            lst_skills.append(skill)

        return lst_skills
