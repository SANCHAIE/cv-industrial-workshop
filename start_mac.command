#!/bin/bash
# ชุด Workshop: ติดตั้งและเปิดใช้งานด้วยคลิกเดียว (Mac)
cd "$(dirname "$0")"
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
if ! command -v uv >/dev/null 2>&1; then
  echo "กำลังติดตั้ง uv (ตัวจัดการ Python) ครั้งเดียว..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi
echo "กำลังเตรียม Python 3.12 และไลบรารีทั้งหมด (ครั้งแรกใช้เวลา 2-5 นาที)..."
uv sync || { echo "ติดตั้งไม่สำเร็จ ถ่ายภาพหน้าจอนี้ส่งให้ TA"; read -p "กด Enter เพื่อปิด"; exit 1; }
echo
echo "เลือก:  1 = ตรวจความพร้อม   2 = เปิด Notebook   3 = เปิด Web app"
read -p "พิมพ์ตัวเลขแล้วกด Enter: " c
case "$c" in
  1) uv run check_setup.py; read -p "กด Enter เพื่อปิด" ;;
  3) uv run streamlit run app/inspection_app.py ;;
  *) uv run jupyter lab notebooks ;;
esac
