from selenium import webdriver

__entry_url__ = 'https://mrmockup.com/freebies/'
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
        self._driver.get(__entry_url__)

    def __item_process__(self, element: webdriver.remote.webelement.WebElement):
        pass
