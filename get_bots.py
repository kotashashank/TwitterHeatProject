import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Assuming create_driver() is a function that creates a Selenium WebDriver instance
def create_driver():
    return webdriver.Chrome()  # Change to the appropriate WebDriver for your browser

if __name__ == '__main__':
    df = pd.read_csv('filtered_travis_tweets_with_blockgroups.csv')
    driver = create_driver()
    driver.get("https://botometer.osome.iu.edu/")

    bot_scores = []  # List to store bot scores
    
    for username in df['username']:


        try:
            print(username)
            time.sleep(0.125)
            search_box = driver.find_element(By.XPATH, '/html/body/div/div[4]/div[1]/form/div[1]/input')
            search_box.clear()  # Clear any previous input
            search_box.send_keys("@" + username)  # Assuming the username doesn't include '@' already
            driver.find_element(By.XPATH, '//*[@id="screenName-form"]/form/button').click()
            time.sleep(0.125)  # Adding a delay to wait for the results to load
            score = driver.find_element(By.XPATH, '/html/body/div/div[4]/div[2]/div/div/div[1]/p[2]/span').text
            numerator = float(score.split('/')[0])
            bot_scores.append(numerator)
        except:
            bot_scores.append('N/A')  # Append 'N/A' if score extraction fails

    driver.quit()  # Close the WebDriver instance
    
    df['bot_score'] = bot_scores  # Add the bot scores to the DataFrame as a new column
    df.to_csv('manual_filtered_travis_tweets_with_blockgroups_with_scores.csv', index=False)  # Save the DataFrame with scores to a new CSV file
