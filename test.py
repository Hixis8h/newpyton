import cv2
import numpy as np
import subprocess
import time
from collections import Counter


# ==================================================
# ตั้งค่า
# ==================================================

ADB = r"C:\LDPlayer\LDPlayer14\adb.exe"
DEVICE = "emulator-5554"

# ความละเอียดอ้างอิงต้นฉบับ
BASE_WIDTH = 960
BASE_HEIGHT = 540

# ตำแหน่งการ์ดอ้างอิงบนสเกล 960x540
CARDS = [
    (260, 136, 395, 314),   # 1 / A
    (407, 136, 542, 314),   # 2 / B
    (553, 136, 688, 314),   # 3 / C
    (260, 328, 395, 506),   # 4 / D
    (407, 328, 542, 506),   # 5 / E
    (553, 328, 688, 506)    # 6 / F
]

POINTS = [
    (327, 225),   # 1 / A
    (474, 225),   # 2 / B
    (620, 225),   # 3 / C
    (327, 417),   # 4 / D
    (474, 417),   # 5 / E
    (620, 417)    # 6 / F
]

INPUT_MODE = "adb"
BOT_VERSION = "v4-safe-filter-full"

CONFIRM_TIMES = 5
CONFIRM_REQUIRED = 4
CHECK_DELAY = 0.15
PRESS_DELAY = 1.2
STATE_TIMEOUT = 5.0
ROUND_WAIT_SECONDS = 180  # พัก 3 นาทีหลังครบ 3 ชุด
HEADER_Y_RATIO = 0.20


# ==================================================
# ADB & Screenshot
# ==================================================

def adb_run(args, timeout=5):
    try:
        return subprocess.run(
            [ADB, "-s", DEVICE] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=timeout
        )
    except Exception:
        return None


def screenshot():
    result = adb_run(["exec-out", "screencap", "-p"], timeout=5)
    if result is None or not result.stdout:
        return None
    return cv2.imdecode(np.frombuffer(result.stdout, np.uint8), cv2.IMREAD_COLOR)


# ==================================================
# ตรวจสอบกรอบการ์ดแบบเข้มงวด (ป้องกันการจับตัวละคร/ฉากหลัง)
# ==================================================

def is_fixed_card_present(img, rect):
    x1, y1, w, h = rect
    img_h, img_w = img.shape[:2]
    x1 = max(0, min(img_w - 1, x1))
    x2 = max(x1 + 1, min(img_w, x1 + w))
    y1 = max(0, min(img_h - 1, y1))
    y2 = max(y1 + 1, min(img_h, y1 + h))
    
    crop = img[y1:y2, x1:x2]
    if crop.size == 0:
        return False

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    
    # เช็คขอบการ์ดต้องมีความเข้มชัดเจน
    edges = cv2.Canny(gray, 50, 150)
    edge_ratio = float(np.mean(edges > 0))

    px = max(2, int(crop.shape[1] * 0.08))
    py = max(2, int(crop.shape[0] * 0.08))
    border = np.concatenate([
        gray[:py, :].ravel(),
        gray[-py:, :].ravel(),
        gray[:, :px].ravel(),
        gray[:, -px:].ravel(),
    ])
    dark_ratio = float(np.mean(border < 150))

    return edge_ratio >= 0.02 and dark_ratio >= 0.015


def get_card_state(img):
    if img is None:
        return {}
    
    h, w = img.shape[:2]
    sx = w / float(BASE_WIDTH)
    sy = h / float(BASE_HEIGHT)
    
    slots = {}
    for slot, (x1, y1, x2, y2) in enumerate(CARDS):
        rx1 = int(round(x1 * sx))
        ry1 = int(round(y1 * sy))
        rx2 = int(round(x2 * sx))
        ry2 = int(round(y2 * sy))
        rect = (rx1, ry1, rx2 - rx1, ry2 - ry1)
        
        if is_fixed_card_present(img, rect):
            slots[slot] = rect
            
    return slots


# ==================================================
# หา Header "Tries left" เฉพาะจุดตรงกลางด้านบน
# ==================================================

def find_header(img):
    if img is None:
        return None

    h, w = img.shape[:2]
    # ค้นหาเฉพาะโซนด้านบนตรงกลาง (ตัดขอบซ้าย/ขวาและล่างออก เพื่อไม่ให้โดนตัวละครหรือฉากหลัง)
    upper = img[int(h * 0.05):int(h * HEADER_Y_RATIO), int(w * 0.25):int(w * 0.75)]
    
    if upper.size == 0:
        return None

    b, g, r = cv2.split(upper)

    mask = (
        (r > 70) & (r < 180) &
        (g > 35) & (g < 115) &
        (b > 5) & (b < 90)
    ).astype(np.uint8) * 255

    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = []

    for c in contours:
        x, y, cw, ch = cv2.boundingRect(c)
        if cw < w * 0.10 or ch < h * 0.02 or ch > h * 0.10:
            continue
        if cw / max(ch, 1) < 2.5:
            continue
        candidates.append((x, y, cw, ch, cw * ch))

    if not candidates:
        return None

    candidates.sort(key=lambda x: x[4], reverse=True)
    bx, by, bcw, bch, _ = candidates[0]
    return (bx + int(w * 0.25), by + int(h * 0.05), bcw, bch)


def get_first_digit(img):
    header = find_header(img)
    if header is None:
        return None

    x, y, w, h = header
    crop = img[y:y+h, x:x+w]
    if crop.size == 0:
        return None

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (202, 34), interpolation=cv2.INTER_AREA)
    return gray[4:31, 115:137].copy()


def compare_first_digit(reference, current):
    if reference is None or current is None:
        return None
    current = cv2.resize(current, (reference.shape[1], reference.shape[0]), interpolation=cv2.INTER_AREA)
    return float(np.mean(np.abs(reference.astype(np.float32) - current.astype(np.float32))))


# ==================================================
# Crop และ Feature
# ==================================================

def crop_card(img, rect):
    x, y, w, h = rect
    pad_x, pad_y = int(w * 0.08), int(h * 0.08)
    return img[max(0, y + pad_y):min(img.shape[0], y + h - pad_y), max(0, x + pad_x):min(img.shape[1], x + w - pad_x)]


def make_feature(img):
    if img is None or img.size == 0:
        return None
    img = cv2.resize(img, (80, 110), interpolation=cv2.INTER_AREA)
    hsv, gray = cv2.cvtColor(img, cv2.COLOR_BGR2HSV), cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    hist = cv2.calcHist([hsv], [0, 1], None, [16, 16], [0, 180, 0, 256])
    cv2.normalize(hist, hist)

    small_gray = cv2.resize(gray, (32, 44), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
    edges = cv2.resize(cv2.Canny(gray, 40, 120), (32, 44), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0

    return np.concatenate([hist.flatten(), small_gray.flatten(), edges.flatten()])


def get_features_dict(img, slots):
    return {slot: make_feature(crop_card(img, rect)) for slot, rect in slots.items()}


def feature_difference(a, b):
    if a is None or b is None:
        return 999999.0
    return float(np.linalg.norm(a - b))


# ==================================================
# หาคู่การ์ด
# ==================================================

def detect_pair(img=None, expected_count=6):
    if img is None:
        img = screenshot()
    if img is None or find_header(img) is None:
        return None, None, None

    slots = get_card_state(img)
    if len(slots) != expected_count:
        return None, None, None

    features = get_features_dict(img, slots)
    active = [i for i, f in features.items() if f is not None]

    if len(active) != expected_count:
        return None, None, None

    if expected_count == 5:
        scores = {i: float(np.mean([feature_difference(features[i], features[j]) for j in active if j != i])) for i in active}
        outlier = max(scores, key=scores.get)
        ordered = sorted(scores.values(), reverse=True)
        gap = ordered[0] - ordered[1] if len(ordered) > 1 else 0.0
        return (int(outlier), None), scores, float(gap)

    if expected_count == 6:
        import itertools
        best_same, best_inside = None, float('inf')

        for group in itertools.combinations(active, 4):
            ds = [feature_difference(features[i], features[j]) for i, j in itertools.combinations(group, 2)]
            inside = float(np.mean(ds))
            if inside < best_inside:
                best_inside, best_same = inside, set(group)

        if best_same is None:
            return None, None, None

        pair = tuple(sorted(set(active) - best_same))
        if len(pair) != 2:
            return None, None, None

        outside = [feature_difference(features[i], features[j]) for i in pair for j in sorted(best_same)]
        gap = (float(np.mean(outside)) if outside else 0.0) - best_inside
        return pair, None, float(gap)

    return None, None, None


def confirm_pair(required_count=6):
    results = []
    label = 'คู่ 2 ใบ' if required_count == 6 else 'ใบต่าง 1 ใบ'
    print(f'กำลังตรวจการ์ด {required_count} ใบ → หา{label}...')

    for i in range(CONFIRM_TIMES):
        pair, _, gap = detect_pair(expected_count=required_count)
        if pair is None:
            time.sleep(CHECK_DELAY)
            continue
        results.append(pair)
        text = f'ช่อง {pair[0] + 1} และ {pair[1] + 1}' if required_count == 6 else f'ช่อง {pair[0] + 1}'
        print(f'ตรวจครั้งที่ {i + 1}: {text} | gap={gap:.2f}')
        time.sleep(CHECK_DELAY)

    if len(results) < CONFIRM_REQUIRED:
        print('ผลตรวจไม่พอ → ไม่กด')
        return None

    result, count = Counter(results).most_common(1)[0]
    print(f'ผลที่ตรงกันมากที่สุด: {tuple(x + 1 for x in result if x is not None)} ({count}/{CONFIRM_TIMES})')
    return result


# ==================================================
# กดการ์ด
# ==================================================

def tap_card(number, slots=None):
    print(f"กดช่อง {number + 1} ({chr(ord('A') + number)})")
    
    img = screenshot()
    if img is None:
        return False
        
    if slots is None:
        slots = get_card_state(img)
        
    rect = slots.get(number)
    if rect is not None:
        rx, ry, rw, rh = rect
        cx = int(rx + rw / 2)
        cy = int(ry + rh / 2)
    else:
        h, w = img.shape[:2]
        sx, sy = w / float(BASE_WIDTH), h / float(BASE_HEIGHT)
        x, y = POINTS[number]
        cx = int(round(x * sx))
        cy = int(round(y * sy))

    res = adb_run(["shell", "input", "tap", str(cx), str(cy)])
    return res is not None and res.returncode == 0


# ==================================================
# รอผลลัพธ์
# ==================================================

def wait_first_card_result(number):
    print("รอผลใบที่ 1...")
    start = time.time()
    while time.time() - start < STATE_TIMEOUT:
        slots = get_card_state(screenshot())
        if len(slots) == 5:
            return "CORRECT"
        if len(slots) == 6:
            return "WRONG"
        time.sleep(CHECK_DELAY)
    return "TIMEOUT"


def wait_second_card_result(set_number, baseline_digit):
    print(f"รอผลชุดที่ {set_number}...")
    start = time.time()
    while time.time() - start < STATE_TIMEOUT:
        img = screenshot()
        digit = get_first_digit(img)

        if baseline_digit is not None and digit is not None:
            diff = compare_first_digit(baseline_digit, digit)
            if diff is not None and diff < 6.0:
                return "WRONG"

        if set_number < 3 and baseline_digit is not None and digit is not None:
            if compare_first_digit(baseline_digit, digit) >= 6.0:
                return "CORRECT"

        if set_number == 3:
            if len(get_card_state(img)) < 5:
                return "CORRECT"

        time.sleep(CHECK_DELAY)
    return "TIMEOUT"


def wait_full_card_screen(required_count=6):
    while True:
        img = screenshot()
        if img is not None and find_header(img) is not None:
            slots = get_card_state(img)
            if len(slots) == required_count:
                h, w = img.shape[:2]
                print(f"[OK] พบหน้าจอการ์ด {required_count} ใบ (Resolution: {w}x{h})")
                return img
        print(f"[WAIT] รอหน้าจอการ์ด {required_count} ใบ...")
        time.sleep(0.3)


# ==================================================
# เล่น 1 ชุด
# ==================================================

def play_one_set(set_number, baseline_digit):
    print(f'\n{"="*55}\nเริ่มชุดที่ {set_number}\n{"="*55}')
    
    wait_full_card_screen(required_count=6)

    pair = confirm_pair(6)
    if pair is None:
        return 'RETRY'

    a, b = pair
    slots = get_card_state(screenshot())
    if not tap_card(a, slots):
        return 'RETRY'

    if wait_first_card_result(a) != 'CORRECT':
        return 'WRONG'

    time.sleep(PRESS_DELAY)

    second_pair = confirm_pair(5)
    if second_pair is None:
        return 'RETRY'

    second = second_pair[0]
    slots = get_card_state(screenshot())
    if not tap_card(second, slots):
        return 'RETRY'

    result = wait_second_card_result(set_number, baseline_digit)
    if result == 'CORRECT':
        print(f'ชุดที่ {set_number} ถูกต้อง ✓')
        return 'CORRECT'
    if result == 'WRONG':
        print(f'ชุดที่ {set_number} ผิด ✗')
        return 'WRONG'
    return 'RETRY'


# ==================================================
# MAIN
# ==================================================

def main():
    print(f'{"="*60}\nCOOKIE RUN CARD BOT - Safe Filter Full\n{"="*60}')
    
    if adb_run(["shell", "echo", "READY"]) is None:
        print("ไม่สามารถเชื่อมต่อ ADB ได้")
        return

    print("รอหน้าจอเกม (6 ใบ)...")
    while True:
        img = wait_full_card_screen(required_count=6)
        baseline_digit = get_first_digit(img)
        if baseline_digit is not None:
            print("เก็บ reference ของ 3/3 แล้ว")
            break
        time.sleep(0.3)

    while True:
        set_number = 1
        while set_number <= 3:
            result = play_one_set(set_number, baseline_digit)
            if result == "CORRECT":
                set_number += 1
            elif result == "WRONG":
                print(f'\n{"="*55}\nผิด → RESET เป็นชุด 1\n{"="*55}')
                set_number = 1
                wait_full_card_screen(required_count=6)
            else:
                time.sleep(0.3)

        print(f'\n{"="*60}\n████ ผ่านครบ 3 ชุดแล้ว ✓ ████\nพักการทำงานเป็นเวลา {ROUND_WAIT_SECONDS // 60} นาที...\n{"="*60}')
        
        for remaining in range(ROUND_WAIT_SECONDS, 0, -1):
            mins, secs = divmod(remaining, 60)
            print(f'กำลังพักเครื่อง... เหลือเวลาอีก {mins:02d}:{secs:02d}', end='\r')
            time.sleep(1)
        print('\nหมดเวลาพัก! เริ่มรอบใหม่...')
        wait_full_card_screen(required_count=6)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n{"="*60}\nหยุดการทำงาน\n{"="*60}')