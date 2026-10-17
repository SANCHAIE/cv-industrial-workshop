# ตรวจความพร้อมของเครื่องก่อนวันอบรม  รัน: uv run check_setup.py  (หรือ python check_setup.py)
import importlib
import os
import platform
import shutil
import sys

OK, NG = chr(9989) + ' ', chr(10060) + ' '
results = []


def check(name, fn, fix):
    try:
        info = fn()
        print(OK + name + '  ' + str(info))
        results.append(True)
    except Exception as e:
        print(NG + name + '  ' + str(e)[:80])
        print('     วิธีแก้: ' + fix)
        results.append(False)


def ver(mod, attr='__version__'):
    m = importlib.import_module(mod)
    return getattr(m, attr, 'ok')


HERE = os.path.dirname(os.path.abspath(__file__))
print('ตรวจความพร้อม: ' + platform.system() + ' ' + platform.release() + '   Python ' + sys.version.split()[0])
print('โฟลเดอร์: ' + HERE)
print()
check('Python 3.12', lambda: sys.version.split()[0] if sys.version_info[:2] == (3, 12) else (_ for _ in ()).throw(Exception('ได้ ' + sys.version.split()[0])),
      'ใช้ start_windows.bat / start_mac.command ซึ่งติดตั้ง Python 3.12 ให้เอง')
check('OpenCV', lambda: ver('cv2'), 'uv sync')
check('numpy', lambda: ver('numpy'), 'uv sync')
check('scikit-learn (AI)', lambda: ver('sklearn'), 'uv sync')
check('matplotlib', lambda: ver('matplotlib'), 'uv sync')
check('streamlit (web app)', lambda: ver('streamlit'), 'uv sync')
check('pypylon (กล้อง Basler)', lambda: ver('pypylon', '__version__'), 'uv sync')


def emu():
    import contextlib, io
    sys.path.insert(0, os.path.join(HERE, 'scripts'))
    from vision_camera import grab_one
    with contextlib.redirect_stdout(io.StringIO()):
        f = grab_one('emu', image='shapes.png')
    return 'กล้องจำลองถ่ายได้ ' + str(f.shape[1]) + 'x' + str(f.shape[0])


check('กล้อง Basler จำลอง', emu, 'ติดตั้งใหม่ด้วย uv sync แล้วลองอีกครั้ง')
check('ภาพตัวอย่าง images/', lambda: str(len(os.listdir(os.path.join(HERE, 'images')))) + ' รายการ',
      'ดาวน์โหลด ZIP จาก GitHub ใหม่ ให้ได้โฟลเดอร์ images ครบ')


def tess():
    import pytesseract
    win = 'C:' + chr(92) + 'Program Files' + chr(92) + 'Tesseract-OCR' + chr(92) + 'tesseract.exe'
    if shutil.which('tesseract') is None and os.path.exists(win):
        pytesseract.pytesseract.tesseract_cmd = win
    return 'Tesseract ' + str(pytesseract.get_tesseract_version())


check('Tesseract OCR (ใช้วันที่ 2)', tess,
      'Windows: ติดตั้งจาก github.com/UB-Mannheim/tesseract/wiki   Mac: brew install tesseract')


def real_cam():
    from pypylon import pylon
    devs = [d for d in pylon.TlFactory.GetInstance().EnumerateDevices() if d.GetDeviceClass() != 'BaslerCamEmu']
    if not devs:
        return 'ไม่ได้ต่อกล้องจริง (ปกติสำหรับวันแรก)'
    return 'พบ ' + devs[0].GetModelName()


check('กล้อง Basler จริง (ไม่บังคับ)', real_cam, 'เช็กสาย LAN / PoE ตั้งการ์ดแลนเป็น Auto IP')
print()
n_ok = sum(results)
need = results[:9]
if all(need):
    print('พร้อมสำหรับวันที่ 1 แล้ว  (' + str(n_ok) + '/' + str(len(results)) + ' รายการผ่าน)')
else:
    print('ยังไม่พร้อม  ผ่าน ' + str(n_ok) + '/' + str(len(results)) + '  ถ่ายภาพหน้าจอนี้ส่งให้ TA')
