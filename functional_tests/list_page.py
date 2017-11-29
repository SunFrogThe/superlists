from selenium.webdriver.common.keys import Keys
from .base import wait


class ListPage:

    def __init__(self, test):
        self.test = test

    def add_list_item(self, text):
        new_item_no = len(self.get_table_rows()) + 1
        self.get_item_input_box().send_keys(text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(text, new_item_no)
        return self

    @wait
    def wait_for_row_in_list_table(self, item_text, item_number):
        expected_row_text = f'{item_number}: {item_text}'
        rows = self.get_table_rows()
        self.test.assertIn(expected_row_text, [row.text for row in rows])

    def get_table_rows(self):
        return self.test.browser.find_elements_by_css_selector('#id_list_table tr')

    def get_item_input_box(self):
        return self.test.browser.find_element_by_id('id_text')
