import json  
import time  
from datetime import datetime  
import logging  
from selenium import webdriver  
from seleniumbase import Driver
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import Select  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.common.exceptions import TimeoutException, WebDriverException  
from telegram import Bot  

# Loglama ayarları  
logging.basicConfig(  
    level=logging.INFO,  
    format='%(asctime)s - %(levelname)s - %(message)s',  
    handlers=[  
        logging.FileHandler('randevu_kontrol.log', encoding='utf-8'),  
        logging.StreamHandler()  
    ]  
)  
logger = logging.getLogger(__name__)  

def load_config():  
    try:  
        try:  
            with open('config.json', 'r', encoding='utf-8') as file:  
                return json.load(file)  
        except UnicodeDecodeError:  
            with open('config.json', 'r', encoding='windows-1254') as file:  
                return json.load(file)  
    except Exception as e:  
        logger.error(f"Hata :{e}")  
        raise

def send_telegram_message(bot_token, channel_id, message):  
    try:  
        bot = Bot(token=bot_token)  
        bot.send_message(  
            chat_id=channel_id,  
            text=message,  
            parse_mode='HTML'  
        )  
        logger.info("Gönderildi!")  
    except Exception as e:  
        logger.error(f"Gönderilmedi {e}")  

def check_appointment(config):  
    driver = Driver(uc=True)  
    try:  
        # Chrome options ayarları  
        chrome_options = webdriver.ChromeOptions()  
        # chrome_options.add_argument('--headless')  # Tarayıcıyı arka planda çalıştır  
        chrome_options.add_argument('--no-sandbox')  
        chrome_options.add_argument('--disable-dev-shm-usage')  
        
        driver.uc_open_with_reconnect(config['web_url'], 4)        
        #driver.uc_gui.click_captcha() // gerek kalmadı 
        logger.info("5 sn bekleniyor")  
        time.sleep(1)  # Captcha geçiyoruz
        # Doldurmaya başlayalım
        for dropdown_id, value in config['dropdowns'].items():  
            try:  
                logger.error("eklendi")
                dropdown = WebDriverWait(driver, 10).until(  
                    EC.presence_of_element_located((By.ID, dropdown_id))  
                )  
                select = Select(dropdown)  
                select.select_by_visible_text(value)  
                logger.info(f"{dropdown_id} dolduruldu")  
                time.sleep(5)  # Her dropdown sonrası kısa bekleme  
            except Exception as e:  
                logger.error(f"{dropdown_id} doldurulurken hata: {e}")  
                raise  
        
        time.sleep(5)

        # Alert mesajını kontrol et  
        try:  
            alert_element = WebDriverWait(driver, 10).until(  
                EC.presence_of_element_located((By.ID, config['alert_message']['element_id']))  
            )  
            alert_text = alert_element.text.strip()  
            
            if config['alert_message']['success_text'] in alert_text:  
                message = f"""  
                                <b>Randevu Bulundu!</b>  
                                <b>Link:</b>  
                                {config['web_url']}  
                                """  
                send_telegram_message(  
                    config['telegram']['bot_token'],  
                    config['telegram']['channel_id'],  
                    message  
                )  
            else:  
                logger.info("N")  
                
        except TimeoutException:  
            logger.warning("Alert mesajı bulunamadı")  
            
    except WebDriverException as e:  
        logger.error(f"WebDriver hatası: {e}")  
    except Exception as e:  
        logger.error(f"Beklenmeyen hata: {e}")  
    finally:  
        if driver:  
            driver.quit()  

def main():  
    try:  
        config = load_config()  
        logger.info("Program başlatıldı")  
        
        while True:  
            try:  
                check_appointment(config)  
                logger.info(f"{config['check_interval']} saniye bekleniyor...")  
                time.sleep(config['check_interval'])  
            except Exception as e:  
                logger.error(f"hata oluştu: {e}")  
                time.sleep(30)  
                
    except KeyboardInterrupt:  
        logger.info("Program kullanıcı tarafından sonlandırıldı")  
    except Exception as e:  
        logger.error(f"Program beklenmeyen şekilde sonlandı: {e}")  

if __name__ == "__main__":  
    main()  