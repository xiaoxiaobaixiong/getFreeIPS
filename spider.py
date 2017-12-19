# _*_ coding:utf-8 _*_

from selenium import webdriver
# #不显示窗口
from pyvirtualdisplay import Display

display = Display(visible=0, size=(800,900))
display.start()

# this part for get args from cmd
import argparse
from datetime import datetime
import calendar
now = datetime.now().today()
today = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
parser = argparse.ArgumentParser(description="Usage for this scrpt")
parser.add_argument('-s', type=str, default=today)
parser.add_argument('-e', type=str, default=today)
parser.add_argument('-d', type=str, default="/home/alan/tempdata")
args = parser.parse_args()
startYMD = args.s.split('-')
endYMD = args.e.split('-')

from getFreeIPS.getFreeIP import getfreeip
ips = getfreeip(100)
# url = 'http://op1.win007.com/index_vip.aspx'
url = 'http://op1.win007.com/bet007history.aspx'
options = webdriver.ChromeOptions()
prefs = {
         'download.default_directory': args.d,
         'download.manager.showWhenStarting': False,
         'helperApps.neverAsk.saveToDisk':  True
         }
options.add_experimental_option('prefs', prefs)
for ip in ips:
    options.add_argument('--proxy-server=http://'+ip.ip+':'+ip.port)
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url=url)

def downloadThisPageAllLinks(strdate):
    # this two line can set time for data extraction
    driver.find_element_by_xpath('//*[@id="form1"]/div[4]/div[2]/div[1]/input[1]').send_keys(strdate)
    driver.find_element_by_xpath('//*[@id="form1"]/div[4]/div[2]/div[1]/input[2]').click()
    # 172

    contents = driver.find_elements_by_class_name("gocheck")

    # print(type(contents))
    # this for find
    for content in contents :
        detail_url = content.find_element_by_link_text('查看').get_attribute('href')
        print(detail_url)

        ## this is for downloads operation
        threadDriver = webdriver.Chrome(chrome_options=options)
        threadDriver.get(detail_url)
        home_team = threadDriver.find_element_by_xpath('//*[@id="team"]/table/tbody/tr[1]/td/span[1]')
        visiting_team = threadDriver.find_element_by_xpath('//*[@id="team"]/table/tbody/tr[1]/td/span[5]/a')
        print(home_team.text + " " + visiting_team.text)
        threadDriver.find_element_by_xpath('//*[@id="downobj"]').click()

for year in range(int(startYMD[0]), int(endYMD[0]) + 1):
    if year == int(startYMD[0]):
        startMonth = int(startYMD[1])
    else:
        startMonth = 1

    if year == int(endYMD[0]):
        endMonth = int(endYMD[1])
    else:
        endMonth = 13

    for month in range(startMonth, endMonth + 1):

        startDay = 1
        endDay = calendar.monthrange(year, month)[1]
        if year == int(startYMD[0]) and month == int(startYMD[1]):
            startDay = int(startYMD[2])

        if year == int(endYMD[0]) and month == int(endYMD[1]):
            endDay = int(endYMD[2])

        for day in range(startDay, endDay+1):
            strdate_for_query = str(year) + "-" + str(month) + "-" + str(day)
            print(strdate_for_query)
            downloadThisPageAllLinks(strdate_for_query)

print("downloads complete!!")
