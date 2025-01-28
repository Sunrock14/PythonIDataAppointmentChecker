#IData sitesinden randevu açılışını kontrol eden bir program
import json
import time
import asyncio
import logging
from datetime import datetime
from selenium import webdriver
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from telegram import Bot  

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('randevu_kontrol.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def load_config() -> dict:
    try:
        encodings = ['utf-8', 'windows-1254']
        for encoding in encodings:
            try:
                with open('config.json', 'r', encoding=encoding) as file:
                    return json.load(file)
            except UnicodeDecodeError:
                continue
        raise ValueError("Unsupported encoding")
    except Exception as e:
        logger.error(f"Configuration loading error: {e}")
        raise

async def send_telegram_message(
        bot_token: str, 
        channel_id: str, 
        message: str) -> bool:
    try:
        bot = Bot(token=bot_token)
        await bot.send_message(
            chat_id=channel_id,
            text=message,
            parse_mode='HTML'
        )
        logger.info("Message sent successfully!")
        return True
    except Exception as e:
        logger.error(f"Telegram message sending error: {str(e)}")
        return False

async def handle_dropdown(
        driver: Driver,
        dropdown_id: str,
        dropdown_value: str,
        wait_time: int = 2):
    try:
        dropdown_element = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((By.ID, dropdown_id))
        )
        dropdown_element.click()
        await asyncio.sleep(1)

        select = Select(dropdown_element)
        select.select_by_value(dropdown_value)
        await asyncio.sleep(1)
    except Exception as e:
        logger.error(f"Error filling dropdown {dropdown_id}: {e}")
        raise

async def check_appointment(config: dict):
    driver = None
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')
        #chrome options seleneiumbase ile veremedik
        driver = Driver(uc=True) #options desteklemiyor
        driver.uc_open_with_reconnect(config['web_url'], 2)
        await asyncio.sleep(1)

        for dropdown_id, dropdown_value in config['dropdowns'].items():
            await handle_dropdown(driver, dropdown_id, dropdown_value)

        button = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "btnAppCountNext"))
        )
        
        display_style = button.value_of_css_property('display')
        
        message = (
            "<b>Randevu Bulundu!</b>\n"
            f"<b>Link:</b>\n{config['web_url']}"
        )
                
        if display_style == 'block':
            logger.info("Appointment found!")
            # Uncomment to enable automatic clicking

            message = (
                "<b>Randevu Bulundu!</b>\n"
                f"<b>Link:</b>\n{config['web_url']}"
            )
            
            success = await send_telegram_message(
                config['telegram']['bot_token'],
                config['telegram']['channel_id'],
                message
            )
        else:

            message = (
                "<b>Randevu bulunamadı!</b>"
            )
            # test edildi
            success = await send_telegram_message(
                config['telegram']['bot_token'],
                config['telegram']['channel_id'],
                message
            )
            logger.info("No appointment available")

    except TimeoutException:
        logger.warning("Button not found!")
    except WebDriverException as e:
        logger.error(f"WebDriver error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        if driver:
            driver.quit()

async def main():
    config = await load_config()
    logger.info("Program started")
    
    try:
        while True:
            try:
                await check_appointment(config)
                logger.info(f"Waiting {config['check_interval']} seconds...")
                await asyncio.sleep(config['check_interval'])
            except Exception as e:
                logger.error(f"Error occurred: {e}")
                await asyncio.sleep(30)
    except KeyboardInterrupt:
        logger.info("Program terminated by user")
    except Exception as e:
        logger.error(f"Program terminated unexpectedly: {e}")

if __name__ == "__main__":
    asyncio.run(main())

# google options için seleniumbase docs içinde gerekli option bulamadım
# fakat python main.py --headless komutuyla çalıştırırsak 
# tarayıcı açılmadan gerekli kontrolleri sağlayabiliyor ve varsayılan şekilde çalıştırabiliyoruz.