# IData Randevu Kontrol Scripti

Bu script, IData'nın web sitesini periyodik olarak kontrol ederek İtalya vizesi için randevu boşluklarını arar. 
Bir randevu mevcut olduğunda, kullanıcının belirttiği bir Telegram kanalına bildirim gönderir.

## Özellikler

- Belirtilen aralıklarla randevu durumunu otomatik olarak kontrol eder.
- Randevu bulunduğunda veya bulunmadığında Telegram üzerinden anlık bildirimler gönderir.
- Yapılandırması kolay bir `config.json` dosyası ile birlikte gelir.
- Docker desteği sayesinde kolayca kurulup çalıştırılabilir.

## Nasıl Kullanılır?
- Proje bilgisayara klonlanıp, kütüphaneler yüklenir.
- Dosya yoluna gidilir. 
- Config dosyasındaki bilgiler kontrol edilir/kişileştirilir.
- Telegram -> BotFather üstünden yeni bir bot açılır ve isim seçilir (exp:idatatestcheckerbot)
- Token Config dosyasına eklenir.
- "python main.py --headless" komutuyla proje çalıştırılır. (Son update ile idata sitesine CAPTHA eklenmiş anlık olarak çalışmıyor.)
- Alternatif olarak "python main.py" kullanılarak çalıştırılır. Bu seçenekte bazen CloudFlare doğrulaması geçilemiyor. Ve her istekte tarayıcı açılıyor.

## Kurulum
0. Python kurulumu yapılır.(https://www.python.org/downloads/)

1.  **Projeyi klonlayın:**

    ```bash
    git clone https://github.com/username/PythonIDataAppointmentChecker.git
    cd PythonIDataAppointmentChecker
    ```

2.  **Gerekli kütüphaneleri yükleyin:**

    ```bash
    pip install -r requirements.txt
    ```

## Yapılandırma

`config.json` dosyasını açın ve aşağıdaki alanları kendi bilgilerinize göre düzenleyin:

-   `web_url`: Randevu aramak istediğiniz web sitesinin adresi.
-   `check_interval`: Saniye cinsinden kontrol sıklığı.
-   `dropdowns`: Randevu arama formundaki seçim alanları. Bu değerleri kendi durumunuza göre düzenlemeniz gerekmektedir.
-   `telegram`:
    -   `bot_token`: Telegram botunuzun token'ı.
    -   `channel_id`: Bildirimlerin gönderileceği Telegram kanalının ID'si.

## Kullanım

Script'i başlatmak için aşağıdaki komutu çalıştırın:

```bash
python main.py
```

Script'i arka planda çalıştırmak isterseniz (headless mode):

```bash
python main.py --headless
```

## Docker ile Çalıştırma

Projeyi Docker ile çalıştırmak için aşağıdaki adımları izleyin:

1.  **Docker imajını oluşturun:**

    ```bash
    docker build -t idata-randevu-kontrol .
    ```

2.  **Docker konteynerini çalıştırın:**

    ```bash
    docker run -d --name idata-randevu-kontrol idata-randevu-kontrol
    ```
