import logging
import pickle
from selenium import webdriver
from typing import List

# __entry_url__ = 'https://mrmockup.com/freebies/'
__entry_url__ = 'http://localhost:8000/freebies.html'
__item_path__ = 'div.posts-container article.regular div.post-content'


class MrMockup:
    _driver: webdriver.remote.webdriver.WebDriver

    def __init__(self, driver: webdriver.remote.webdriver.WebDriver) -> None:
        self._driver = driver

    def foo(self):
        '''
        1. 获取列表页
        2. 将当前页所有的东西一个一个处理完（下载）
        3. 检测是否有下一页，如果有的话重复第1步
        4. 完成
        '''
        logging.debug('will get')
        self._driver.get(__entry_url__)
        web_items = self._driver.find_elements_by_css_selector(__item_path__)
        logging.debug('got items')
        self.__page_item_process__(web_items)

    def __page_item_process__(self, elements: List[webdriver.remote.webelement.WebElement]):
        logging.debug('process items')
        for element in elements[:1]:
            logging.debug('will click')
            element.click()
            self.__mockup_item_process__()
            self._driver.back()
        breakpoint()

    def __mockup_item_process__(self):
        patterns = {
            'title': 'h1.entry-title',
            'cover_url': 'div.inner img',
            'description': 'div.wpb_wrapper p',
            'download_button': 'div.wpb_wrapper a.nectar-button',
        }
        title = self._driver.find_element_by_css_selector(
            patterns['title']).text
        cover_url = self._driver.find_element_by_css_selector(patterns['cover_url'])[
            0].get_attribute('src')
        description = self._driver.find_element_by_css_selector(
            patterns['description']).text
        button = self._driver.find_element_by_css_selector(
            patterns['download_button'])
        breakpoint()


def get_driver() -> webdriver.remote.webdriver.WebDriver:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.headless = True
    options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

    driver = webdriver.Chrome(
        executable_path='/usr/local/bin/chromedriver', options=options)

    return driver


if __name__ == '__main__':
    driver = get_driver()
    runner = MrMockup(driver)
    runner.foo()
