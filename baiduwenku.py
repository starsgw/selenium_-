#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: dj
@contact: dj@itmojun.com
@software: PyCharm
@file: main.py
@time: 2018/10/31 10:37
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
from lxml import etree
import re

def main():
    # 通过设置--headless选项让火狐浏览器无GUI运行，提升效率
    option = webdriver.FirefoxOptions()
    option.add_argument("--headless")
    browser = webdriver.Firefox(options=option)
    browser.get('https://wenku.baidu.com/view/fbdc423a3968011ca30091f0.html')

    # browser = webdriver.PhantomJS()
    # browser.get('https://wenku.baidu.com/view/fbdc423a3968011ca30091f0.html')

    # 第一种方法：
    # browser.set_window_size(1366, 6000)  # 可以通过将浏览器窗口高度设置为很高，以让“继续浏览”链接显示出来，然后点击它
    # elem = browser.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[6]/div[2]/div[1]/span")
    # elem.click()
    # browser.fullscreen_window()  # 将浏览器窗口全屏，否则后面某些页面的爬取会出问题

    # 第二种方法（更优雅）：
    # 将“继续浏览”链接移动到浏览器可视区域，然后点击它
    elem = browser.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[6]/div[2]/div[1]/span")
    browser.execute_script("arguments[0].scrollIntoView();", elem)
    elem.click()

    f = open("pid_data.txt", "w", encoding="utf-8")

    for i in range(2, 83):
            try:
                print("正在爬取第%d页内容..." % i)
                elem = browser.find_elements_by_css_selector("input.page-input")
                elem[0].clear()
                elem[0].send_keys(str(i), Keys.RETURN)

                # time.sleep(10)
                WebDriverWait(browser, 20, 0.5).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@id='pageNo-%d']//p" % i)))

                page = str(browser.page_source)

                root = etree.HTML(page)

                p_list = root.xpath("//div[@id='pageNo-%d']//p" % i)

                cnt = 1
                for p in p_list:
                    if len(p.text) == 1 or len(p.text) == 2:
                        continue

                    if "，" in p.text:
                        continue

                    if re.match("\d{6}", p.text):
                        p.text = p.text[0:6]

                    if re.fullmatch("\d{6}", p.text) == None and "省" not in p.text and "市" not in p.text and "区" not in p.text and "县" not in p.text:
                        continue

                    print(p.text)

                    if cnt % 2 != 0:
                        f.write(p.text)
                    else:
                        f.write(" " + p.text + "\n")
                    cnt += 1

                f.flush()
            except TimeoutException:
                pass


    f.close()

    browser.close()


    # with open("test.html", "w", encoding="utf-8") as f:
    #     f.write(page)

    # page = browser.find_elements_by_css_selector("#pageNo-2")



if __name__ == '__main__':
    main()
