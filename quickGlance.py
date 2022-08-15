from multiprocessing.connection import wait
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.extensions.android.nativekey import AndroidKey
import time

#=============== Declaration of webDriver ===================

driver = {
  "platformName": "Android",
  "appium:platformVersion": "12.0",
  "appium:deviceName": "redfin",             #replace this field using your phone name: terminal > adb devices -l 
  "appium:automationName": "UiAutomator2",   #if your phone OS is < Android 10 use UiAutomator 1
  "appium:udid": "0B251FDD40023Y",           #replace this field using your phone id: terminal > adb devices 
  "appium:forceMjsonwp":"True"
}

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', driver)
#=================================================================

#============= Functions Declaration =============================
def blockScreenEGV(driver):
    #This Function simply retreives EstimatedGlucoseValue (EGV) from blockScreen 
    #  and returns it as float type
    #Try block makes sure QG Screen is showing numeric values
    QuickGlanceEGV = driver.find_element(MobileBy.ID,'com.dexcom.g7:id/glucose_value_text').text
    try:
        return float(QuickGlanceEGV)
    except: 
        print("---Not numeric Values Displayed QuickGlanceEGV---")
        QuickGlanceEGV = 0.0
        return QuickGlanceEGV

    
def g7EGV(driver):
    #This function retreives EstimatedGlucoseValue (EGV) 
    # from g7App and returns it as float type
    #Try block makes sure QG Screen is showing numeric values
    g7Value = driver.find_element(MobileBy.ID,'com.dexcom.g7:id/id_glucose_compass_egv').text
    try:
        return float(g7Value)
    except:
        print("---Not numeric Values Displayed G7Eegv--- ")
        g7Value = 0.0
        return g7Value
#======================================================================

# ==== Variables Declaration Initialization ====================

error = 0.0 # difference between QuickGlance value (QG) - G7 app
QGvalue=0.0 # values shown by QuickGlance while screen locked
g7value=0.0 # values shown by G7App
currentTrials = 0
desiredTrials = 5  # <<<< Input here your desired number of trials 
#======================================================================

#========== Values comparison ===================

"""
    This cicle is in charge to periodically compare values between QG and G7
    in order to find some discrepancies
"""
while(abs(error)<0.5 and desiredTrials >= currentTrials):
    
    currentTrials += 1
    print("---- trial number : {} ----".format(currentTrials))

    driver.lock()                    # Device gets blocked
    driver.keyevent(224)             # Wake up screen  
    QGvalue = blockScreenEGV(driver) # Get QGvalue 
    driver.swipe(200,200,200,-500)   # Swipe Screen in order to access g7
    g7value= g7EGV(driver)           # Get G7 app value

    error = QGvalue - g7value       # computing error

    print("QGvalue: {} , g7value: {} , error: {} ".format(QGvalue,g7value,error))

#===============================================

#==========Issues found Check ===========================

if (desiredTrials + 1  == currentTrials):
    print("=======Test finished No errors found during this Trials ======")

else:
    print("Issues were found: {}".format(driver.get_device_time()))