import logging
import requests
import dao

from selenium import webdriver
from typing import Dict, List

# __entry_url__ = 'https://mrmockup.com/freebies/'
__entry_url__ = 'http://localhost:8000/freebies.html'
__item_path__ = 'div.posts-container article.regular div.post-content'


__default_headers__ = {
    'upgrade-insecure-requests': '1',
    'dnt': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9',
}


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

    def bar(self, url: str):
        logging.debug('will get')
        self._driver.get(url)
        self.__mockup_item_process__()

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
            'download_url': 'meta[http-equiv]'
        }
        title = self._driver.find_element_by_css_selector(
            patterns['title']).text
        cover_url = self._driver.find_element_by_css_selector(
            patterns['cover_url']).get_attribute('src')
        description = self._driver.find_element_by_css_selector(
            patterns['description']).text
        button = self._driver.find_element_by_css_selector(
            patterns['download_button'])

        button.click()

        download_page_meta_tag = self._driver.find_element_by_css_selector(
            patterns['download_url'])
        download_url = download_page_meta_tag.get_attribute(
            'content').split('url=')[-1]
        download_headers = {'referer': self._driver.current_url}
        print('download headers: %s' % download_headers)
        resource_url = get_resource_link(
            download_url, headers=download_headers)
        print(resource_url)
        # download by url
        entity = dao.MockupEntity.create(title=title, description=description,
                                         cover_url=cover_url, source=self._driver.current_url)
        entity.save()
        breakpoint()
        self._driver.back()


def get_resource_link(url: str, headers: Dict[str, str], default_headers: Dict[str, str] = __default_headers__) -> str:
    '''
    获取资源下载链接
    '''
    combined_headers = {**headers}

    for key in default_headers:
        value = default_headers[key]
        combined_headers.setdefault(key, value)

    assert('referer' in combined_headers)

    breakpoint()
    r = requests.get(url, headers=combined_headers, allow_redirects=False)

    assert(r.ok)
    assert('Location' in r.headers)

    return r.headers['Location']


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
    dao.db_setup()
    driver = get_driver()
    runner = MrMockup(driver)
    runner.bar('https://mrmockup.com/lying-coffee-cup-mockup/')
