from model.contact import Contact
import time

class Contacthelper:
    def __init__(self, app):
        self.app= app

    def open_home_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith('addressbook/') and len(wd.find_elements_by_name("searchstring")) > 0):
            wd.find_element_by_link_text("home").click()

    def create(self, contact):
        wd = self.app.wd
        self.open_home_page()
        wd.find_element_by_link_text("add new").click()
        self.fill_forms(contact)
        wd.find_element_by_xpath("(//input[@name='submit'])[2]").click()
        self.open_home_page()
        self.contact_cache = None

    def edit_first(self, contact):
        wd = self.app.wd
        self.open_home_page()
        wd.find_element_by_xpath("//img[@alt='Edit']").click()
        self.fill_forms(contact)
        wd.find_element_by_name('update').click()
        self.contact_cache = None

    def fill_forms(self, contact):
        wd = self.app.wd
        self.change_field_value('firstname', contact.firstname)
        self.change_field_value('middlename', contact.middlename)
        self.change_field_value('lastname', contact.lastname)
        self.change_field_value('nickname', contact.nickname)
        self.change_field_value('title', contact.title)
        self.change_field_value('company', contact.company)
        self.change_field_value('address', contact.address)
        self.change_field_value('home', contact.home)
        self.change_field_value('mobile', contact.mobile)
        self.change_field_value('work', contact.work)
        self.change_field_value('fax', contact.fax)
        self.change_field_value('email', contact.email)
        self.change_field_value('email2', contact.email2)
        self.change_field_value('email3', contact.email3)
        self.change_field_value('homepage', contact.homepage)
        self.change_field_value('address2', contact.address2)
        self.change_field_value('phone2', contact.phone2)
        self.change_field_value('notes', contact.notes)
        self.change_field_value('notes', contact.email)


    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def delete_first(self):
        wd = self.app.wd
        self.open_home_page()
        # выбрать первый контакт
        wd.find_element_by_name('selected[]').click()
        # подтвердить удаление
        wd.find_element_by_xpath("// input[ @ value = 'Delete']").click()
        wd.switch_to_alert().accept()
        self.open_home_page()
        self.contact_cache = None

    def return_homepage(self):
        wd = self.app.wd
        if not (wd.current_url.endswith('addressbook/') and len(wd.find_elements_by_name("searchstring")) > 0):
            wd.find_element_by_link_text("home page").click()

    def count(self):
        wd = self.app.wd
        self.return_homepage()
        return len(wd.find_elements_by_name('selected[]'))

    contact_cache = None

    def get_contacts_list(self):
        if self.contact_cache is None:
            wd = self.app.wd
            self.open_home_page()
            self.contact_cache = []
            for element in wd.find_elements_by_name('entry'):
                firstname_text = element.find_element_by_xpath('.//td[3]').text
                lastname_text = element.find_element_by_xpath('.//td[2]').text
                id= element.find_element_by_name('selected[]').get_attribute('value')
                self.contact_cache.append(Contact(firstname=firstname_text, lastname=lastname_text, id=id))
        return list(self.contact_cache)
