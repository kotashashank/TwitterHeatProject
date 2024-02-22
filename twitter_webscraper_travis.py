import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import pandas as pd
import geopandas as gpd
import urllib.parse


# constants
DEBUG_MODE = True

UNTIL_IDENTIFER = "[UNTIL]"
DEFAULT_UNTIL = "2023-10-01T23:59:59.000Z"

FAILS_BEFORE_BREAK = 5
CURRENT_USER = 1


def printd(out: str):
    if(not DEBUG_MODE):    return
    print(out)

def create_driver():
    # add options
    options =  webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.cookies": 1,
            "profile.cookie_controls_mode": 1}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("window_size=1280,800")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("executable_path=/usr/local/bin/chromedriver")

    # return driver instance
    return webdriver.Chrome(options=options)

def change_current_user_tag(emails):
    global CURRENT_USER
    if(CURRENT_USER == len(emails) - 1):
        CURRENT_USER = 0
    else:
        CURRENT_USER = CURRENT_USER + 1

def change_modes(driver, emails, passwords):
    global CURRENT_USER
     
    wait = WebDriverWait(driver, 10)
    if(CURRENT_USER >= 0):
        # switch to logged on
        logout(driver)
        printd("switching to mode 1")

        driver.find_element(By.XPATH, '//a[contains(@href, "login")]').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//iframe').click()
        time.sleep(1)
        # switch to google view
        current_window = driver.current_window_handle

        wait = WebDriverWait(driver, 10)
        wait.until(EC.number_of_windows_to_be(2))

        for window_handle in driver.window_handles:
            if window_handle != current_window:
                driver.switch_to.window(window_handle)
                printd(window_handle)
                break
        time.sleep(2)        
        login_to_google(driver, emails[CURRENT_USER], passwords[CURRENT_USER])
        time.sleep(1.5)
        driver.switch_to.window(current_window)
        time.sleep(1)
        
    change_current_user_tag(emails)

    # check if actually switched

# returns bool depending on success of operation
def logout(driver) -> bool:
    try:
        driver.find_element(By.XPATH, '//div[contains(@aria-label, "Account menu")]').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//a[contains(@href, "/logout")]').click()
        driver.find_element(By.XPATH, '//div[contains(@data-testid, "confirmationSheetConfirm")]').click()
        time.sleep(1)
    except:
        return False
    return True

def login_to_google(driver, email, password) -> bool:
    try:
        # login to Google Account
        # check if cna use another account
        use_another_account = len(driver.find_elements(By.XPATH, '//div/div[contains(text(), "Use another account")]')) > 0
        if(use_another_account):
            driver.find_element(By.XPATH, '//div/div[contains(text(), "Use another account")]').click()
            time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="identifierId"]').send_keys(email)
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="identifierNext"]/div/button/span').click()
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="passwordNext"]/div/button/span').click()
        time.sleep(2.5)
    except:
        return False

    return True

def login(driver, email, password) -> bool:
    try:
        driver.get("https://twitter.com/")
        time.sleep(2)
        driver.find_element(By.XPATH, '//iframe').click()
        time.sleep(2)
        current_window = driver.current_window_handle

        wait = WebDriverWait(driver, 10)
        wait.until(EC.number_of_windows_to_be(2))

        for window_handle in driver.window_handles:
            if window_handle != current_window:
                driver.switch_to.window(window_handle)
                printd(window_handle)
                break

        time.sleep(2)
        driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div/main/div/div/div[1]/div[2]').click()
        time.sleep(2)
        out = login_to_google(driver, email, password)
        if(not out):
            return False
    except:
        return False

    return True




# filename 
# index => index in file
# radius => radius of tweets (in km)
# start_date => left to replace by user
# end_date => end date of twitter query(YYYY-MM-DD)
# returns tuple of two arrays 
def get_points(filename: str, index: int, radius: str, end_date: str) -> tuple[list[str], list[str]]:
    points = gpd.read_file(filename);

    long_lat_strings = []
    search_queries = []

    i = 0

    # iterate through dataframe, process points of interet, create twitter search query
    for point in points.geometry:
        if(i >= index):
            long_lat_string = str(point.y) + "," + str(point.x)
            search_query = '" " geocode:' + long_lat_string + ',' + radius + 'km until:' + UNTIL_IDENTIFER + ' since:' + end_date + ' -is:retweet'
            long_lat_strings.append(long_lat_string)
            search_queries.append(search_query)
        i += 1
        

    return long_lat_strings, search_queries

def query_with_until(original_query: str, until_date: str) -> str:
    return original_query.replace(UNTIL_IDENTIFER, until_date)

def setup_scrape(driver: webdriver, email: str, password: str) -> bool:
    # go to google signin
    try: 
        driver.get("https://accounts.google.com/v3/signin/identifier?hl=en_GB&ifkv=AXo7B7VGP4Y_gNfwPri72zV40Ii9kmgYbvLRXoOhOeBNkeBYcMPcPOX_Aolo1vK16FetaA4URMIfUA&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-1140670556%3A1692882589574310")

        login_to_google(driver, email, password)

        # active selenium stealth to avoid being detected as a bot on twitter 
        stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True) # i need this bad fr
        
        # go to twitter 
        driver.get("https://twitter.com/")
        time.sleep(2)
        driver.find_element(By.XPATH, '//iframe').click()
        time.sleep(2)
        current_window = driver.current_window_handle

        wait = WebDriverWait(driver, 10)
        wait.until(EC.number_of_windows_to_be(2))

        for window_handle in driver.window_handles:
            if window_handle != current_window:
                driver.switch_to.window(window_handle)
                printd(window_handle)
                break

        time.sleep(2)
        driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div/main/div/div/div[1]/div[1]').click()
        time.sleep(5)
        driver.switch_to.window(current_window)
    except:
        return False
    
    return True

# list of tweet information (list)
# did_finish (boolean)
# final date (str)
def get_tweet_links(driver: webdriver, query: str, start_date: str) -> tuple[list[list[str]], bool, str]:

    actions = ActionChains(driver)

    processed_tweets = []
    # input search query

    url = 'https://twitter.com/search?'
    params = {'q': query, 'src': 'typed_query', 'f': 'live'}
    # print(url + urllib.parse.urlencode(params))
    driver.get(url + urllib.parse.urlencode(params))
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.XPATH, '//div[contains(@aria-label, "Home timeline")]//*[name()="circle"]')))   

    # to avoid duplicate tweets
    seen_links = set()

    change_queue = []

    until_date = start_date

    # make sure actually logged in
    if(len(driver.find_elements(By.XPATH, '//nav[contains(@role, "navigation")]')) == 0):
        print("LOL!")
        return (processed_tweets, False, until_date)
    
    while True:
        # keep scrolling until end of page found
        actions.send_keys(Keys.PAGE_DOWN).perform()
        actions.send_keys(Keys.PAGE_DOWN).perform()

        # Give page some time to load new content
        time.sleep(0.025)  


        is_retry_button_here = len(driver.find_elements(By.XPATH, '//*[contains(text(), "Something went wrong.")]')) > 0
        if(is_retry_button_here):
            return (processed_tweets, False, until_date)
        # Fetch tweet data
        tweets = driver.find_elements(By.XPATH,
                                    '//article[contains(@data-testid, "tweet")]')
        
        # Locate all tweet hrefs 
        for i in range(len(tweets)):
            tweet = tweets[i]
            try:
                link = get_tweet_link(tweet)
                if(link not in seen_links):
                    seen_links.add(link)
                    link, username, datetime, tweet_text, impressions, likes = scrape_tweet(tweet)
                    processed_tweets.append([link, username, datetime, tweet_text, impressions, likes])
                    until_date = datetime
            except Exception as e:
                # scrolled too fast, but don't break entire code 
                continue
        
        
        # when no new tweets have been found for more than 2 iterations, break
        if(len(change_queue) >= 6):
            if(change_queue.pop(0) == len(seen_links)):
                break
        change_queue.append(len(seen_links))
        
    return (processed_tweets, True, until_date)


def get_tweet_link(tweet) -> str:
    return tweet.find_element(By.XPATH, './div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[3]/a').get_attribute('href')

# link, username, datetime, tweet text, impressions, likes
def scrape_tweet(tweet) -> tuple[str, str, str, str, str, str]:

    link = get_tweet_link(tweet)
    
    username = tweet.find_element(By.XPATH, './div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[1]//span').text
    
    datetime = tweet.find_element(By.XPATH, './/time').get_attribute('datetime')

    is_reply = "Replying to" in tweet.find_element(By.XPATH, './div/div/div[2]/div[2]/div[2]').text
    tweet_text = ""
    if(is_reply):
        # third div instead of 2nd
        tweet_text = tweet.find_element(By.XPATH, './div/div/div[2]/div[2]/div[3]').text
    else:
        tweet_text = tweet.find_element(By.XPATH, './div/div/div[2]/div[2]/div[2]').text

    impressions = tweet.find_element(By.XPATH, './/div[contains(@role, "group")]/div[4]').text

    likes = tweet.find_element(By.XPATH, './/div[contains(@role, "group")]/div[3]').text

    return (link, username, datetime, tweet_text, impressions, likes)





if (__name__ == '__main__'):
    
    # TODO
    emails = [] 
    passwords = [] 

    offset = 0
    locations, queries = get_points("travis_hex.geojson", offset, "0.2", "2023-04-30")
    driver = create_driver()
    printd("Setting up scrape")
    setup_scrape(driver, emails[0], passwords[0])


    links = list()
    i = 0
    start_date = DEFAULT_UNTIL
    final_tweets = []
    while i < len(queries):
        try:
            printd("scraping index " + str(i + offset))
            default_query = queries[i];
            location = locations[i];
            printd("Getting tweets from location" + location)
            
            query = query_with_until(default_query, start_date)
            # break when get_tweet_links's did_finish returns true
            while(True):
                tweets, did_finish, until_date = get_tweet_links(driver, query, start_date)
                
                # append each tweet to final_tweets
                for tweet in tweets:
                    final_tweets.append(tweet)
                
                if(did_finish):
                    break
                
                # change query
                query = query_with_until(default_query, until_date)
                start_date = until_date
                change_modes(driver, emails, passwords)
                


            tweets_data_frame = pd.DataFrame(columns=['link', 'username', 'datetime', 'tweet_text', 'impressions', 'likes'])
            for j in range(0, len(final_tweets)):
                tweets_data_frame.loc[j] = final_tweets[j]


            printd("Exporting tweets from location" + location)
            tweets_data_frame.to_csv('../tweets_by_location/tweets_tc_2023/' + location + '.csv')
            
            start_date = DEFAULT_UNTIL
            final_tweets = []

            i = i + 1
        except Exception as e:
            print(e)
            failed_connections = 0
            # allow repeated attempts to reconncect scraper
            while(failed_connections < FAILS_BEFORE_BREAK):
                driver.quit()
                # connection issue probably, wait 6 minutes before attempting to scrape again
                if(failed_connections >= FAILS_BEFORE_BREAK-1):
                    time.sleep(360)  
                    failed_connections = 0
                driver = create_driver()
                was_success = setup_scrape(driver, emails[CURRENT_USER], passwords[CURRENT_USER])
                if(was_success):
                    break
                failed_connections += 1
                change_current_user_tag(emails)

            continue
