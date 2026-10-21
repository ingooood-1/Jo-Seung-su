# -*- coding: utf-8 -*-
"""
Generate Pure 9:16 Magazine Card Shorts Videos (NO OTHER UI OVERLAYS)
Matches user's exact scrapbook magazine card specification.
"""

import os
import sys
import subprocess
import mutagen.mp3
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

sys.stdout.reconfigure(encoding='utf-8')

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
FONT_BOLD = 'C:/Windows/Fonts/malgunbd.ttf'
FONT_REG = 'C:/Windows/Fonts/malgun.ttf'

W, H = 720, 1280

def wrap_text(text, max_chars=28):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur += (" " if cur else "") + w
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_washi_tapes(img):
    # Top-left washi tape (slanted)
    tape1 = Image.new('RGBA', (130, 40), (235, 225, 205, 220))
    tape1 = tape1.rotate(-15, expand=True)
    img.paste(tape1, (15, 90), tape1)

    # Bottom-right washi tape (slanted)
    tape2 = Image.new('RGBA', (130, 40), (94, 128, 160, 220))
    tape2 = tape2.rotate(-28, expand=True)
    img.paste(tape2, (W - 150, 480), tape2)

def create_pure_card_base(meta_tag="2026.10 SPECIAL", cut_badge="CUT 01"):
    img = Image.new('RGB', (W, H), (250, 248, 242)) # #faf8f2 warm paper
    draw = ImageDraw.Draw(img)

    # Clean paper border
    draw.rectangle([12, 12, W - 12, H - 12], outline=(228, 223, 211), width=2)

    f_meta = ImageFont.truetype(FONT_BOLD, 16)
    f_htitle = ImageFont.truetype(FONT_BOLD, 23)

    # Top Header
    draw.text((36, 38), meta_tag, fill=(30, 41, 59), font=f_meta)
    draw.text((210, 34), "DOBONG LITTLE BASEBALL NEWS", fill=(15, 23, 42), font=f_htitle)

    # Barcode
    bx = W - 105
    for bw in [4, 2, 6, 2, 4, 3, 5, 2, 4]:
        draw.rectangle([bx, 34, bx + bw, 58], fill=(15, 23, 42))
        bx += bw + 3

    # Double line
    draw.line([(32, 72), (W - 32, 72)], fill=(15, 23, 42), width=2)
    draw.line([(32, 76), (W - 32, 76)], fill=(15, 23, 42), width=1)

    return img, draw

# =========================================================================
# VOL 2: 도봉리틀 홍보영상 특강 (순수 9:16 매거진 카드 6종)
# =========================================================================
def render_vol2_card(cut_num):
    f_hand = ImageFont.truetype(FONT_BOLD, 36)
    f_sub = ImageFont.truetype(FONT_BOLD, 26)
    f_body = ImageFont.truetype(FONT_REG, 19)
    f_body_b = ImageFont.truetype(FONT_BOLD, 19)
    f_box_head = ImageFont.truetype(FONT_BOLD, 24)
    f_item = ImageFont.truetype(FONT_BOLD, 18)

    px1, py1, px2, py2 = 36, 120, W - 36, 520

    if cut_num == 1:
        img, draw = create_pure_card_base("2026.10 SPECIAL", "CUT 01")
        # Polaroid Frame
        draw.rounded_rectangle([px1, py1, px2, py2], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        # Blue gradient
        for y in range(py1 + 10, py2 - 10):
            ratio = (y - py1) / (py2 - py1)
            r = int(2 * (1 - ratio) + 30 * ratio)
            g = int(132 * (1 - ratio) + 58 * ratio)
            b = int(199 * (1 - ratio) + 138 * ratio)
            draw.line([(px1 + 10, y), (px2 - 10, y)], fill=(r, g, b))

        draw.text((220, 240), "도봉 리틀 꿈나무", fill=(255, 255, 255), font=ImageFont.truetype(FONT_BOLD, 26))
        draw.text((180, 285), "야구도, 키도 쑥쑥!", fill=(253, 224, 71), font=ImageFont.truetype(FONT_BOLD, 38))
        draw.text((260, 355), "CSS 야구센터 바이오피치 랩", fill=(191, 219, 254), font=ImageFont.truetype(FONT_BOLD, 18))
        draw_washi_tapes(img)

        # Title
        draw.text((38, 560), "야구도, 키도 쑥쑥!", fill=(15, 23, 42), font=f_hand)
        draw.text((38, 615), "초등 성장 발육 & 균형잡힌 체형 관리", fill=(2, 132, 199), font=f_sub)

        # Description
        p1 = "야구처럼 한쪽 회전력을 강하게 쓰는 편측 회전 운동일수록, 반대쪽 밸런스를 균형 있게 채워줄 때 숨은 키와 잠재력이 함께 깨어납니다!"
        p2 = "좌우 밸런스를 바로잡아주면 균형잡힌 체형 형성은 물론, 어깨와 팔꿈치 성장판 스트레스 및 관절 과부하를 대폭 줄여줍니다."
        yy = 675
        for l in wrap_text(p1, 28):
            draw.text((38, yy), l, fill=(15, 23, 42), font=f_body_b)
            yy += 32
        yy += 10
        for l in wrap_text(p2, 28):
            draw.text((38, yy), l, fill=(30, 41, 59), font=f_body)
            yy += 32

        # Sub-box
        box_y = yy + 25
        draw.rounded_rectangle([36, box_y, W - 36, box_y + 175], radius=14, fill=(255, 255, 255, 200), outline=(2, 132, 199), width=2)
        draw.text((56, box_y + 18), "성장 발육 & 부상 예방", fill=(2, 132, 199), font=f_box_head)
        draw.text((56, box_y + 65), "• 16년 임상 물리치료사 출신의 성장기 맞춤 코칭", fill=(15, 23, 42), font=f_item)
        draw.text((56, box_y + 102), "• 체형 불균형 예방 (어깨·팔꿈치 과부하 대폭 감소)", fill=(15, 23, 42), font=f_item)
        draw.text((56, box_y + 138), "• 관절 가동성 회복 (성장판을 지키는 올바른 투구 폼)", fill=(15, 23, 42), font=f_item)

        # Bottom Stamp
        stamp_y = H - 85
        draw.line([(36, stamp_y - 20), (W - 36, stamp_y - 20)], fill=(226, 232, 240), width=1)
        draw.text((38, stamp_y), "CSS 야구센터 × 도봉 리틀 야구단", fill=(71, 85, 105), font=ImageFont.truetype(FONT_BOLD, 18))
        draw.rounded_rectangle([W - 160, stamp_y - 5, W - 36, stamp_y + 30], radius=8, outline=(225, 29, 72), width=2)
        draw.text((W - 142, stamp_y + 2), "성장 케어", fill=(225, 29, 72), font=ImageFont.truetype(FONT_BOLD, 16))

    elif cut_num == 2:
        img, draw = create_pure_card_base("EXPERT INTERVIEW", "CUT 02")
        # Polaroid Frame with Park In-guk profile
        draw.rounded_rectangle([px1, py1, px2, py2], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        if os.path.exists("park_inguk_profile.jpg"):
            pk = Image.open("park_inguk_profile.jpg").convert('RGB')
            pk = pk.resize((240, 290), Image.Resampling.LANCZOS)
            img.paste(pk, (60, 160))
            draw.rectangle([60, 160, 300, 450], outline=(37, 99, 235), width=2)

        draw.text((325, 175), "가동성 컨디셔닝 디렉터", fill=(37, 99, 235), font=ImageFont.truetype(FONT_BOLD, 16))
        draw.text((325, 210), "박인국 실장", fill=(15, 23, 42), font=ImageFont.truetype(FONT_BOLD, 34))
        draw.text((325, 268), "16년 임상 경력", fill=(51, 65, 85), font=ImageFont.truetype(FONT_BOLD, 20))
        draw.text((325, 300), "물리치료사 출신", fill=(51, 65, 85), font=ImageFont.truetype(FONT_BOLD, 20))
        draw.rounded_rectangle([325, 350, 520, 395], radius=8, fill=(219, 234, 254))
        draw.text((345, 360), "2만여 명 임상 경험", fill=(30, 64, 175), font=ImageFont.truetype(FONT_BOLD, 18))
        draw_washi_tapes(img)

        # Title
        draw.text((38, 560), "2만여 명 임상 경험 담은 1:1 맞춤형 코칭", fill=(15, 23, 42), font=f_hand)
        draw.text((38, 615), "관절 안정화 & 성장기 맞춤형 가동성 코칭", fill=(5, 150, 105), font=f_sub)

        # Description
        p1 = "병원 도수치료실 16년 경력을 바탕으로, 현재 유도 엘리트 선수들의 전담 매뉴얼 코칭을 맡아 관절 안정화와 가동성을 지도하고 있습니다."
        p2 = "어린 선수들의 움직임을 정밀 분석하여 관절 손상 없이 스스로 통제하는 바른 폼을 만들어 드립니다."
        yy = 675
        for l in wrap_text(p1, 28):
            draw.text((38, yy), l, fill=(15, 23, 42), font=f_body_b)
            yy += 32
        yy += 10
        for l in wrap_text(p2, 28):
            draw.text((38, yy), l, fill=(30, 41, 59), font=f_body)
            yy += 32

        # Sub-box
        box_y = yy + 25
        draw.rounded_rectangle([36, box_y, W - 36, box_y + 175], radius=14, fill=(236, 253, 245), outline=(5, 150, 105), width=2)
        draw.text((56, box_y + 18), "핵심 전문성 & 임상 코칭 경력", fill=(6, 95, 70), font=f_box_head)
        draw.text((56, box_y + 65), "• 16년 임상 경력 물리치료사 출신 & 2만여 명 임상 케어", fill=(4, 120, 87), font=f_item)
        draw.text((56, box_y + 102), "• 現 유도 엘리트 선수 매뉴얼 코칭 전담 (관절 안정화)", fill=(4, 120, 87), font=f_item)
        draw.text((56, box_y + 138), "• 수술 후 움직임 회복 & 재활 가동성 점진 코칭", fill=(4, 120, 87), font=f_item)

        stamp_y = H - 85
        draw.line([(36, stamp_y - 20), (W - 36, stamp_y - 20)], fill=(226, 232, 240), width=1)
        draw.text((38, stamp_y), "의료법 안심 준수 전문 코칭", fill=(71, 85, 105), font=ImageFont.truetype(FONT_BOLD, 18))
        draw.rounded_rectangle([W - 160, stamp_y - 5, W - 36, stamp_y + 30], radius=8, outline=(5, 150, 105), width=2)
        draw.text((W - 142, stamp_y + 2), "전문 코칭", fill=(5, 150, 105), font=ImageFont.truetype(FONT_BOLD, 16))

    elif cut_num == 3:
        img, draw = create_pure_card_base("DOBONG LESSON 1", "CUT 03")
        draw.rounded_rectangle([px1, py1, px2, py2], radius=16, fill=(15, 23, 42), outline=(56, 189, 248), width=2)
        draw.text((120, 230), "하체 제어 & 몸통 안정화", fill=(56, 189, 248), font=ImageFont.truetype(FONT_BOLD, 36))
        draw.text((150, 290), "흔들리지 않는 기둥이 먼저!", fill=(255, 255, 255), font=ImageFont.truetype(FONT_BOLD, 30))
        draw.text((90, 365), "모양은 같아도 쓰는 근육이 다르면 능력치가 달라집니다!", fill=(253, 224, 71), font=ImageFont.truetype(FONT_BOLD, 19))
        draw_washi_tapes(img)

        draw.text((38, 560), "아이마다 체형이 다른데, 왜 폼은 다 같을까요?", fill=(15, 23, 42), font=f_hand)
        draw.text((38, 615), "몸통 무너지면 힘 전달 불가!", fill=(225, 29, 72), font=f_sub)

        p1 = "모양과 움직임은 같을지 몰라도, 쓰는 근육이 달라지면 선수의 능력치와 구속도 완전히 달라집니다!"
        p2 = "몸통에 안정성이 떨어지고 하체가 제어되지 않으면, 아무리 세게 던져도 공에 힘이 실리지 않아요."
        yy = 675
        for l in wrap_text(p1, 28):
            draw.text((38, yy), l, fill=(15, 23, 42), font=f_body_b)
            yy += 32
        yy += 10
        for l in wrap_text(p2, 28):
            draw.text((38, yy), l, fill=(30, 41, 59), font=f_body)
            yy += 32

        box_y = yy + 25
        draw.rounded_rectangle([36, box_y, W - 36, box_y + 175], radius=14, fill=(255, 241, 242), outline=(225, 29, 72), width=2)
        draw.text((56, box_y + 18), "체크 포인트 (STEP 1 & 2)", fill=(190, 18, 60), font=f_box_head)
        draw.text((56, box_y + 65), "• ① 체형 평가: 내 뼈·관절에 딱 맞는 맞춤 폼 찾기", fill=(15, 23, 42), font=f_item)
        draw.text((56, box_y + 102), "• ② 몸통 안정화: 하체가 버텨줘야 손끝까지 힘 전달", fill=(15, 23, 42), font=f_item)
        draw.text((56, box_y + 138), "• ③ 성장판 보호: 편측 회전 불균형 사전 차단", fill=(15, 23, 42), font=f_item)

        stamp_y = H - 85
        draw.line([(36, stamp_y - 20), (W - 36, stamp_y - 20)], fill=(226, 232, 240), width=1)
        draw.text((38, stamp_y), "도봉 리틀 움직임 공식 STEP 1 & 2", fill=(71, 85, 105), font=ImageFont.truetype(FONT_BOLD, 18))
        draw.rounded_rectangle([W - 160, stamp_y - 5, W - 36, stamp_y + 30], radius=8, outline=(225, 29, 72), width=2)
        draw.text((W - 142, stamp_y + 2), "핵심 원리", fill=(225, 29, 72), font=ImageFont.truetype(FONT_BOLD, 16))

    elif cut_num == 4:
        img, draw = create_pure_card_base("DOBONG LESSON 2", "CUT 04")
        draw.rounded_rectangle([px1, py1, px2, py2], radius=16, fill=(30, 58, 138), outline=(253, 224, 71), width=2)
        draw.text((115, 230), "발끝에서 손끝까지 전달!", fill=(253, 224, 71), font=ImageFont.truetype(FONT_BOLD, 36))
        draw.text((130, 290), "공과 배트에 힘이 실리는 몸", fill=(255, 255, 255), font=ImageFont.truetype(FONT_BOLD, 30))
        draw.text((100, 365), "몸통과 고관절의 큰 움직임에서 소근육으로 부드럽게!", fill=(224, 242, 254), font=ImageFont.truetype(FONT_BOLD, 19))
        draw_washi_tapes(img)

        draw.text((38, 560), "몸통·고관절 큰 회전에서 소근육으로 강력하게!", fill=(15, 23, 42), font=f_hand)
        draw.text((38, 615), "발끝 지면반력에서 손끝 채찍 방출까지", fill=(37, 99, 235), font=f_sub)

        p1 = "팔만 휘두르면 인대가 다칩니다. 몸통과 고관절의 큰 움직임에서 시작해 소근육으로 부드럽게 이어져야 합니다."
        p2 = "근육 활성화와 힘 전달 순서를 학습하여 공과 배트에 온전히 힘을 실어줍니다."
        yy = 675
        for l in wrap_text(p1, 28):
            draw.text((38, yy), l, fill=(15, 23, 42), font=f_body_b)
            yy += 32
        yy += 10
        for l in wrap_text(p2, 28):
            draw.text((38, yy), l, fill=(30, 41, 59), font=f_body)
            yy += 32

        box_y = yy + 25
        draw.rounded_rectangle([36, box_y, W - 36, box_y + 175], radius=14, fill=(239, 246, 255), outline=(37, 99, 235), width=2)
        draw.text((56, box_y + 18), "투구 메커니즘 팁 (STEP 3 & 4)", fill=(30, 64, 175), font=f_box_head)
        draw.text((56, box_y + 65), "• ③ 큰 움직임 ➔ 소근육 섬세한 컨트롤 전달", fill=(15, 23, 42), font=f_item)
        draw.text((56, box_y + 102), "• ④ 순서 학습: 발끝 지면반력 ➔ 고관절 ➔ 손끝 방출", fill=(15, 23, 42), font=f_item)
        draw.text((56, box_y + 138), "• ⑤ 회전력 증폭: 부드럽고 폭발적인 구속 향상", fill=(15, 23, 42), font=f_item)

        stamp_y = H - 85
        draw.line([(36, stamp_y - 20), (W - 36, stamp_y - 20)], fill=(226, 232, 240), width=1)
        draw.text((38, stamp_y), "도봉 리틀 움직임 공식 STEP 3 & 4", fill=(71, 85, 105), font=ImageFont.truetype(FONT_BOLD, 18))
        draw.rounded_rectangle([W - 160, stamp_y - 5, W - 36, stamp_y + 30], radius=8, outline=(37, 99, 235), width=2)
        draw.text((W - 142, stamp_y + 2), "구속 증가", fill=(37, 99, 235), font=ImageFont.truetype(FONT_BOLD, 16))

    elif cut_num == 5:
        img, draw = create_pure_card_base("DOBONG LESSON 3", "CUT 05")
        draw.rounded_rectangle([px1, py1, px2, py2], radius=16, fill=(6, 95, 70), outline=(110, 231, 183), width=2)
        draw.text((110, 230), "물결 파동처럼 스트레스 분산", fill=(110, 231, 183), font=ImageFont.truetype(FONT_BOLD, 36))
        draw.text((105, 290), "관절 스트레스 온몸으로 흡수", fill=(255, 255, 255), font=ImageFont.truetype(FONT_BOLD, 30))
        draw.text((105, 365), "물에 파동이 일어 잔잔해지듯 관절 충격 부하를 분산!", fill=(209, 250, 229), font=ImageFont.truetype(FONT_BOLD, 19))
        draw_washi_tapes(img)

        draw.text((38, 560), "물의 파동처럼 흘러야 예방! 근본 원인 개선", fill=(15, 23, 42), font=f_hand)
        draw.text((38, 615), "그냥 쉬는 건 해결책이 아니다!", fill=(6, 95, 70), font=f_sub)

        p1 = "물에 파동이 일어 잔잔해지듯 관절 스트레스(충격 부하)가 온몸으로 분산되어야 어깨와 팔꿈치를 안전하게 보호할 수 있어요."
        p2 = "통증만 잠시 잊는 단순 휴식 대신, 아픈 근본 원인을 바로잡아야 부상 예방과 기능 향상이 완성됩니다."
        yy = 675
        for l in wrap_text(p1, 28):
            draw.text((38, yy), l, fill=(15, 23, 42), font=f_body_b)
            yy += 32
        yy += 10
        for l in wrap_text(p2, 28):
            draw.text((38, yy), l, fill=(30, 41, 59), font=f_body)
            yy += 32

        box_y = yy + 25
        draw.rounded_rectangle([36, box_y, W - 36, box_y + 175], radius=14, fill=(236, 253, 245), outline=(5, 150, 105), width=2)
        draw.text((56, box_y + 18), "부상 관리 철칙 (STEP 5 & 6)", fill=(6, 95, 70), font=f_box_head)
        draw.text((56, box_y + 65), "• ⑤ 스트레스 분산: 물결처럼 부드럽게 관절 부하 분산", fill=(15, 23, 42), font=f_item)
        draw.text((56, box_y + 102), "• ⑥ 원인 개선: 바른 움직임을 완전히 내 것으로 체득", fill=(15, 23, 42), font=f_item)
        draw.text((56, box_y + 138), "• ⑦ 통증 악순환 차단: 실전 마운드 안심 복귀 지원", fill=(15, 23, 42), font=f_item)

        stamp_y = H - 85
        draw.line([(36, stamp_y - 20), (W - 36, stamp_y - 20)], fill=(226, 232, 240), width=1)
        draw.text((38, stamp_y), "도봉 리틀 움직임 공식 STEP 5 & 6", fill=(71, 85, 105), font=ImageFont.truetype(FONT_BOLD, 18))
        draw.rounded_rectangle([W - 160, stamp_y - 5, W - 36, stamp_y + 30], radius=8, outline=(5, 150, 105), width=2)
        draw.text((W - 142, stamp_y + 2), "부상 예방", fill=(5, 150, 105), font=ImageFont.truetype(FONT_BOLD, 16))

    else:
        # Cut 6: Dual Profile Pictures! (조승수 대표 & 박인국 실장 실사)
        img, draw = create_pure_card_base("SPECIAL BENEFIT", "CUT 06")
        draw.rounded_rectangle([px1, py1, px2, py2], radius=16, fill=(255, 255, 255), outline=(225, 29, 72), width=2)

        # Dual Profile Photos
        if os.path.exists("cho_seungsoo_real.jpg"):
            cs = Image.open("cho_seungsoo_real.jpg").convert('RGB')
            cs = cs.resize((270, 240), Image.Resampling.LANCZOS)
            img.paste(cs, (50, 140))
            draw.rectangle([50, 140, 320, 380], outline=(15, 23, 42), width=2)
            draw.rectangle([50, 340, 320, 380], fill=(15, 23, 42))
            draw.text((65, 348), "조승수 대표 | 실전 투구", fill=(255, 255, 255), font=ImageFont.truetype(FONT_BOLD, 16))

        if os.path.exists("park_inguk_profile.jpg"):
            pk = Image.open("park_inguk_profile.jpg").convert('RGB')
            pk = pk.resize((270, 240), Image.Resampling.LANCZOS)
            img.paste(pk, (365, 140))
            draw.rectangle([365, 140, 635, 380], outline=(15, 23, 42), width=2)
            draw.rectangle([365, 340, 635, 380], fill=(15, 23, 42))
            draw.text((380, 348), "박인국 실장 | 16년 임상", fill=(255, 255, 255), font=ImageFont.truetype(FONT_BOLD, 16))

        # Price banner
        draw.rounded_rectangle([50, 400, 635, 455], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((70, 415), "조승수 × 박인국 스페셜 맞춤 분석 [50% 지원]", fill=(15, 23, 42), font=ImageFont.truetype(FONT_BOLD, 18))
        draw.text((505, 410), "50,000원", fill=(225, 29, 72), font=ImageFont.truetype(FONT_BOLD, 26))
        draw_washi_tapes(img)

        # Title
        draw.text((38, 560), '"선수모집 & 특별 혜택" 조승수 × 박인국 콜라보', fill=(15, 23, 42), font=ImageFont.truetype(FONT_BOLD, 30))
        draw.text((38, 615), "초등학생 ~ 중1 선수모집! (입단테스트 상시 가능)", fill=(225, 29, 72), font=f_sub)

        # Description
        p1 = "조승수 감독의 전문 야구 수업과 연계하여, 16년 임상 박인국 실장의 1:1 맞춤 케어 서비스를 도봉 리틀 선수들에게 첫 방문 50% 할인 혜택(5만 원)으로 지원합니다."
        p2 = "※ 조승수 감독 야구 수업과 별개로 1:1 케어가 진행됩니다."
        yy = 675
        for l in wrap_text(p1, 28):
            draw.text((38, yy), l, fill=(15, 23, 42), font=f_body_b)
            yy += 32
        yy += 10
        draw.text((38, yy), p2, fill=(225, 29, 72), font=ImageFont.truetype(FONT_BOLD, 17))
        yy += 32

        # Sub-box / Call box
        box_y = yy + 20
        draw.rounded_rectangle([36, box_y, W - 36, box_y + 175], radius=14, fill=(255, 241, 242), outline=(225, 29, 72), width=2)
        draw.text((56, box_y + 18), "📞 입단 & 1:1 케어 상담 문의", fill=(190, 18, 60), font=f_box_head)
        draw.text((56, box_y + 65), "• 조승수 대표 직통: 010-3666-9069", fill=(225, 29, 72), font=ImageFont.truetype(FONT_BOLD, 22))
        draw.text((56, box_y + 105), "• 대상: 초등학생 ~ 중학교 1학년 야구 꿈나무", fill=(15, 23, 42), font=f_item)
        draw.text((56, box_y + 138), "• 위치: CSS 야구센터 & 바이오피치 랩", fill=(15, 23, 42), font=f_item)

        stamp_y = H - 85
        draw.line([(36, stamp_y - 20), (W - 36, stamp_y - 20)], fill=(226, 232, 240), width=1)
        draw.text((38, stamp_y), "도봉 리틀 야구단 특별 지원 프로모션", fill=(71, 85, 105), font=ImageFont.truetype(FONT_BOLD, 18))
        draw.rounded_rectangle([W - 160, stamp_y - 5, W - 36, stamp_y + 30], radius=8, outline=(225, 29, 72), width=2)
        draw.text((W - 142, stamp_y + 2), "50% 지원", fill=(225, 29, 72), font=ImageFont.truetype(FONT_BOLD, 16))

    return img

# =========================================================================
# VOL 1: 감성매거진 1호 (순수 9:16 매거진 카드 6종)
# =========================================================================
def render_vol1_card(cut_num):
    f_hand = ImageFont.truetype(FONT_BOLD, 34)
    f_sub = ImageFont.truetype(FONT_BOLD, 24)
    f_body = ImageFont.truetype(FONT_REG, 18)
    f_body_b = ImageFont.truetype(FONT_BOLD, 18)
    f_box_head = ImageFont.truetype(FONT_BOLD, 22)
    f_item = ImageFont.truetype(FONT_BOLD, 17)

    px1, py1, px2, py2 = 36, 120, W - 36, 680

    if cut_num == 1:
        ipath = "cardnews/감성매거진_01_표지_야구도키도쑥쑥.png"
        meta_tag = "VOL.01 COVER"
        title = "야구도 잘하고 키도 쑥쑥!"
        sub = "초등 성장기 성장판 보호 & 좌우 밸런스 회복"
        p1 = "초등 성장기 성장판 보호와 좌우 밸런스 회복으로 숨은 키와 폭발적인 잠재력을 깨우는 1호 감성 매거진 카드뉴스입니다."
        p2 = "한쪽만 쓰는 야구 운동의 편측 불균형을 사전에 바로잡아 건강한 성장과 관절 안전을 지켜줍니다."
        pt_head = "1호 성장 솔루션"
        pts = ["• 초등 성장기 성장판 보호 & 좌우 밸런스 회복", "• 16년 임상 물리치료사 출신의 전문 1:1 케어", "• 어깨·팔꿈치 관절 과부하 사전 차단"]
        badge = "성장 케어"
    elif cut_num == 2:
        ipath = "cardnews/감성매거진_02_메인_성장판지키며키쑥쑥.png"
        meta_tag = "GROWTH CARE"
        title = "성장판을 지키며 키 쑥쑥! 좌우 밸런스 회복"
        sub = "반대쪽 밸런스를 균형 있게 채워주는 솔루션"
        p1 = "야구는 한쪽만 쓰는 편측 회전 운동입니다! 반복적인 회전으로 굳어진 반대쪽 근육을 풀어줄 때 숨은 키가 쑥쑥 자라납니다."
        p2 = "좌우 균형이 맞아야 관절에 가해지는 충격이 고르게 분산되어 부상 없이 롱런할 수 있습니다."
        pt_head = "밸런스 회복 핵심"
        pts = ["• 편측 회전 불균형 사전 차단 및 체형 교정", "• 반대쪽 근육 이완으로 숨은 키 회복", "• 어깨 및 팔꿈치 인대 과부하 대폭 감소"]
        badge = "밸런스 회복"
    elif cut_num == 3:
        ipath = "cardnews/감성매거진_03_원인_왜또아플까.png"
        meta_tag = "CAUSE ANALYSIS"
        title = "쉬었는데 왜 또 아플까? 반복되는 통증의 비밀"
        sub = "단순 휴식만으로는 근본 원인이 해결되지 않습니다"
        p1 = "반복된 회전 동작으로 굳어진 반대쪽 근육과 틀어진 체형이 통증의 진짜 원인입니다!"
        p2 = "단순히 쉬는 것만으로는 굳은 관절이 정상 가동 범위를 되찾지 못해, 다시 공을 던지면 통증이 재발합니다."
        pt_head = "통증 재발 차단 솔루션"
        pts = ["• 아픈 근본 원인(틀어진 체형 & 가동성 결손) 교정", "• 굳은 반대쪽 근육 정밀 이완", "• 통증 재발 악순환의 연결고리 원천 차단"]
        badge = "통증 원인 개선"
    elif cut_num == 4:
        ipath = "cardnews/감성매거진_04_솔루션_3단계성장프로세스.png"
        meta_tag = "3-STEP PROCESS"
        title = "3단계 성장 프로세스: 이완 ➔ 가동성 ➔ 투구"
        sub = "체계적이고 과학적인 1:1 맞춤형 성장 케어"
        p1 = "굳은 근육 이완부터 관절 가동성 회복, 그리고 부드러운 투구 폼 연결까지 3단계로 케어합니다."
        p2 = "관절 안정성을 확보한 뒤 올바른 움직임을 학습하여 선수가 스스로 통제하는 바른 폼을 체득합니다."
        pt_head = "3단계 프로세스"
        pts = ["• STEP 1: 굳은 근육 정밀 이완 & 긴장 해소", "• STEP 2: 관절 가동 범위 정상화 & 안정성 확보", "• STEP 3: 부드럽고 안전한 실전 투구 폼 완성"]
        badge = "3단계 솔루션"
    elif cut_num == 5:
        ipath = "cardnews/감성매거진_05_원팀_조승수X박인국.png"
        meta_tag = "EXPERT ONE-TEAM"
        title = "조승수 × 박인국 스페셜 콜라보 케어"
        sub = "KBO 프로 레슨과 16년 임상 케어의 환상적 시너지"
        p1 = "KBO 프로 출신 조승수 대표의 정규 야구 기술 레슨과, 16년 임상 물리치료사 박인국 실장의 1:1 맞춤 케어가 만났습니다!"
        p2 = "실전 기술과 관절 건강을 동시에 잡는 도봉 리틀 선수들만의 특별한 원팀 시스템을 경험해 보세요."
        pt_head = "전문가 시너지"
        pts = ["• 조승수 대표: 실전 투구 폼 & 구속 메커니즘 레슨", "• 박인국 실장: 1:1 맞춤 관절 안정화 & 체형 케어", "※ 조승수 대표 야구 수업과 별개로 1:1 케어 진행"]
        badge = "전문가 원팀"
    else:
        ipath = "center_facility_3zones.jpg"
        meta_tag = "SPECIAL BENEFIT"
        title = "선수모집 & 첫 방문 50% 특별 혜택 (5만 원)"
        sub = "원스톱 3개 존 시설 완비 & 입단 테스트 진행"
        p1 = "초등학생 ~ 중학교 1학년 야구 꿈나무 선수모집! 입단 테스트와 1:1 개인레슨 상담이 상시 가능합니다."
        p2 = "실내 투구장 · 웨이트 존 · 기능성 트레이닝 원스톱 시설에서 첫 방문 50% 할인 혜택(5만 원)으로 정밀 분석을 지원합니다."
        pt_head = "📞 입단 & 1:1 케어 상담 문의"
        pts = ["• 조승수 대표 직통: 010-3666-9069", "• 시설: 실내 투구장 · 웨이트 존 · 기능성 트레이닝", "• 혜택: 도봉 리틀 선수 첫 방문 1:1 정밀 분석 50% 지원"]
        badge = "50% 혜택 지원"

    img, draw = create_pure_card_base(meta_tag, f"CUT 0{cut_num}")

    # Polaroid Frame with image
    draw.rounded_rectangle([px1, py1, px2, py2], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
    if os.path.exists(ipath):
        cimg = Image.open(ipath).convert('RGB')
        cimg.thumbnail((px2 - px1 - 20, py2 - py1 - 20), Image.Resampling.LANCZOS)
        iw, ih = cimg.size
        img.paste(cimg, (px1 + 10 + (px2 - px1 - 20 - iw) // 2, py1 + 10 + (py2 - py1 - 20 - ih) // 2))

    draw_washi_tapes(img)

    # Title & Sub
    draw.text((38, 715), title, fill=(15, 23, 42), font=f_hand)
    draw.text((38, 765), sub, fill=(2, 132, 199), font=f_sub)

    yy = 815
    for l in wrap_text(p1, 28):
        draw.text((38, yy), l, fill=(15, 23, 42), font=f_body_b)
        yy += 30
    yy += 8
    for l in wrap_text(p2, 28):
        draw.text((38, yy), l, fill=(51, 65, 85), font=f_body)
        yy += 30

    box_y = yy + 20
    draw.rounded_rectangle([36, box_y, W - 36, box_y + 160], radius=14, fill=(255, 255, 255, 220), outline=(2, 132, 199), width=2)
    draw.text((56, box_y + 15), pt_head, fill=(2, 132, 199), font=f_box_head)
    by = box_y + 55
    for pt in pts:
        draw.text((56, by), pt, fill=(15, 23, 42), font=f_item)
        by += 32

    stamp_y = H - 80
    draw.line([(36, stamp_y - 18), (W - 36, stamp_y - 18)], fill=(226, 232, 240), width=1)
    draw.text((38, stamp_y), "CSS 야구센터 × 도봉 리틀 야구단", fill=(71, 85, 105), font=ImageFont.truetype(FONT_BOLD, 18))
    draw.rounded_rectangle([W - 160, stamp_y - 5, W - 36, stamp_y + 30], radius=8, outline=(225, 29, 72), width=2)
    draw.text((W - 145, stamp_y + 2), badge, fill=(225, 29, 72), font=ImageFont.truetype(FONT_BOLD, 16))

    return img

def render_and_build_pure_video(vol_num):
    out_dir = f"pure_frames_vol{vol_num}"
    os.makedirs(out_dir, exist_ok=True)

    if vol_num == 1:
        out_mp4 = "1호_숏츠_야구도키도쑥쑥.mp4"
        audio_prefix = "audio/tts_mag_0"
    else:
        out_mp4 = "2호_숏츠_도봉리틀홍보영상특강.mp4"
        audio_prefix = "audio/tts_video_0"

    print(f"\n==========================================")
    print(f"Building Pure Card Shorts Video for Vol {vol_num}...")
    print(f"==========================================")

    frame_files = []
    cut_durations = []

    for c in range(1, 7):
        if vol_num == 1:
            frame_img = render_vol1_card(c)
        else:
            frame_img = render_vol2_card(c)

        fpath = os.path.join(out_dir, f"card_cut_{c}.png")
        frame_img.save(fpath, "PNG")
        frame_files.append(fpath)

        audio_path = f"{audio_prefix}{c}.mp3"
        duration = mutagen.mp3.MP3(audio_path).info.length
        cut_durations.append(duration)
        print(f"  [Cut {c}] Card rendered -> {fpath} ({duration:.2f}s audio)")

    # Render segments
    segment_files = []
    for c in range(1, 7):
        fpath = frame_files[c - 1]
        audio_path = f"{audio_prefix}{c}.mp3"
        seg_mp4 = os.path.join(out_dir, f"seg_{c}.mp4")
        dur = cut_durations[c - 1] + 0.35 # small breath between cuts

        cmd = [
            FFMPEG, '-y',
            '-loop', '1', '-i', fpath,
            '-i', audio_path,
            '-vf', 'scale=720:1280,format=yuv420p',
            '-c:v', 'libx264', '-preset', 'fast', '-tune', 'stillimage',
            '-c:a', 'aac', '-b:a', '192k',
            '-t', str(dur),
            seg_mp4
        ]
        subprocess.run(cmd, check=True)
        segment_files.append(seg_mp4)

    # Concat
    concat_txt = os.path.join(out_dir, "concat.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for seg in segment_files:
            abs_p = os.path.abspath(seg).replace('\\', '/')
            f.write(f"file '{abs_p}'\n")

    merged_no_bgm = os.path.join(out_dir, "merged_no_bgm.mp4")
    cmd_concat = [
        FFMPEG, '-y',
        '-f', 'concat', '-safe', '0', '-i', concat_txt,
        '-c', 'copy',
        merged_no_bgm
    ]
    subprocess.run(cmd_concat, check=True)

    # Mix BGM
    bgm_path = "audio/bgm_morning.mp3"
    cmd_final = [
        FFMPEG, '-y',
        '-i', merged_no_bgm,
        '-i', bgm_path,
        '-filter_complex', '[1:a]volume=0.10[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]',
        '-map', '0:v',
        '-map', '[aout]',
        '-c:v', 'copy',
        '-c:a', 'aac', '-b:a', '192k',
        out_mp4
    ]
    subprocess.run(cmd_final, check=True)

    size_mb = os.path.getsize(out_mp4) / (1024 * 1024)
    print(f"SUCCESS: Generated {out_mp4} ({size_mb:.2f} MB)")

if __name__ == '__main__':
    render_and_build_pure_video(1)
    render_and_build_pure_video(2)
    print("ALL PURE CARD SHORTS COMPLETED SUCCESSFULLY!")
