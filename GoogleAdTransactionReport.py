import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os



def get_profile_path(profile):
    FF_PROFILE_PATH = os.path.join(os.environ['APPDATA'],'Mozilla', 'Firefox', 'Profiles')

    try:
        profiles = os.listdir(FF_PROFILE_PATH)
    except WindowsError:
        print("Could not find profiles directory.")
        sys.exit(1)
    try:
        for folder in profiles:
            print(folder)
            if folder.endswith(profile):
                loc = folder
    except StopIteration:
        print("Firefox profile not found.")
        sys.exit(1)
    return os.path.join(FF_PROFILE_PATH, loc)



url= # URL of Google Ad Transaction page;

download_path_root = # Report Download Root Path Here

file_path= # Report Folder Name

prof = # Firefox Profile name i.e: abcxyz.default-release



mime_types = "text/csv"
profile = webdriver.FirefoxProfile(get_profile_path(prof))
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", os.path.join(download_path_root, file_path))
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
profile.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)


print(os.path.join(download_path_root, file_path))

driver = webdriver.Firefox(firefox_profile=profile)
driver.get(url)
driver.maximize_window()
wait = WebDriverWait(driver, 10)

time.sleep(30)

driver.switch_to.frame("embedded-page-containerIframe")

drp_down=driver.find_element(By.CSS_SELECTOR, "div[data-name = 'timelineViewDateRangeFilter']")
drp_down.click()
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, "div.goog-menuitem[data-value='THIS_MONTH']").click()
time.sleep(10)

driver.switch_to.window(driver.window_handles[0])
driver.switch_to.frame("embedded-page-containerIframe")
try:
    down_btn = driver.find_element(By.CSS_SELECTOR, "div[aria-label = 'Download']")

    for root, dirs, files in os.walk(download_path_root+"\\"+file_path):
        for file in files:
            os.remove(os.path.join(root, file))

    down_btn.click()
    time.sleep(20)

    driver.quit()
except:
    driver.quit()
