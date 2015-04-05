#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from filereader import *

class Compare(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_start_page(self):
        driver = self.driver
        self.files = 0
        while self.files != len(file_list):
            driver.get("http://www.herdprotect.com/knowledgebase.aspx")
            assert 'herdProtect' in driver.title
            self.file_page()

    def tearDown(self):
        self.driver.close()

    def file_page(self):
        files = self.files
        search = self.driver.find_element_by_name("ctl00$txtSearch")
        search.send_keys(md5_list[files])
        search.send_keys(Keys.ENTER)
        self.wait()
        self.search()

    def search(self):
        m = 0; errors = 0
        fields = ['File name:', 'Publisher:', 'Product:', 'Description:', 'MD5:', 'SHA-1:', 'SHA-256:',
                'File size:', 'Product version:', 'Copyright:', 'Compilation timestamp:']
        try:
            assert '%s' % file_names[self.files] in self.driver.title.lower()
            print("Name of the file for analis: '%s'" % file_names[self.files])
            line_number = 1
            while m != 11:
                try:
                    item = self.driver.find_element_by_xpath("//div[@class = 'keyvaluepairs']/div[%d]" % line_number)
                    field_name = item.text.split('\n')[0]
                    if field_name == fields[m]:
                        object = item.text.split('\n')[1]
                        if field_name == "Compilation timestamp:":
                            object = datetime.datetime.strptime(object, "%m/%d/%Y %H:%M:%S %p")
                            object = object.strftime("%m/%d/%Y %H:%M:%S %p")
                        if field_name == "File size:":
                            object = object.split(' ', 2)[2]
                        if (all_information[m][self.files]) != object:
                            print("  %s '%s' is not like '%s'" % (field_name, all_information[m][self.files], object))
                            errors += 1
                        m += 1
                    line_number += 1
                except:
                    print("  '%s' is not in this page" % (fields[m]))
                    errors += 1; m += 1
            print('  Number of errors: %d' % errors)
            self.files += 1
        except AssertionError:
            print("File '%s' not found" % file_names[self.files])
            self.files += 1

    def wait(self):
        wait_time = 10
        while 'anti-malware multiscanning' in self.driver.title.lower():
            self.driver.implicitly_wait(wait_time)
            not_found_massage = self.driver.find_element_by_xpath("//div[@id = 'windowModalContent']").text
            wait_time += 10
            if wait_time == 100:
                print 'Page with %s not load' % file_names[self.files]
                break
            if 'OK' in not_found_massage:
                break

if __name__ == "__main__":
    unittest.main()