FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Cài đặt Tkinter, Màn hình ảo (Xvfb) và Web VNC
RUN apt-get update && apt-get install -y \
    python3-tk \
    xvfb \
    x11vnc \
    novnc \
    websockify \
    && rm -rf /var/lib/apt/lists/*

# Mặc định mở trang vnc.html khi vào localhost:6080
RUN ln -s /usr/share/novnc/vnc.html /usr/share/novnc/index.html

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Sửa lỗi ký tự xuống dòng Windows (CRLF) và cấp quyền cho start.sh
RUN sed -i 's/\r$//' start.sh && chmod +x start.sh

CMD ["./start.sh"]