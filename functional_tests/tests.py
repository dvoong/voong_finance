from django.test import TestCase

# Create your tests here.
from selenium import webdriver
from django.test import LiveServerTestCase

class FunctionalTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Chrome()
        
    def tearDown(self):
        self.browser.quit()

    def test_new_entry(self):

        # load homepage
        self.browser.get(self.live_server_url)
        self.assertEqual(self.browser.title, 'Voong Finance')
        
        # # add transaction entry
        # form = self.browser.find_element_by_id('transaction-form')
        # date_input = form.find_element_by_name('date')
        # transaction_input = form.find_element_by_name('transaction')
        # description_input = form.find_element_by_name('description')
        # submit = form.find_element_by_css_selector('input[type="submit"]')
        
        # date_input.send_keys('2016-08-01')
        # transaction_input.send_keys('150')
        # description_input.send_keys('Bank pays dividends')
