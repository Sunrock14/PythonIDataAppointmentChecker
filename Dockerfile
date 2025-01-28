# Python 3.10 tabanlı bir imaj kullanıyoruz
FROM python:3.10-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gereksinim dosyasını kopyala ve bağımlılıkları yükle
COPY requirements.txt .

# Bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# Python scriptini ve diğer dosyaları kopyala
COPY . .

# Uygulamanın çalışması için gerekli ek yazılımlar
RUN apt-get update && apt-get install -y \
    chromium-driver \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

# Selenium'un çalışması için gerekli PATH değişkeni
ENV PATH="/usr/lib/chromium/:$PATH"

# Uygulamayı çalıştır
CMD ["python", "main.py"]

#docker build -t idatachecker .
#docker run -d --name idatachecker idatachecker
