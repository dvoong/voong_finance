# Unit tests tell a developer that the code is doing things right; functional tests tell a developer that the code is doing the right things.

import datetime
from django.test import TestCase

# Create your tests here.
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

DEFAULT_TIMEOUT = 1

def wait_for_element_with_id(browser, element_id, timeout=DEFAULT_TIMEOUT):
    return WebDriverWait(browser, timeout=timeout).until(
        lambda b: b.find_element_by_id(element_id),
        'Could not find element with id: {}. Page text was:\n{}'.format(
            element_id, browser.find_element_by_tag_name('body').text
        )
    )

#class FunctionalTest(LiveServerTestCase):
class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        # self.browser = webdriver.Firefox()
        self.today = datetime.date(2017, 1, 24)
        
    def tearDown(self):
        self.browser.quit()

    def wait_for_element_with_id(self, element_id, timeout=DEFAULT_TIMEOUT):
        return wait_for_element_with_id(self.browser, element_id, timeout)

    def test_new_entry(self):
        INITIAL_BALANCE = 4344.40
        
        # david loads the homepage
        self.browser.get(self.live_server_url)
        self.assertEqual(self.browser.title, 'Voong Finance')

        # it's his first time to the site # TODO: sign in, sessions, welcome page, etc
        # he is invited to initialise his balance or to "do it later"
        initialise_balance = self.wait_for_element_with_id('balance-initialisation')
        input_field = initialise_balance.find_element_by_id('input')
        submit_button = initialise_balance.find_element_by_id('submit-button')
        date = initialise_balance.find_element_by_id('date')
        date.send_keys(self.today.isoformat())

        # he inputs his balance as 4344.40 GBP and hits ok/next/done button
        input_field.send_keys(str(INITIAL_BALANCE))

        # He clicks the submit button
        submit_button.click()

        # A blance chart appears at the top of the page
        balance_chart = self.wait_for_element_with_id('balance-chart')

        # The balance chart shows
        bars = balance_chart.find_elements_by_css_selector('.bar');
        self.assertEqual(len(bars), 28)

        self.assertEqual(bars[1].get_attribute('balance'), str(INITIAL_BALANCE))
        self.assertEqual(bars[-1].get_attribute('balance'), str(INITIAL_BALANCE))

        # the initial balance prompt should have disappeared
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('balance-initialisation')

        # a navbar appears at the top
        navbar = self.browser.find_element_by_id('navbar')
        
        # the navbar contains a logo which presumably takes the user back to the homepage TODO: test for the logo
        logo = navbar.find_element_by_id('logo')
        
        # the navbar contains a 'create transaction' button
        create_transaction_btn = navbar.find_element_by_id('create-transaction-btn')
        
        # the navbar contains other typical navigation buttons
        # TODO: other navbar things, e.g. contact, settings/profile, transaction_history maybe
        
        # a calendar view appears below the chart
        calendar = self.browser.find_element_by_id('calendar')
        
        # he is now invited to create his first entry
        # perhaps a popup appears over a highlighted transaction button or the rest of the page is dimmed
        first_entry_prompt = self.get_first_entry_prompt()

        # a transaction form appears
        transaction_form = first_entry_prompt.find_element_by_id('transaction-form')

        # the date for the transaction is set to today
        today = datetime.date.today()
        year_selector = transaction_form.find_element_by_id('date-selector_year');
        self.assertEqual(year_selector.get_attribute('value'), str(today.year))
        month_selector = transaction_form.find_element_by_id('date-selector_month');
        self.assertEqual(month_selector.get_attribute('value'), str(today.month))
        day_selector = transaction_form.find_element_by_id('date-selector_day');
        self.assertEqual(day_selector.get_attribute('value'), str(today.day))
        
        # david sets transaction type to expense
        transaction_type_dropdown = transaction_form.find_element_by_id('transaction-type-dropdown')
        Select(transaction_type_dropdown).select_by_visible_text('Expense')
        
        # david types name as phone bill
        transaction_description = transaction_form.find_element_by_id('transaction-description')
        transaction_description.send_keys('New Phone')

        # david sets the date to next week
        transaction_date = self.today + datetime.timedelta(days=7)
        year_selector.send_keys(str(transaction_date.year))
        month_selector.send_keys(transaction_date.strftime("%B"))
        day_selector.send_keys(str(transaction_date.day))

        # david enters the amount as 719.99
        transaction_size_input = transaction_form.find_element_by_id('transaction-size-input')
        transaction_size_input.send_keys('719.99')
        
        # david clicks the create transaction button
        create_transaction_btn = transaction_form.find_element_by_id('create-transaction-btn')
        create_transaction_btn.click()

        # the first transaction prompt disappears
        WebDriverWait(self.browser, 5).until_not(EC.presence_of_element_located(('id', 'first-entry-prompt')))
        
        # The balance chart updates
        # bars = balance_chart.find_elements_by_css_selector('.bar[date="{}"]'.format(date))
        bars = balance_chart.find_elements_by_css_selector('.bar')
        bar = [bar for bar in bars if bar.get_attribute('date') == transaction_date.isoformat()]
        self.assertEqual(len(bar), 1)
        bar = bar[0]
        self.assertEqual(bar.get_attribute('balance'), str(INITIAL_BALANCE - 719.99))

        # the range of dates should be unchanged
        bars[0].get_attribute('date') == self.today.isoformat()
        bars[0].get_attribute('balance') == INITIAL_BALANCE
        self.assertEqual(len(bars), 28)

        # next week shows the balance as 4329.40, this is true for dates following it also
        bars[-1].get_attribute('date') == (self.today + datetime.timedelta(days=27)).isoformat()
        bars[-1].get_attribute('balance') == str(INITIAL_BALANCE - 719.99)

        # the dates between today and next week show the original balance (inclusive of today, exclusive of next week)
        bars[6].get_attribute('date') == (self.today + datetime.timedelta(days=6)).isoformat()
        bars[6].get_attribute('balance') == str(INITIAL_BALANCE)
        bars[7].get_attribute('date') == transaction_date.isoformat()
        bars[7].get_attribute('balance') == str(INITIAL_BALANCE - 719.99)

        # David reloads the page
        self.browser.get(self.live_server_url)

        # instead of seeing the welcome screen he sees the existing balance chart
        WebDriverWait(self.browser, 5).until_not(EC.presence_of_element_located(('id', 'balance-initialisation')))
        balance_chart = self.browser.find_element_by_id('balance-chart')

        # The balance chart should be centred around today
        bars = balance_chart.find_elements_by_css_selector('.bar')
        self.assertEqual(len(bars), 28)
        bar = bars[13]
        self.assertEqual(bar.get_attribute('date'), datetime.date.today().isoformat())

        # bars should have the same values
        map(lambda bar: self.assertEqual(bar.get_attribute('balance'), str(INITIAL_BALANCE - 719.99)), bars)
        
        # the calendar view also shows a new entry on the date for next week
        dates = calendar.find_element_by_css_selector('.date');
        date = None
        for date in dates:
            if date.get_attribute('date') == transaction_date.isoformat():
                break
        transaction = date.find_element_by_css_selector('.transaction')
        self.assertEqual(transaction.get_attribute('size'), str(719.99))
        self.assertEqual(transaction.text(), str(719.99))
        
        # david ticks the "transaction repeats" checkbox
        # repeating_transaction_checkbox = transaction_form.find_element_by_id('repeating-transaction-checkbox')
        # repeating_transaction_checkbox.click()
        
        # # david selects "repeats monthly"
        # repeat_frequency_dropdown = transaction_form.find_element_by_id('repeat-frequency-dropdown')
        # Select(repeat_frequency_dropdown).select_by_visible_text('Monthly')
        
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

    def get_first_entry_prompt(self):
        return self.browser.find_element_by_id('first-entry-prompt')

    #     # OLD STUFF
    #     # homepage shows a balance chart
    #     self.browser.find_element_by_id('balance-chart')
        
    #     # # add transaction entry
    #     # form = self.browser.find_element_by_id('transaction-form')
    #     # date_input = form.find_element_by_name('date')
    #     # transaction_input = form.find_element_by_name('transaction')
    #     # description_input = form.find_element_by_name('description')
    #     # submit = form.find_element_by_css_selector('input[type="submit"]')
        
    #     # date_input.send_keys('2016-08-01')
    #     # transaction_input.send_keys('150')
    #     # description_input.send_keys('Bank pays dividends')
