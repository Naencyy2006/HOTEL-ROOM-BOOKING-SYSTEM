#!/bin/sh
# 1. Khởi tạo màn hình ảo
Xvfb :99 -screen 0 1280x800x24 &
export DISPLAY=:99

# 2. Chạy VNC Server ngầm
x11vnc -display :99 -forever -shared -nopw -rfbport 5900 &

# 3. Chạy noVNC chuyển tiếp giao diện ra Web cổng 6080
websockify --web=/usr/share/novnc/ 6080 localhost:5900 &

# 4. Chạy ứng dụng Python Tkinter
python main.py