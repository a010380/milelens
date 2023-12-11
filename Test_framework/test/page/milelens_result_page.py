from selenium.webdriver.common.by import By
from .milelens_login_page import MilelensLoginPage



class MilelensResultPage(MilelensLoginPage):
    loc_result_links = (By.XPATH, '//div[contains(@class, "result")]/h3/a')

    @property
    def result_links(self):
        return self.find_elements(*self.loc_result_links) 
