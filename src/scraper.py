from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from datetime import datetime
import uuid
import time
from config.config import Config

class TwitterScraper:
    def __init__(self):
        self.mongo_client = MongoClient(Config.MONGO_URI)
        self.db = self.mongo_client['twitter_trends']
        self.collection = self.db['trending_topics']

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-notifications')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        return webdriver.Chrome(options=options)

    def login(self, driver):
        try:
            wait = WebDriverWait(driver, 20)
            print("Starting login process...")

            driver.get("https://twitter.com/i/flow/login")
            time.sleep(5)
            print("Loaded login page")

            # Enter username
            print("Finding username field...")
            username_input = wait.until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, 'input[autocomplete="username"]'
            )))
            username_input.clear()
            username_input.send_keys(Config.TWITTER_USERNAME)
            username_input.send_keys(Keys.RETURN)
            time.sleep(3)
            print("Username entered and submitted")
            print("Finding password field...")
            password_input = wait.until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, 'input[type="password"]'
            )))
            password_input.clear()
            password_input.send_keys(Config.TWITTER_PASSWORD)
            password_input.send_keys(Keys.RETURN)
            time.sleep(5)
            print("Password entered and submitted")
            wait.until(lambda d: "x.com/home" in d.current_url or "twitter.com/home" in d.current_url)
            print("Successfully logged in")

        except Exception as e:
            print(f"Error during login: {str(e)}")
            print("Current URL:", driver.current_url)
            print("Page content:")
            print(driver.page_source[:1000])
            raise e

    def get_trends(self):
        driver = self.setup_driver()
        try:
            print("Starting trend scraping process...")
            
            self.login(driver)
            time.sleep(3)
            print("Login complete")

            print("Navigating to explore...")
            driver.get("https://twitter.com/explore")
            time.sleep(5)

            print("Finding trends...")
            wait = WebDriverWait(driver, 20)
            trends = wait.until(EC.presence_of_all_elements_located((
                By.CSS_SELECTOR, '[data-testid="trend"]'
            )))[:5]
            
            trending_topics = []
            for trend in trends:
                try:
                    spans = trend.find_elements(By.TAG_NAME, "span")
                    trend_text = None
                    
                    for span in spans:
                        text = span.text.strip()
                        if (text and 
                            not text.endswith('· Trending') and 
                            not text.startswith('Trending in') and 
                            not text.isnumeric() and 
                            not text.startswith('#')):
                            trend_text = text
                            break
                    
                    if trend_text:
                        trending_topics.append(trend_text)
                    else:
                        for span in spans:
                            text = span.text.strip()
                            if text and not text.isnumeric():
                                trending_topics.append(text)
                                break
                                
                except Exception as e:
                    print(f"Error extracting trend: {e}")
                    trending_topics.append("Unable to fetch trend")

            print(f"Found {len(trending_topics)} trends")
            print("Trends:", trending_topics)

            trend_data = {
                "_id": str(uuid.uuid4()),
                "nameoftrend1": trending_topics[0] if trending_topics else "N/A",
                "nameoftrend2": trending_topics[1] if len(trending_topics) > 1 else "N/A",
                "nameoftrend3": trending_topics[2] if len(trending_topics) > 2 else "N/A",
                "nameoftrend4": trending_topics[3] if len(trending_topics) > 3 else "N/A",
                "nameoftrend5": trending_topics[4] if len(trending_topics) > 4 else "N/A",
                "datetime": datetime.now(),
                "ip_address": "127.0.0.1"
            }

            self.collection.insert_one(trend_data)
            print("Data saved to MongoDB")
            return trend_data

        except Exception as e:
            print(f"Error in scraping: {e}")
            print("Current URL:", driver.current_url)
            raise e

        finally:
            print("Closing browser...")
            driver.quit()