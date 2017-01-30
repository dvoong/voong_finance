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

        # david loads the homepage
        self.browser.get(self.live_server_url)
        self.assertEqual(self.browser.title, 'Voong Finance')

        # it's his first time to the site # TODO
        # he is invited to initialise his balance or to "do it later"
        # he inputs his balance as 4344.40 GBP and hits ok/next/done button
        # A blance chart appears at the top of the page
        # On the x axis is date
        # the chart is centred around today's date
        # David is viewing the website on his laptop, i.e. his window width is big* (TODO: be more specific)
        # 15 days prior are shown on the left
        # 15 days in the future are shown on the right
        # today'date is highlighted or emphasised in some way
        # the y axis show's the balance of their account
        # the dates before today have the value 0 GBP
        # the dates in the future all have the value of 4344.40 GBP
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
        # 

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
