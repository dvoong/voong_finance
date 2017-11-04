import datetime
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_first_visit_flow(self):

        today = datetime.date.today()

        self.browser.get(self.live_server_url)
        # user is taken to the splash page
        self.assertEqual(self.browser.title, 'Voong Finance')

        # user is given to the option to register or to sign in
        registration_button = self.browser.find_element_by_id('registration-button')
        self.browser.find_element_by_id('signin-button')

        # user clicks on the registration button and is redirected to the registration page
        registration_button.click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/registration')

        registration_form = self.browser.find_element_by_id('registration-form')
        registration_form.find_element_by_id('first-name-input').send_keys('David')
        registration_form.find_element_by_id('last-name-input').send_keys('Voong')
        registration_form.find_element_by_id('email-input').send_keys('voong.david@gmail.com')
        registration_form.find_element_by_id('password-input').send_keys('password')
        registration_form.find_element_by_id('re-password-input').send_keys('password')
        registration_form.find_element_by_id('submit-button').click()

        self.assertEqual(self.browser.current_url, self.live_server_url + '/signin')

        # user verifies the email belongs to them

        # user reloads homepage
        self.browser.get(self.live_server_url)
        
        # user clicks sign in button
        self.browser.find_element_by_id('signin-button').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/signin')

        # user enters their details and signs in
        signin_form = self.browser.find_element_by_id('signin-form')
        signin_form.find_element_by_id('email-input').send_keys('voong.david@gmail.com')
        signin_form.find_element_by_id('password-input').send_keys('password')
        signin_form.find_element_by_id('submit-button').click()

        # user is redirected to their homepage
        self.assertEqual(self.browser.title, 'Home')
        self.assertEqual(self.browser.current_url, self.live_server_url + '/home')
        balance_chart = self.browser.find_element_by_id('balance-chart')
        transactions_table = self.browser.find_element_by_id('transactions-table')
        transaction_form = self.browser.find_element_by_id('transaction-form')

        # user creates a new transaction
        date_input = transaction_form.find_element_by_id('date-input')
        self.assertEqual(date_input.get_attribute('value'), today.isoformat())
        date_input.send_keys('{:02}{:02}{}'.format(today.day, today.month, today.year))

        type_input = transaction_form.find_element_by_id('type-input')
        Select(type_input).select_by_visible_text('Income')

        description_input = transaction_form.find_element_by_id('description-input')
        description_input.send_keys('Description')

        size_input = transaction_form.find_element_by_id('size-input')
        size_input.send_keys(100)

        transaction_form.find_element_by_id('submit-button').click()

        WebDriverWait(self.browser, timeout=2).until(lambda b: len(transactions_table.find_elements_by_css_selector('.transaction')) == 1)

        transactions = transactions_table.find_elements_by_css_selector('.transaction')
        self.assertEqual(len(transactions), 1)
        
        transaction_date = transactions[0].find_element_by_id('transaction-date')
        transaction_type = transactions[0].find_element_by_id('transaction-type')
        transaction_description = transactions[0].find_element_by_id('transaction-description')
        transaction_size = transactions[0].find_element_by_id('transaction-size')
        balance = transactions[0].find_element_by_id('balance')

        self.assertEqual(transaction_date.get_attribute('innerHTML'), today.isoformat())
        self.assertEqual(transaction_type.get_attribute('innerHTML'), 'income')
        self.assertEqual(transaction_description.get_attribute('innerHTML'), 'Description')
        self.assertEqual(transaction_size.get_attribute('innerHTML'), '100')
        self.assertEqual(balance.get_attribute('innerHTML'), '100')

        # the input form is cleared
        self.assertEqual(date_input.get_attribute('value'), today.isoformat())
        self.assertEqual(type_input.get_attribute('value'), 'income')
        self.assertEqual(description_input.get_attribute('value'), '')
        self.assertEqual(size_input.get_attribute('value'), '')

        # user creates another transaction
        # leaves the date as the same
        Select(type_input).select_by_visible_text('Expense')
        description_input.send_keys('Phone Bill')
        size_input.send_keys('15')
        transaction_form.find_element_by_id('submit-button').click()

        WebDriverWait(self.browser, timeout=2).until(lambda b: len(transactions_table.find_elements_by_css_selector('.transaction')) == 2)
        transactions = transactions_table.find_elements_by_css_selector('.transaction')
        self.assertEqual(len(transactions), 2)

        transaction = transactions[1]
        transaction_date = transaction.find_element_by_id('transaction-date')
        transaction_type = transaction.find_element_by_id('transaction-type')
        transaction_description = transaction.find_element_by_id('transaction-description')
        transaction_size = transaction.find_element_by_id('transaction-size')
        balance = transaction.find_element_by_id('balance')

        self.assertEqual(transaction_date.get_attribute('innerHTML'), today.isoformat())
        self.assertEqual(transaction_type.get_attribute('innerHTML'), 'expense')
        self.assertEqual(transaction_description.get_attribute('innerHTML'), 'Phone Bill')
        self.assertEqual(transaction_size.get_attribute('innerHTML'), '-15')
        self.assertEqual(balance.get_attribute('innerHTML'), '85')

        # user creates another transaction
        # date is earlier than today
        yesterday = today - datetime.timedelta(days=1)
        date_input.send_keys('{:02}{:02}{}'.format(yesterday.day, yesterday.month, yesterday.year))        
        Select(type_input).select_by_visible_text('Income')
        description_input.send_keys('Salary')
        size_input.send_keys('1000')
        transaction_form.find_element_by_id('submit-button').click()

        WebDriverWait(self.browser, timeout=2).until(lambda b: len(transactions_table.find_elements_by_css_selector('.transaction')) == 3)

        transactions = transactions_table.find_elements_by_css_selector('.transaction')
        
        # should be the new transaction
        transaction = transactions[0]
        transaction_date = transaction.find_element_by_id('transaction-date')
        transaction_type = transaction.find_element_by_id('transaction-type')
        transaction_description = transaction.find_element_by_id('transaction-description')
        transaction_size = transaction.find_element_by_id('transaction-size')
        balance = transaction.find_element_by_id('balance')

        self.assertEqual(transaction_date.get_attribute('innerHTML'), yesterday.isoformat())
        self.assertEqual(transaction_type.get_attribute('innerHTML'), 'income')
        self.assertEqual(transaction_description.get_attribute('innerHTML'), 'Salary')
        self.assertEqual(transaction_size.get_attribute('innerHTML'), '1000')
        self.assertEqual(balance.get_attribute('innerHTML'), '1000')

        # should be the first transaction and should be updated
        transaction = transactions[1]
        transaction_date = transaction.find_element_by_id('transaction-date')
        transaction_type = transaction.find_element_by_id('transaction-type')
        transaction_description = transaction.find_element_by_id('transaction-description')
        transaction_size = transaction.find_element_by_id('transaction-size')
        balance = transaction.find_element_by_id('balance')

        self.assertEqual(transaction_date.get_attribute('innerHTML'), today.isoformat())
        self.assertEqual(transaction_type.get_attribute('innerHTML'), 'income')
        self.assertEqual(transaction_description.get_attribute('innerHTML'), 'Description')
        self.assertEqual(transaction_size.get_attribute('innerHTML'), '100')
        self.assertEqual(balance.get_attribute('innerHTML'), '1100')

        # should be the second transaction
        transaction = transactions[2]
        transaction_date = transaction.find_element_by_id('transaction-date')
        transaction_type = transaction.find_element_by_id('transaction-type')
        transaction_description = transaction.find_element_by_id('transaction-description')
        transaction_size = transaction.find_element_by_id('transaction-size')
        balance = transaction.find_element_by_id('balance')

        self.assertEqual(transaction_date.get_attribute('innerHTML'), today.isoformat())
        self.assertEqual(transaction_type.get_attribute('innerHTML'), 'expense')
        self.assertEqual(transaction_description.get_attribute('innerHTML'), 'Phone Bill')
        self.assertEqual(transaction_size.get_attribute('innerHTML'), '-15')
        self.assertEqual(balance.get_attribute('innerHTML'), '1085')

        # user reloads page - should see existing transactions already created
        self.browser.refresh();        

        transactions_table = self.browser.find_element_by_id('transactions-table')
        transactions = transactions_table.find_elements_by_css_selector('.transaction')
        self.assertEqual(len(transactions), 3)

        # should be the salary transaction
        transaction = transactions[0]
        transaction_date = transaction.find_element_by_id('transaction-date')
        transaction_type = transaction.find_element_by_id('transaction-type')
        transaction_description = transaction.find_element_by_id('transaction-description')
        transaction_size = transaction.find_element_by_id('transaction-size')
        balance = transaction.find_element_by_id('balance')

        self.assertEqual(transaction_date.get_attribute('innerHTML'), yesterday.isoformat())
        self.assertEqual(transaction_type.get_attribute('innerHTML'), 'income')
        self.assertEqual(transaction_description.get_attribute('innerHTML'), 'Salary')
        self.assertEqual(transaction_size.get_attribute('innerHTML'), '1000')
        self.assertEqual(balance.get_attribute('innerHTML'), '1000')

        # should be the first transaction
        transaction = transactions[1]
        transaction_date = transaction.find_element_by_id('transaction-date')
        transaction_type = transaction.find_element_by_id('transaction-type')
        transaction_description = transaction.find_element_by_id('transaction-description')
        transaction_size = transaction.find_element_by_id('transaction-size')
        balance = transaction.find_element_by_id('balance')

        self.assertEqual(transaction_date.get_attribute('innerHTML'), today.isoformat())
        self.assertEqual(transaction_type.get_attribute('innerHTML'), 'income')
        self.assertEqual(transaction_description.get_attribute('innerHTML'), 'Description')
        self.assertEqual(transaction_size.get_attribute('innerHTML'), '100')
        self.assertEqual(balance.get_attribute('innerHTML'), '1100')

        # should be the phone bill transaction
        transaction = transactions[2]
        transaction_date = transaction.find_element_by_id('transaction-date')
        transaction_type = transaction.find_element_by_id('transaction-type')
        transaction_description = transaction.find_element_by_id('transaction-description')
        transaction_size = transaction.find_element_by_id('transaction-size')
        balance = transaction.find_element_by_id('balance')

        self.assertEqual(transaction_date.get_attribute('innerHTML'), today.isoformat())
        self.assertEqual(transaction_type.get_attribute('innerHTML'), 'expense')
        self.assertEqual(transaction_description.get_attribute('innerHTML'), 'Phone Bill')
        self.assertEqual(transaction_size.get_attribute('innerHTML'), '-15')
        self.assertEqual(balance.get_attribute('innerHTML'), '1085')
        
# Unit tests tell a developer that the code is doing things right; functional tests tell a developer that the code is doing the right things.
# import datetime, time
# from django.test import TestCase
#
# # Create your tests here.
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
#
# from django.test import LiveServerTestCase
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
#
# DEFAULT_TIMEOUT = 1
#
# def wait_for_element_with_id(browser, element_id, timeout=DEFAULT_TIMEOUT):
#     return WebDriverWait(browser, timeout=timeout).until(
#         lambda b: b.find_element_by_id(element_id),
#         'Could not find element with id: {}. Page text was:\n{}'.format(
#             element_id, browser.find_element_by_tag_name('body').text
#         )
#     )
#
#class FunctionalTest(LiveServerTestCase):
# class FunctionalTest(StaticLiveServerTestCase):
#
#     def setUp(self):
#         self.browser = webdriver.Chrome()
#         # self.browser = webdriver.Firefox()
#         # self.today = datetime.date(2017, 1, 24)
#         self.today = datetime.date.today()
#
#     def tearDown(self):
#         self.browser.quit()
#
#     def wait_for_element_with_id(self, element_id, timeout=DEFAULT_TIMEOUT):
#         return wait_for_element_with_id(self.browser, element_id, timeout)
#
#     def test_new_entry(self):
#         INITIAL_BALANCE = 4344.40
#
#         # david loads the homepage
#         self.browser.get(self.live_server_url)
#         self.assertEqual(self.browser.title, 'Voong Finance')
#
#         # it's his first time to the site # TODO: sign in, sessions, welcome page, etc
#         # he is invited to initialise his balance or to "do it later"
#         initialise_balance = self.wait_for_element_with_id('balance-initialisation')
#         input_field = initialise_balance.find_element_by_id('input')
#         submit_button = initialise_balance.find_element_by_id('submit-button')
#         date = initialise_balance.find_element_by_id('date')
#         date.send_keys(self.today.isoformat())
#
#         # he inputs his balance as 4344.40 GBP and hits ok/next/done button
#         input_field.send_keys(str(INITIAL_BALANCE))
#
#         # He clicks the submit button
#         submit_button.click()
#
#         # A blance chart appears at the top of the page
#         balance_chart = self.wait_for_element_with_id('balance-chart')
#
#         # The balance chart shows
#         bars = balance_chart.find_elements_by_css_selector('.bar');
#         self.assertEqual(len(bars), 28)
#
#         self.assertEqual(bars[1].get_attribute('balance'), str(INITIAL_BALANCE))
#         self.assertEqual(bars[-1].get_attribute('balance'), str(INITIAL_BALANCE))
#
#         # the initial balance prompt should have disappeared
#         with self.assertRaises(NoSuchElementException):
#             self.browser.find_element_by_id('balance-initialisation')
#
#         # a navbar appears at the top
#         navbar = self.browser.find_element_by_id('navbar')
#
#         # the navbar contains a logo which presumably takes the user back to the homepage TODO: test for the logo
#         logo = navbar.find_element_by_id('logo')
#
#         # the navbar contains a 'create transaction' button
#         create_transaction_btn = navbar.find_element_by_id('create-transaction-btn')
#
#         # the navbar contains other typical navigation buttons
#         # TODO: other navbar things, e.g. contact, settings/profile, transaction_history maybe
#
#         # a calendar view appears below the chart
#         calendar = self.browser.find_element_by_id('calendar')
#
#         # he is now invited to create his first entry
#         # perhaps a popup appears over a highlighted transaction button or the rest of the page is dimmed
#         first_entry_prompt = self.get_first_entry_prompt()
#
#         # a transaction form appears
#         transaction_form = first_entry_prompt.find_element_by_id('transaction-form')
#
#         # the date for the transaction is set to today
#         today = datetime.date.today()
#         year_selector = transaction_form.find_element_by_id('date-selector_year');
#         self.assertEqual(year_selector.get_attribute('value'), str(today.year))
#         month_selector = transaction_form.find_element_by_id('date-selector_month');
#         self.assertEqual(month_selector.get_attribute('value'), str(today.month))
#         day_selector = transaction_form.find_element_by_id('date-selector_day');
#         self.assertEqual(day_selector.get_attribute('value'), str(today.day))
#
#         # david sets transaction type to expense
#         transaction_type_dropdown = transaction_form.find_element_by_id('transaction-type-dropdown')
#         Select(transaction_type_dropdown).select_by_visible_text('Expense')
#
#         # david types name as phone bill
#         transaction_description = transaction_form.find_element_by_id('transaction-description')
#         transaction_description.send_keys('New Phone')
#
#         # david sets the date to next week
#         transaction_date = self.today + datetime.timedelta(days=7)
#         year_selector.send_keys(str(transaction_date.year))
#         month_selector.send_keys(transaction_date.strftime("%B"))
#         day_selector.send_keys(str(transaction_date.day))
#
#         # david enters the amount as 719.99
#         transaction_size_input = transaction_form.find_element_by_id('transaction-size-input')
#         transaction_size_input.send_keys('719.99')
#
#         # david clicks the create transaction button
#         create_transaction_btn = transaction_form.find_element_by_id('create-transaction-btn')
#         create_transaction_btn.click()
#
#         # the first transaction prompt disappears
#         WebDriverWait(self.browser, 5).until_not(EC.presence_of_element_located(('id', 'first-entry-prompt')))
#
#         # The balance chart updates
#         # bars = balance_chart.find_elements_by_css_selector('.bar[date="{}"]'.format(date))
#         bars = balance_chart.find_elements_by_css_selector('.bar')
#         bar = [bar for bar in bars if bar.get_attribute('date') == transaction_date.isoformat()]
#         self.assertEqual(len(bar), 1)
#         bar = bar[0]
#         self.assertEqual(bar.get_attribute('balance'), str(INITIAL_BALANCE - 719.99))
#
#         # the range of dates should be unchanged
#         bars[0].get_attribute('date') == self.today.isoformat()
#         bars[0].get_attribute('balance') == INITIAL_BALANCE
#         self.assertEqual(len(bars), 28)
#
#         # next week shows the balance as 4329.40, this is true for dates following it also
#         bars[-1].get_attribute('date') == (self.today + datetime.timedelta(days=27)).isoformat()
#         bars[-1].get_attribute('balance') == str(INITIAL_BALANCE - 719.99)
#
#         # the dates between today and next week show the original balance (inclusive of today, exclusive of next week)
#         bars[6].get_attribute('date') == (self.today + datetime.timedelta(days=6)).isoformat()
#         bars[6].get_attribute('balance') == str(INITIAL_BALANCE)
#         bars[7].get_attribute('date') == transaction_date.isoformat()
#         bars[7].get_attribute('balance') == str(INITIAL_BALANCE - 719.99)
#
#         # David reloads the page
#         self.browser.get(self.live_server_url)
#
#         # instead of seeing the welcome screen he sees the existing balance chart
#         WebDriverWait(self.browser, 1).until_not(EC.presence_of_element_located(('id', 'balance-initialisation')))
#
#         # The balance chart should be centred around today
#
#         balance_chart = WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located(('id', "balance-chart")))
#         WebDriverWait(balance_chart, 1).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, ".bar")))
#         bars = balance_chart.find_elements_by_css_selector('.bar')
#         self.assertEqual(len(bars), 28)
#         bar = bars[13]
#         self.assertEqual(bar.get_attribute('date'), datetime.date.today().isoformat())
#
#         # bars should have the same values
#         map(lambda bar: self.assertEqual(bar.get_attribute('balance'), str(INITIAL_BALANCE - 719.99)), bars)
#
#         # the calendar view also shows a new entry on the date for next week
#         calendar = self.browser.find_element_by_id('calendar')
#         dates = calendar.find_element_by_css_selector('.date');
#
#         # add transaction for pay day
#         tomorrow = datetime.date.today() + datetime.timedelta(days=1)
#         transaction_form = TransactionForm(self.browser)
#         self.assertEqual(transaction_form.year_widget.get_attribute('value'), str(today.year))
#         self.assertEqual(transaction_form.month_widget.get_attribute('value'), str(today.month))
#         self.assertEqual(transaction_form.day_widget.get_attribute('value'), str(today.day))
#         create_transaction(transaction_form, type='Income', description='Pay Day', date=tomorrow, transaction_size=3000)
#
#         import time
#         time.sleep(1)
#
#         # he sees the balance chart has been updated
#         balance_chart = BalanceChart(self.browser)
#         self.assertEqual(balance_chart.dates[13], self.today)
#         self.assertEqual(balance_chart.balances[13], INITIAL_BALANCE)
#         self.assertEqual(balance_chart.dates[14], tomorrow)
#         self.assertEqual(balance_chart.balances[14], INITIAL_BALANCE + 3000)
#         self.assertEqual(balance_chart.dates[20], datetime.date.today() + datetime.timedelta(days=7))
#         self.assertEqual(balance_chart.balances[20], INITIAL_BALANCE + 3000 - 719.99)
#
#         # bug: Add transaction on initialise date will remove the initialisation
#         print('today:', self.today)
#         transaction_form = TransactionForm(self.browser)
#         create_transaction(transaction_form, type='Expense', description='Chicken', date=self.today, transaction_size=2.99)
#         time.sleep(1)
#
#         balance_chart = BalanceChart(self.browser)
#         self.assertEqual(balance_chart.dict[self.today],INITIAL_BALANCE - 2.99)
#
#         # delete transactions
#
#         # scale rescales when min/max balance outside original range
#
#         # move forwards and backwards in time
#
#         # hover tool
#
#         # repeat transactions
#         # repeating_transaction_checkbox.find_element_by_id('repeating-transaction-checkbox')
#         # repeating_transaction_checkbox.click()
#         # repeat_frequency_dropdown = transaction_form.find_element_by_id('repeat-frequency-dropdown')
#         # Select(repeat_frequency_dropdown).select_by_visible_text('Monthly')
#
#         # transaction view
#
#         self.assertEqual(1, 0, 'Finish functional tests')
#
#     def get_first_entry_prompt(self):
#         return self.browser.find_element_by_id('first-entry-prompt')
#
# def create_transaction(form, type, description, date, transaction_size):
#     print('create_transaction')
#     print('date:', date)
#
#     Select(form.type_widget).select_by_visible_text(type)
#     form.description_widget.send_keys(description)
#     form.year_widget.send_keys(date.year)
#     form.month_widget.send_keys(date.strftime("%B"))
#     print(str(date.day))
#     print(form.day_widget.get_attribute('value'))
#     form.day_widget.send_keys(str(date.day))
#     print(str(date.day))
#     print(form.day_widget.get_attribute('value'))
#
#     form.transaction_size_widget.send_keys(str(transaction_size))
#     time.sleep(5)
#     form.create_transaction_btn.click()
#
# class TransactionForm:
#
#     def __init__(self, browser):
#         browser.find_element_by_id('create-transaction-btn').click()
#         self.form = WebDriverWait(browser, timeout=5).until(lambda b: b.find_element_by_id('transaction-form'))
#         self.type_widget = self.form.find_element_by_id('transaction-type-dropdown')
#         self.description_widget = self.form.find_element_by_id('transaction-description')
#         self.year_widget = self.form.find_element_by_id('date-selector_year');
#         self.month_widget = self.form.find_element_by_id('date-selector_month');
#         self.day_widget = self.form.find_element_by_id('date-selector_day');
#         self.transaction_size_widget = self.form.find_element_by_id('transaction-size-input')
#         self.create_transaction_btn = self.form.find_element_by_id('create-transaction-btn')
#
# class BalanceChart:
#
#     def __init__(self, browser):
#         self.balance_chart = wait_for_element_with_id(browser, 'balance-chart')
#         self.bars = self.balance_chart.find_elements_by_css_selector('.bar')
#         self.dates = [datetime.datetime.strptime(bar.get_attribute('date'), '%Y-%m-%d').date() for bar in self.bars]
#         self.balances = [float(bar.get_attribute('balance')) for bar in self.bars]
#         self.dict = {date: balance for date, balance in zip(self.dates, self.balances)}
