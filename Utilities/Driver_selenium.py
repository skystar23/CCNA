import io
import json
import platform
import re
import subprocess
import time

import allure
import pingparsing
import pyautogui
# from allure import attachment_type
# from allure.types import AttachmentType
from allure_commons.types import AttachmentType
from pynput.keyboard import Key, Controller
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from Utilities.Dynamicdata import Dynamicdata


def traceroute_checking(target,version = 'ipv4'):
    print(f"Performing traceroute to {target}...")
    
    # Check the OS and select the command accordingly
    if platform.system() == "Windows":
        if version.lower() == "ipv4":
            command = ["tracert", target]  # Use tracert for Windows
        else:
            command = ["tracert6", target]
    else:
        if version.lower() == "ipv4":
            command = ["traceroute", target]  # Use traceroute for Linux/Ubuntu
        else:
            command = ["traceroute6", target]
    try:
        # Run the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Return the output as a string
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Traceroute failed: {e}"
    except FileNotFoundError:
        return "Traceroute/tracert command not found. Please make sure it's installed."


def ping_checking(ipaddress):
    """This function is used for ping checking for an ip address nd return success or fail"""
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = ipaddress
    transmitter.count = 5
    result = transmitter.ping()
    t = (json.dumps(ping_parser.parse(result).as_dict(), indent=4))
    pingdir = json.loads(t)
    if int(pingdir["packet_loss_rate"]) <= 50 and pingdir["rtt_min"] is not None:
        k = "success"
    else:
        k = "fail"
    return k
    
def fileupload(file):
    keyboard = Controller()
    keyboard.type(str(file))
    time.sleep(5)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    
def ping_checking_with_result(ipaddress):
    """This function is used for ping checking for an ip address nd return success or fail"""
    print(f'started ping checking for 100 packets for ip address :{ipaddress}')
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = ipaddress
    transmitter.count = 100
    result = transmitter.ping()
    t = (json.dumps(ping_parser.parse(result).as_dict(), indent=4))
    pingdir = json.loads(t)
    if int(pingdir["packet_loss_rate"]) <= 50 and pingdir["rtt_min"] is not None:
        k = "pass"
    else:
        k = "fail"
    print(f'ping packet loss {pingdir["packet_loss_rate"]} for ip address :{ipaddress}')
    return k,pingdir

def json_reading(filename):
    json_file = open(filename, 'r')
    elements = json.load(json_file)
    json_file.close()
    return elements


class Driver_selenium:
    """This class is used to handle all the driver related methods use this class by creating object and access all methods"""
    def __init__(self, browser):
        """Use to open browser as per the request from user"""
        if browser.upper() == 'FIREFOX':
           self.driver = webdriver.Firefox()
        elif browser.upper() == 'CHROME':
            self.driver = webdriver.Chrome()
        elif browser.upper() == 'EDGE':
            self.driver = webdriver.Edge()
        else:
            self.driver = None
    
    def page_Zoom_IN_OUT(self,value):
        self.driver.execute_script(f"document.body.style.zoom='{value}%'")


    def driver_refresh(self):
        "this Method is refresh current page"
        self.driver.refresh()

    def text_box(self, locator_name, locator_value, input_data):
        """This method is used to fill textbox uses sendkeys to write into page input_data as string if we set Enter and Space just set input_data to space or enter if u want any special keys change condition """
        if input_data.upper() == "ENTER" or input_data.upper() == "SPACE":
            self.driver.find_element(eval("By." + locator_name), locator_value).send_keys(eval(f"Keys.{input_data.upper()}"))
        elif input_data.upper() == 'EMPTY':
            self.driver.find_element(eval("By." + locator_name), locator_value)
        else:
            self.driver.find_element(eval("By." + locator_name), locator_value).send_keys(f"{input_data}")
        time.sleep(0.5)

    def drop_down(self, locator_name, locator_value, input_data, locator_type):
        """This method is used to handle dropdown by text or value or index position"""
        drop = Select(self.driver.find_element(eval("By." + locator_name), locator_value))
        if locator_type.upper() == "TEXT":
            drop.select_by_visible_text(input_data)
        elif locator_type.upper() == "VALUE":
            drop.select_by_value(input_data)
        elif locator_type.upper() == "INDEX":
            drop.select_by_index(input_data)
        time.sleep(0.5)

    def selected_option_drop_down(self, locator_name, locator_value):
        """This method is used to get selected value from the dropdown""" "(added by Guru)"
        sel_ele = self.driver.find_element(eval("By." + locator_name), locator_value);
        sel_val = sel_ele.get_attribute("value")
        dropdown = Select(sel_ele)

        selected_text = ""
        for option in dropdown.options:
            if option.get_attribute("value") == sel_val:
                selected_text = option.get_attribute("innerHTML")
                break
       
        #print("selected text is : ",k.text,"selected_dropdown")
        #print("dropdown id is",select_element.get_attribute('innerHTML'))
        #print(selected_text,"selected_dropdown")

        return selected_text

    #def selected_option_drop_down(self, locator_name, locator_value):
    #drop = Select(self.driver.find_element(eval("By." + locator_name), locator_value))
      # k = select_element.first_selected_option
      # return k.text

    def read_drop_down(self, locator_name, locator_value, locator_type):
        """This method is used to get list dropdown options"""
        drop = Select(self.driver.find_element(eval("By." + locator_name), locator_value))
        dropdown_elements = drop.options
        data = []
        if locator_type.upper() != "TEXT":
            for element in dropdown_elements:
                data.append(element.get_attribute(f'{locator_type}'))
            time.sleep(0.5)
        else:
            for element in dropdown_elements:
                data.append(element.text)
            time.sleep(0.5)
        return data

    def button(self, locator_name, locator_value):
        """This method is """
        self.driver.find_element(eval("By." + locator_name), locator_value).click()
        time.sleep(0.5)

    def drop_check(self, locator_name, locator_value, locator_name1, locator_value1):
        """This method is used for dropdown with checkboxes"""
        self.button(locator_name, locator_value)
        for i in locator_value1:
            self.button(locator_name1, i.strip())
        self.button(locator_name, locator_value)
        time.sleep(0.5)

    def side_menu(self, locator_name, locator_value):
        """This method is used to click side menu like network,services etc."""
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame("SideMenuFrame")
        self.button(locator_name, locator_value)
        self.driver.switch_to.default_content()
        time.sleep(0.5)

    def menu_with_submenu(self, locator_name, locator_value, locator_name1, locator_value1):
        """This method is used to click from menu and clik submenu"""
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame("menubarFrame")
        self.button(locator_name, locator_value)
        self.button(locator_name1, locator_value1)
        self.driver.switch_to.default_content()
        time.sleep(0.5)

    def file_send_selenium(self, locator_name, locator_value, filename):
        self.driver.execute_script(";", self.text_box(locator_name=locator_name, locator_value=locator_value,
                                                      input_data=filename))

    def menu_with_submenu_submenu(self, locator_name, locator_value, locator_name1, locator_value1, locator_name2, locator_value2):
        """This method is used to click from menu and clik submenu"""
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame("menubarFrame")
        self.button(locator_name, locator_value)
        self.button(locator_name1, locator_value1)
        self.button(locator_name2,locator_value2)
        self.driver.switch_to.default_content()
        time.sleep(0.5) 

    def main_page(self):
        """This is method is move your cursor to main protocol page"""
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame("menubarFrame")
        self.driver.switch_to.frame("displayframe")
        time.sleep(5)

    def read_popup(self, name=None):
        """This method is handle popup is reads and accept the popup and return the popup text"""
        aletmsg = self.driver.switch_to.alert
        aletmsg1 = aletmsg.text
        self.allure_capture(name)
        time.sleep(1)
        aletmsg.accept()
        time.sleep(0.5)
        return aletmsg1

    def menu_without_submenu(self, locator_name, locator_value):
        """This method is used to click only pages without any submenu in it"""
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame("menubarFrame")
        self.button(locator_name, locator_value)
        # self.driver.find_element(eval("By." + locator_name1), locator_value1).click()
        self.driver.switch_to.default_content()
        time.sleep(0.5)

    def read_error_page(self, locator_name, locator_value):
        """This method is used to popup pages"""
        return self.driver.find_element(eval("By." + locator_name), locator_value).text

    def get_value_text_box(self, locator_name, locator_value):
        """This method is used to read only value of the text_box"""
        return self.driver.find_element(eval("By." + locator_name), locator_value).get_attribute("value")

    def get_text_box(self, locator_name, locator_value, value):
        """This method is used to read all attributes of the text_box"""
        return self.driver.find_element(eval("By." + locator_name), locator_value).get_attribute(f"{value}")

    def clear_text_box(self, locator_name, locator_value):
        """This method clear data from the textbox"""
        return self.driver.find_element(eval("By." + locator_name), locator_value).clear()

    def url_open(self, path, locator_name, locator_value, logger):
        """This method is used to open Url for the given ip address"""
        i = 1
        locator_names = locator_name.split(',')
        locator_values = locator_value.split(',')
        if len(locator_names) != len(locator_values):
            if len(locator_names) < len(locator_values):
                locator_names.append('')
            elif len(locator_names) > len(locator_values):
                locator_values.append('')
        self.driver.get(f'{path}')
        for index in range(len(locator_names)):
            i = 1
            while i < 4:
                # Wait for the presence of a specific element on the page.
                try:
                    self.locator_check_with_time(locator_names[index],locator_values[index],timeout=5)
                    print("Page loaded successfully!")
                    logger.info("Device Page loaded successfully!")
                    return True
                except Exception:
                    # print(e)
                    try:
                        message = self.Welcome()
                        if message == "Welcome":
                            logger.info("Device already  in login")
                            print("Device already in login")
                            return False
                        else:
                            logger.error("Timed out waiting for page to load.")
                            print(f"{i}.Timed out waiting for page to load.")
                            self.driver.refresh()
                    except:
                        logger.error("Timed out waiting for page to load.")
                        print(f"{i}.Timed out waiting for page to load.")
                        self.driver.refresh()
                    i += 1
            if i == 4 and index == len(locator_names) - 1:
                return None

    def driver_close(self):
        """This method is used to close the browser"""
        self.driver.quit()

    def Current_url(self):
        """This method is used to read current url of the page"""
        return self.driver.current_url

    def Welcome(self):
        """This welcome method is used to read welcome page of the devices"""
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame("menubarFrame")
        self.driver.switch_to.frame("displayframe")
        time.sleep(2)
        k = self.driver.find_element(By.XPATH, "/html/body/div/p[1]")
        return k.text

    def scrolling_page_down(self):
        """This method is used to scroll page down"""
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    def scrolling_same_page(self, action="down"):
        """This method is used to scroll in the same page up and down"""
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame("menubarFrame")
        if action == "down":
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        else:
            self.driver.execute_script("window.scrollTo(0,0)")
        # time.sleep(0.5)

    def scrolling_page_up(self):
        """This method is used to scroll page to up"""
        self.driver.execute_script("window.scrollTo(0,0)")

    def locator_check_with_size(self, locator_name, locator_value):
        try:
            return True if len(self.driver.find_elements(eval("By." + locator_name), locator_value)) > 0 else False
        except:
            return False

    def locator_check_with_time(self,locator_name, locator_value,timeout):
        """This method used to check the element with time visibility_of_element_located"""
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((eval("By." + locator_name), locator_value)))

    def scrolling_into_locator(self, locator_name, locator_value, action="down"):
        """This method is used to scroll into element default it scroll down we can change to up"""
        if action == "down":
            self.driver.execute_script("arguments[0].scrollIntoView();",
                                       self.driver.find_element(eval("By." + locator_name), locator_value))
        else:
            self.driver.execute_script("arguments[0].scrollIntoView(false)",
                                       self.driver.find_element(eval("By." + locator_name), locator_value))
        # time.sleep(0.5)

    def IsEnabled(self, locator_name, locator_value):
        """This method is used to find sider is enabled or not """
        return self.driver.find_element(eval("By." + locator_name), locator_value).is_selected()

    def script_click(self, locator_name, locator_value):
        """This method is used to click multiple sliders"""
        self.driver.execute_script("arguments[0].click();",
                                   self.driver.find_element(eval("By." + locator_name), locator_value))

    def locator_isdisplayed(self,locator_name,locator_value):
        return self.driver.find_element(eval("By." + locator_name), locator_value).is_displayed()

    def locator_present(self, locator_name, locator_value):
        """"This method is used to check locator is present or not with size"""
        i = 1
        while i < 4:
            # Wait for the presence of a specific element on the page.
            if self.locator_check_with_size(locator_name, locator_value):
                self.scrolling_into_locator(locator_name, locator_value)
                # if self.locator_isdisplayed(locator_name, locator_value):
                return True
                # else:
            else:
                print(f"{i}.waiting for element {locator_name} {locator_value}")
                try:
                    self.scrolling_into_locator(locator_name, locator_value)
                except:
                    try:
                        self.scrolling_same_page()
                        self.main_page()
                    except:
                        self.scrolling_page_down()
            i = i + 1
        return False

    def locator_present_time(self, locator_name, locator_value, timeout=2):
        """This method is used to locate the locator based on  time"""
        i = 1
        update = False
        while i < 4:
            # Wait for the presence of a specific element on the page.
            try:
                self.locator_check_with_time(locator_name, locator_value, timeout)
                update = True
                break
            except TimeoutException:
                print(f"{i}.waiting for element {locator_name} {locator_value}")
                try:
                    self.scrolling_into_locator(locator_name, locator_value)
                except:
                    try:
                        self.scrolling_same_page()
                        self.main_page()
                    except:
                        self.scrolling_page_down()
                i = i + 1
        if update:
            return True
        else:
            return False

    def screen_short(self):
        """This method is used to capture the screenshot"""
        # Take a screenshot using PyAutoGUI
        screenshot = pyautogui.screenshot()

        # Create a BytesIO object to store the screenshot as bytes
        byte_io = io.BytesIO()

        # Save the screenshot as PNG to the byte stream
        screenshot.save(byte_io, format='PNG')

        # Get the byte content of the screenshot
        screenshot_bytes = byte_io.getvalue()

        return screenshot_bytes

    def reading_table(self, locator_name, locator_value):
        """This method is used to read table and convert into dictionary"""
        values = self.driver.find_elements(eval("By." + locator_name), locator_value)
        k, data1 = [], {}
        for i in values:
            j = i.find_elements(By.TAG_NAME, "td")
            for m in j:
                k.append(m.text)
        data1.update(dict(zip(k[::2], k[1::2])))
        return data1

    def allure_capture(self, name):
        """This method is used to capture the screenshot using allure"""
        # allure.attach(self.screen_short(), name=f'{Dynamicdata.dateandtime()}:{name}', attachment_type=AttachmentType.PNG)
        pass

    @staticmethod
    def allure_capture_file(filename):
        allure.attach.file(f'./Reports/{filename}',name=filename, extension="xlsx")

    @staticmethod
    def allure_capture_video(videoname):
        allure.attach.file(f'./Reports/{videoname}', name=videoname, extension="mp4",attachment_type=AttachmentType.MP4)

    def checking_locators(self, locator_name, locator_value, rowid):
        elements = locator_name.split(',')
        values = locator_value.split(',')
        if len(elements) != len(values):
            if len(elements) < len(values):
                elements.append('')
            elif len(elements) > len(values):
                values.append('')
        for index in range(len(elements)):
            try:
                if rowid != 0:
                    if self.locator_present(elements[index], values[index].strip('"').strip("'") + str(rowid)):
                        return elements[index], values[index].strip('"').strip("'") + str(rowid)
                else:
                    if self.locator_present(elements[index], values[index].strip('"').strip("'")):
                        return elements[index], values[index].strip('"').strip("'")
            except Exception as e:
                print(e)
                print(f"Trying with {index + 1} new element")
        return False

    def reading_page_tables(self,locator_name, locator_value):
        # Locate the table (you can locate by class, id, or any other selector)
        table = self.driver.find_element(eval("By." + locator_name), locator_value)
        # Find all rows in the table (tr tags)
        rows = table.find_elements(By.TAG_NAME, 'tr')
        # Get the number of rows
        num_rows = len(rows)-1
        return num_rows

    def reading_table_filled_data(self):
        time.sleep(5)
        script_tags = self.driver.find_elements(By.TAG_NAME, "script")
        # Search for the script containing "fillrow"
        fillrow_calls = []
        for script in script_tags:
            script_content = script.get_attribute("innerHTML")
            # Use regex to find all fillrow calls
            matches = re.findall(r"fillrow\(([^)]+)\)", script_content)
            if matches:
                fillrow_calls.extend(matches)
        # Parse fillrow data
        fillrow_data = {}
        key_dic=1
        for call in fillrow_calls:
            # Split the arguments by comma and remove quotes/whitespace
            args = [arg.strip().strip("'\"") for arg in call.split(",")]
            # The first argument is the key, the rest are values
            # key = args[0]
            # values = args[1:]
            # fillrow_data[key] = values
            # Print the extracted data
            fillrow_data[key_dic]=args
            key_dic += 1
        if fillrow_data:
            return fillrow_data
        else:
            return "No fillrow calls found."

    def reading_column_values(self,locator_name, locator_value,locator_value1,column_value):
        table = self.driver.find_element(eval("By." + locator_name), locator_value)
        # Find all rows in the table (tr tags)
        rows = table.find_elements(By.TAG_NAME, 'tr')
        value = []
        index_value1 = 0
        # Loop through each row (skip the header row if needed)
        for index , row in enumerate(rows):
            if index != 0:
                # Find all columns in the current row (td tags)
                columns = row.find_elements(By.TAG_NAME, locator_value1)
            else:
                columns = row.find_elements(By.TAG_NAME, 'th')
            # Loop through each column in the row and print the text
            for index_value, column in enumerate(columns):
                if index == 0 :
                    if column_value.upper() == column.text.upper():
                        # print(f"Row {rows.index(row) + 1}, Column {index_value + 1}: {column.text}")
                        index_value1 = index_value
                else:
                    if index_value1 == index_value:
                        print(column.find_elements(By.XPATH,".//child::*")[0].get_attribute("value"))
                        value.append(column.find_elements(By.XPATH,".//child::*")[0].get_attribute("value"))
        return value
    
    def is_alert_present(self):
        try:
            # Try switching to alert
            self.driver.switch_to.alert
            return True  # Alert is present
        except NoAlertPresentException:
            return False 
    
    def driver_screenshot(self,filename):
        self.driver.save_full_page_screenshot(f"{filename}.png")


    def driver_screenshot_page(self,filename):
        self.scrolling_page_up()
        #self.scrolling_same_page()
        self.driver.save_screenshot(f"{filename}.png")
    

    def reading_column_values_status(self,locator_name, locator_value,locator_value1,column_value):
        table = self.driver.find_element(eval("By." + locator_name), locator_value)
        # Find all rows in the table (tr tags)
        rows = table.find_elements(By.TAG_NAME, 'tr')
        value = []
        index_value1 = 0
        # Loop through each row (skip the header row if needed)
        for index , row in enumerate(rows):
            if index != 0:
                # Find all columns in the current row (td tags)
                columns = row.find_elements(By.TAG_NAME, locator_value1)
            else:
                columns = row.find_elements(By.TAG_NAME, 'th')
            # Loop through each column in the row and print the text
            for index_value, column in enumerate(columns):
                if index == 0 :
                    if column_value.upper() == column.text.upper():
                        # print(f"Row {rows.index(row) + 1}, Column {index_value + 1}: {column.text}")
                        index_value1 = index_value
                else:
                    if index_value1 == index_value:
                        value.append(column.text)
        return value
    def read_lable(self,locator_name, locator_value):
        return self.driver.find_element(eval("By." + locator_name), locator_value).text


    