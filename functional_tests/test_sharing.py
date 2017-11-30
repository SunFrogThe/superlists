from selenium import webdriver

from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage

EMAIL_EDITH = 'edith@example.com'
EMAIL_ONI = 'oniciferous@example.com'


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):

    def test_can_share_a_list_with_another_user(self):
        # edith is a logged-in user
        self.create_pre_authenticated_session(EMAIL_EDITH)
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        # her friend Oniciferous is also hanging out on the lists site
        oni_browser = webdriver.Chrome()
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.browser = oni_browser
        self.create_pre_authenticated_session(EMAIL_ONI)

        # Edith goes to the home page and starts a list
        self.browser = edith_browser
        list_page = ListPage(self).add_list_item('Get help')

        # She notices a "Share this list" option
        self.wait_for(lambda: self.assertIn(
            'Share this list with:',
            self.browser.find_element_by_tag_name('body').text
        ))
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )

        # She shares her list.
        list_page.share_list_with(EMAIL_ONI)

        # The page updates to say that it's shared with Oniciferous:
        self.wait_for(lambda: self.assertIn(
            f'List shared with {EMAIL_ONI}',
            self.browser.find_element_by_tag_name('body').text
        ))

        # Oniciferous now goes to the lists page with his browser
        self.browser = oni_browser
        MyListsPage(self).go_to_my_lists_page()

        # He sees Edith's list in there!
        self.browser.find_element_by_link_text('Get help').click()

        # On the list page, Oniciferous can see it says that it's Edith's list
        self.wait_for(lambda: self.assertEqual(
            list_page.get_list_owner(),
            EMAIL_EDITH
        ))

        # He adds an item to the list
        list_page.add_list_item('Hi Edith!')

        # When Edith refreshes the page, she sees Oniciferous's addition
        self.browser = edith_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('Hi Edith!', 2)
