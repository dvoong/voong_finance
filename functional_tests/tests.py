# Unit tests tell a developer that the code is doing things right; functional tests tell a developer that the code is doing the right things.

import datetime
from django.test import TestCase

# Create your tests here.
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
    
from django.test import LiveServerTestCase

DEFAULT_TIMEOUT = 1

def wait_for_element_with_id(browser, element_id, timeout=DEFAULT_TIMEOUT):
    return WebDriverWait(browser, timeout=timeout).until(
        lambda b: b.find_element_by_id(element_id),
        'Could not find element with id: {}. Page text was:\n{}'.format(
            element_id, browser.find_element_by_tag_name('body').text
        )
    )

class FunctionalTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.today = datetime.date(2017, 1, 24)
        
    def tearDown(self):
        self.browser.quit()

    def wait_for_element_with_id(self, element_id, timeout=DEFAULT_TIMEOUT):
        return wait_for_element_with_id(self.browser, element_id, timeout)

    def test_new_entry(self):

        # david loads the homepage
        self.browser.get(self.live_server_url)
        self.assertEqual(self.browser.title, 'Voong Finance')

        # it's his first time to the site # TODO: sign in, sessions, welcome page, etc
        # he is invited to initialise his balance or to "do it later"
        initialise_balance = self.wait_for_element_with_id('balance-initialisation')
        print(initialise_balance)
        print(dir(initialise_balance))
        input_field = initialise_balance.find_element_by_id('input')
        submit_button = initialise_balance.find_element_by_id('submit-button')

        # he inputs his balance as 4344.40 GBP and hits ok/next/done button
        input_field.send_keys('4344.40')
        # TODO: invalid input

        # He clicks the submit button
        submit_button.click()

        # redirects to a new page?
        # nah lets make it a single page app
        
        # A blance chart appears at the top of the page
        balance_chart = self.wait_for_element_with_id('balance-chart')

        # the initial balance prompt should have disappeared
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('balance-initialisation')

        # a navbar appears at the top
        # the navbar contains a logo which presumably takes the user back to the homepage
        # the navbar contains a 'create transaction' button
        # the navbar contains other typical navigation buttons
        # a calendar view appears below the chart
        # he is now invited to create his first entry
        # perhaps a popup appears over a highlighted transaction button or the rest of the page is dimmed
        # a transaction form appears
        # david sets transaction type to expense
        # david types name as phone bill
        # david sets the date to next week
        # david ticks the "transaction repeats" checkbox
        # david selects "repeats monthly"
        # david enters the amount as 15 GBP
        # david clicks the create transaction button
        # The balance chart updates
        # next week shows the balance as 4329.40, this is true for dates following it also
        # the dates between today and next week show the original balance (inclusive of today, exclusive of next week)
        # the calendar view also shows a new entry on the date for next week
        # david wants to check that this worked for future dates
        # he clicks a button to skip ahead to the next month
        # the charts slides along and centres on the same date (TODO: What about when the next month doesn't have the smae number of dates?
        # probably go to the next highests date, but how to test this properly in functional tests?
        # This kind of test is better handled by unit tests? Argument for keeping this in functional tests too. But then how to test certain dates?
        # Would need to mock the date? Not sure you should use mocks in functional tests?
        # How is today determined? The server date seems the most sensible. This means 'today' is not exposed by the backend
        # Testing how the dates are manipulated feels like it should be in a functional test, having the logic here seems appropriate
        # But it also seems appropriate to put it in unit tests for development reasons
        # To have it in both would involve duplication in code?
        # Should it be abstracted out of unit and functional tests?
        # How to get the functional test to run for a given date?
        # Need to mock the today method in the datetime module?
        # problem: cannot mock the datetime module for the server, it's in a different python process
        self.assertEqual(1, 0, 'Finish functional tests')


        # OLD STUFF
        # homepage shows a balance chart
        self.browser.find_element_by_id('balance-chart')
        
        # # add transaction entry
        # form = self.browser.find_element_by_id('transaction-form')
        # date_input = form.find_element_by_name('date')
        # transaction_input = form.find_element_by_name('transaction')
        # description_input = form.find_element_by_name('description')
        # submit = form.find_element_by_css_selector('input[type="submit"]')
        
        # date_input.send_keys('2016-08-01')
        # transaction_input.send_keys('150')
        # description_input.send_keys('Bank pays dividends')
