from typing import Dict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
from time import sleep, strftime
import HTMLTestRunner
from selenium.webdriver.support.select import Select
from bbx_utils import switch_frame, getOriAdd


flow_info: Dict[str, None] = {"order_id": '1', "driver_phone": '18030142505'}


class TestFlow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://106.15.43.157:8083/login.html")
        cls.driver.maximize_window()
        cls.driver.find_element_by_id('username').send_keys("chenronghuai")
        cls.driver.find_element_by_id('userpwd').send_keys("asdf_123456")
        cls.driver.find_element_by_id('loginBtn').click()
        WebDriverWait(cls.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="mCSB_1_container"]/ul/li[1]/span')))
        WebDriverWait(cls.driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'layui-layer-setwin')))\
            .click()
        cls.driver.find_element_by_css_selector('img[src$="menu1.png"]').click()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
    '''
    def __init__(self):
        self.flow_info = {"order_id" : None, "driver_phone" : None}
    '''
    def driver_report(self, phone_number):

        switch_frame(self.driver, '[tit=司机报班]', '[tit=司机报班]', '[src="/driverReport.do"]')
        self.driver.find_element_by_id('phone').send_keys(phone_number)
        sleep(1)
        self.driver.find_element_by_id('query_driver').click()
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//tbody/tr/td[2]')))
        self.driver.find_element_by_xpath('//tbody/tr/td[15]/a[text()="报班"]').click()

        ori = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.ID, 'startName')))
        '''
        DOM树有相关suggest条目，即可点击方位
        '''
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@id="startName-suggest"]/div')))
        ori.click()

        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.ID, 'startName-suggest')))
        ori.send_keys('X')
        WebDriverWait(self.driver, 5).until(EC.text_to_be_present_in_element_value((By.ID, 'sel_origin'), "361000"))

        des = self.driver.find_element_by_id('endsName')
        '''
        DOM树有相关suggest条目，即可点击方位
        '''
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@id="endsName-suggest"]/div')))
        des.click()
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.ID, 'endsName-suggest')))
        des.send_keys('N')
        WebDriverWait(self.driver, 5).until(EC.text_to_be_present_in_element_value((By.ID, 'sel_destination'), "362300"))

        self.driver.find_element_by_id('report').click()
        sleep(2)
        flow_info['driver_phone'] = self.driver.find_element_by_xpath('//tbody/tr/td[4]').text
        return self.driver.find_element_by_xpath('//tbody/tr/td[10]').text

    def customer_call(self, c_phone):
        switch_frame(self.driver, '[tit=司机报班]', '[tit=客户来电]', '[src="/customerCall.do"]')

        e_number = self.driver.find_element_by_css_selector("#phone")
        e_number.clear()
        e_number.send_keys(c_phone)
        self.driver.find_element_by_css_selector("#query_all").click()
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="userInfoDiv"]/i[1]')))
#        ele_ori_bearing = self.driver.find_element(By.ID, 'startName')
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@id="startName-suggest"]/div')))
        self.driver.find_element(By.ID, 'startName').click()
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.ID, 'startName-suggest')))
        self.driver.find_element(By.ID, 'startName').send_keys('XM')
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="startName-suggest"]/div[@text="厦门市|XMCJ"]')),
            '起始方位无法获取').click()
        ele_ori_addr = self.driver.find_element_by_id('startAddr')

        ele_ori_addr.click()
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="start-lists-penal"]/li')))
        ele_ori_addr.send_keys('高林居住区')
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="start-lists-penal"]/li[1]')), '起点POI无法获取').click()
        self.oriAdd = self.driver.find_element_by_id('startAddr').get_attribute('addr_hidden')

#        ele_des_bearing = self.driver.find_element_by_id('endsName')
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@id="endsName-suggest"]/div')))
        self.driver.find_element_by_id('endsName').click()
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.ID, 'endsName-suggest')))
        self.driver.find_element_by_id('endsName').send_keys('NA')
        WebDriverWait(self.driver, 5).until_not(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="start-lists-penal"]/li[1]')), '起点信息还没消失')
        ele_des_addr = self.driver.find_element_by_id('endAddr')

        ele_des_addr.click()
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="end-lists-penal"]/li')))
        ele_des_addr.send_keys('东区小区')
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="end-lists-penal"]/li[1]')),
            '终点POI无法获取').click()
        self.desAdd = self.driver.find_element_by_id('endAddr').get_attribute('addr_hidden')
        WebDriverWait(self.driver, 5).until_not(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="end-lists-penal"]/li[1]')), '终点信息还没消失')
        xpath1 = '//div/label[text()=' + "\"" + "城际拼车" + "\"" + ']'
        self.driver.find_element(By.XPATH, xpath1).click()
        xpath2 = '//div/label[text()=' + "\"" + "今天" + "\"" + ']'
        self.driver.find_element(By.XPATH, xpath2).click()
        WebDriverWait(self.driver, 5).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="priceTips"]'), '预估花费'),
            '获取价格失败')
        self.driver.find_element_by_id('submitAll').click()
        sleep(3)
        flow_info['order_id'] = self.driver.find_element_by_xpath('//*[@id="callOrderPage"]/table/tbody/tr[1]').get_attribute('order-id')


    def order_center(self):
        switch_frame(self.driver, '[tit=司机报班]', '[tit=城际调度中心]', '[src="/orderCenterNew.do"]')

        ori = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.ID, 'startName')))
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@id="startName-suggest"]/div')))
        ori.click()

        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.ID, 'startName-suggest')))
        ori.send_keys('XMC')
        WebDriverWait(self.driver, 5).until(EC.text_to_be_present_in_element_value((By.ID, 'sel_origin'), "361000"))

        des = self.driver.find_element_by_id('endsName')
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@id="endsName-suggest"]/div')))
        des.click()
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.ID, 'endsName-suggest')))
        des.send_keys('NA')
        WebDriverWait(self.driver, 5).until(
            EC.text_to_be_present_in_element_value((By.ID, 'sel_destination'), "362300"))
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[1]/ul/li[2]'))
        ).click() #点击订单列表
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="order-nav-query"]/span'))
        ).click()  #点击查询
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="orderImmediately"]/table/tbody/tr')))
        records = self.driver.find_elements_by_xpath('//*[@id="orderImmediately"]/table/tbody/tr')
        for i in range(len(records)):

            if records[i].get_attribute('order-id') == flow_info['order_id']:
                xpath = '//*[@id="tdy_driver_queue"]/tr[%s]/td[15]/a[text()="指派"]' % (i+1)
                self.driver.find_element_by_xpath(xpath).click()
                WebDriverWait(self.driver, 5).until(
                    EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, '[src^="/orderCtrl.do"]')))
                WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="intercity-lists"]/tr')))
                drivers_phone = self.driver.find_elements_by_xpath('//*[@id="intercity-lists"]/tr/td[4]')
                for j in range(len(drivers_phone)):
                    if drivers_phone[j].text == flow_info['driver_phone']:
                        if len(drivers_phone) > 1:
                            focus_driver_xpath = '//*[@id="intercity-lists"]/tr[%s]/td[1]' % (j+1)
                        elif len(drivers_phone) == 1:
                            focus_driver_xpath = '//*[@id="intercity-lists"]/tr/td[1]'

                        self.driver.find_element_by_xpath(focus_driver_xpath).click()
                        sleep(1)
                        self.driver.find_element_by_id('todoSaveBtn').click()
#                         self.driver.switch_to.parent_frame()
                        break
                    elif j == len(drivers_phone)-1:
                        self.driver.find_element_by_class_name('todoExitBtn').click()
                self.driver.switch_to.parent_frame()
                break
        sleep(2)    #"已派"可见，但被遮挡
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[3]/div[1]/div[2]/a[@title="已派"]'))).click()
#        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[3]/div[1]/div[2]/a[@title="已派"]'))).click()
 #       WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tdy_driver_queue"]/tr')))
        sleep(1)
        orders_send = self.driver.find_elements_by_xpath('//*[@id="tdy_driver_queue"]/tr')
        for i in range(len(orders_send)):
            if orders_send[i].get_attribute('order-id') == flow_info['order_id']:
                return True
                break
        return False

    def order_manage(self):
        switch_frame(self.driver, '[tit=司机报班]', '[tit=订单管理]', '[src="/orderManage.do"]')
        ori = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.ID, 'startName')))
        '''
        DOM树有相关suggest条目，即可点击方位
        '''
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@id="startName-suggest"]/div')))
        # sleep(1)
        ori.click()

        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.ID, 'startName-suggest')))
        ori.send_keys('XMC')
        WebDriverWait(self.driver, 5).until(EC.text_to_be_present_in_element_value((By.ID, 'sel_origin'), "361000"))

        des = self.driver.find_element_by_id('endsName')
        '''
        DOM树有相关suggest条目，即可点击方位
        '''
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@id="endsName-suggest"]/div')))
        des.click()
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.ID, 'endsName-suggest')))
        des.send_keys('NA')
        WebDriverWait(self.driver, 5).until(EC.text_to_be_present_in_element_value((By.ID, 'sel_destination'), "362300"))
#        s = Select(self.driver.find_element_by_id('orderStatus'))
#        s.select_by_visible_text('已指派')
        self.driver.find_element_by_id('btnQuery').click()
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="data_table"]/tbody/tr[1]')))
        records =self.driver.find_elements_by_xpath('//*[@id="data_table"]/tbody/tr')

        for i in range(len(records)):
            if records[i].get_attribute('order-list-id') == flow_info['order_id']:
                if len(records) == 1:
                    xpath = '//*[@id="data_table"]/tbody/tr/td[21]/a[text()="上车"]'
                else:
                    xpath = '//*[@id="data_table"]/tbody/tr[%s]/td[21]/a[text()="上车"]' % (i+1)
                self.driver.find_element_by_xpath(xpath).click()
                WebDriverWait(self.driver, 5).until(
                    EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, '[src^="/orderManage.do?method=getOrderManageOnCar"]')))
                WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.ID, 'todoSureBtn'))).click()
                self.driver.switch_to.parent_frame()

                xpath = '//*[@id="data_table"]/tbody/tr[%s]/td[21]/a[text()="下车"]' % (i+1)
                WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, xpath))).click()
                WebDriverWait(self.driver, 5).until(
                    EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, '[src^="/orderManage.do?method=getOrderManageOffCar"]')))
                WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.ID, 'todoSureBtn'))).click()
                self.driver.switch_to.parent_frame()

                xpath = '//*[@id="data_table"]/tbody/tr[%s]/td[21]/a[text()="线下"]' % (i + 1)
                WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, xpath))).click()
                WebDriverWait(self.driver, 5).until(
                    EC.frame_to_be_available_and_switch_to_it(
                        (By.CSS_SELECTOR, '[src^="/orderManage.do?method=getOrderManageOffline"]')))
                WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.ID, 'todoSureBtn'))).click()
                WebDriverWait(self.driver, 5).until(
                    EC.invisibility_of_element_located((By.ID, 'todoSureBtn')))
                self.driver.switch_to.parent_frame()
                xpath = '//*[@id="data_table"]/tbody/tr[%s]/td[17]' % (i + 1)
   #             WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, xpath))
                if self.driver.find_element_by_xpath(xpath).text == '已完成':
                    return True
                else:
                    return False
                break

#    @unittest.skip("直接跳过")
    def test_driver_report(self):
        report_status = self.driver_report(13345678965)
        self.assertEqual(report_status, '报班')

    def test_customer_call(self):
        self.customer_call(5603293)
        str_ori = self.driver.find_element_by_xpath('//*[@id="callOrderPage"]/table/tbody/tr[1]/td[5]').text
        str_des = self.driver.find_element_by_xpath('//*[@id="callOrderPage"]/table/tbody/tr[1]/td[6]').text
        self.assertEqual(getOriAdd(' ', 0, self.oriAdd), getOriAdd(' ', 1, str_ori))
        self.assertEqual(getOriAdd(' ', 0, self.desAdd), getOriAdd(' ', 1, str_des))

    def test_order_center(self):
        status = self.order_center()
        self.assertTrue(status)

    def test_order_manage(self):
        status = self.order_manage()
        self.assertTrue(status)


if __name__ == '__main__':

    suite = unittest.TestSuite()
    suite.addTest(TestFlow("test_driver_report"))
    suite.addTest(TestFlow("test_customer_call"))
    suite.addTest(TestFlow('test_order_center'))
    suite.addTest(TestFlow("test_order_manage"))
    now_time = strftime("%Y-%m-%d %H-%M-%S")
    file_path = "d:\\test_report\\" + now_time + "_result.html"
    file_result = open(file_path, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(file_result, 2, u"业务后台测试报告", u"执行概况")
    runner.run(suite, 0, 2)
    file_result.close()

