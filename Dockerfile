FROM python:3.10-slim

# התקנת ספריות מערכת נדרשות להרצת דפדפנים בלינוקס
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# העתקת דרישות והתקנתן
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# פקודת הקסם שמתקינה את דפדפן כרום הנסתר בתוך השרת בענן
RUN playwright install chromium
RUN playwright install-deps

# העתקת שאר קבצי הקוד
COPY . .

# הרצת השרת
CMD ["python", "app.py"]
