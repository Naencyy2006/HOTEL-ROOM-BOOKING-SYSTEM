FROM python:3.10-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Biến môi trường ngăn Python ghi file .pyc và bật log trực tiếp
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Cài đặt thư viện phụ thuộc
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY . .

# Lệnh chạy ứng dụng khi container khởi động
CMD ["python", "main.py"]