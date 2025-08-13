# Device Image Analyzer API (Starter)

این یک بک‌اند ساده‌ی FastAPI است که فایل تصویر را می‌گیرد و:
- اطلاعات پایه‌ای تصویر (ابعاد، نوع فایل، هش، EXIF) را برمی‌گرداند.
- یک بانک داده محلی (`data.json`) را برای لیبل مشخص جستجو می‌کند.
- فعلاً «شناسایی خودکار» را انجام نمی‌دهد و صرفاً یک اسکلت اولیه است تا بعداً مدل یا API هوش مصنوعی اضافه شود.

## اجرا به صورت محلی
```bash
pip install -r requirements.txt
uvicorn app:app --reload
```
سپس به آدرس `http://127.0.0.1:8000/docs` بروید.

## متغیرهای محیطی
- `ALLOWED_ORIGINS`: لیست دامنه‌هایی که مجاز هستند (CORS). مثال: `https://example.com,https://www.example.com`
- `DATA_PATH`: مسیر فایل دیتای محلی (پیش‌فرض `data.json`).

## استقرار روی Render (پیشنهادی ساده)
1. این پوشه را در یک مخزن GitHub قرار دهید.
2. در Render یک **Web Service** جدید بسازید و مخزن‌تان را وصل کنید.
3. **Build Command**:
   ```
   pip install -r requirements.txt
   ```
4. **Start Command**:
   ```
   uvicorn app:app --host 0.0.0.0 --port $PORT
   ```
5. `ALLOWED_ORIGINS` را روی دامنه وب‌فلو خود (یا برای تست، `*`) تنظیم کنید.

## فایل داده محلی
`data.json` یک دیکشنری ساده است. کلیدها نام «لیبل» و مقدار، اطلاعات مربوطه است.
