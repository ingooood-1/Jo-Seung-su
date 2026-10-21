# -*- coding: utf-8 -*-
"""
Generate 9:16 Mobile MP4 Shorts Videos for Work 1 and Work 2
with synchronized audio (TTS voice + background music with ducking).
"""

import os
import subprocess
import mutagen.mp3
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
FONT_BOLD = 'C:/Windows/Fonts/malgunbd.ttf'
FONT_REG = 'C:/Windows/Fonts/malgun.ttf'

W, H = 720, 1280

def create_base_canvas(vol_num, cut_num, total_cuts=6):
    """Create the 9:16 dark gradient canvas with top progress bars and side actions."""
    img = Image.new('RGB', (W, H), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    # Vertical gradient from #0b132b to #020617
    for y in range(H):
        ratio = y / H
        r = int(11 * (1 - ratio) + 2 * ratio)
        g = int(19 * (1 - ratio) + 6 * ratio)
        b = int(43 * (1 - ratio) + 23 * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Top progress bars
    bar_pad = 20
    bar_gap = 6
    avail_w = W - 2 * bar_pad - (total_cuts - 1) * bar_gap
    seg_w = avail_w / total_cuts
    bar_y = 22
    bar_h = 5

    for c in range(1, total_cuts + 1):
        x1 = bar_pad + (c - 1) * (seg_w + bar_gap)
        x2 = x1 + seg_w
        if c < cut_num:
            fill = (255, 255, 255)
        elif c == cut_num:
            fill = (56, 189, 248) # Cyan highlight
        else:
            fill = (71, 85, 105)
        draw.rounded_rectangle([x1, bar_y, x2, bar_y + bar_h], radius=3, fill=fill)

    # Top Header Pill
    f_header = ImageFont.truetype(FONT_BOLD, 16)
    vol_title = "1호 숏츠 · 성장판 & 밸런스" if vol_num == 1 else "2호 숏츠 · 도봉리틀 홍보특강"
    badge_text = f"⚾ CSS 야구센터 × 도봉리틀  |  {vol_title} ({cut_num}/{total_cuts})"
    draw.rounded_rectangle([20, 36, 470, 68], radius=16, fill=(15, 23, 42), outline=(56, 189, 248), width=1)
    draw.text((34, 43), badge_text, fill=(255, 255, 255), font=f_header)

    # Side Floating Action Buttons (Right side x=625)
    f_side = ImageFont.truetype(FONT_BOLD, 12)
    actions = [
        ("❤️", "1.4K", (244, 63, 94)),
        ("💬", "공유", (226, 232, 240)),
        ("🔊", "음성", (56, 189, 248)),
        ("📞", "상담", (225, 29, 72))
    ]
    start_y = 660
    for idx, (icon, label, color) in enumerate(actions):
        cy = start_y + idx * 76
        # Circle
        draw.ellipse([630, cy, 686, cy + 56], fill=(20, 30, 50), outline=(255, 255, 255), width=1)
        # Icon
        draw.text((646, cy + 10), icon, fill=color, font=ImageFont.truetype(FONT_BOLD, 18))
        # Label
        bbox = draw.textbbox((0, 0), label, font=f_side)
        lw = bbox[2] - bbox[0]
        draw.text((658 - lw // 2, cy + 34), label, fill=(241, 245, 249), font=f_side)

    # Bottom Profile Row
    avatar_path = "cho_seungsoo_real.jpg"
    if os.path.exists(avatar_path):
        try:
            av = Image.open(avatar_path).convert('RGB')
            av = av.resize((48, 48), Image.Resampling.LANCZOS)
            mask = Image.new('L', (48, 48), 0)
            ImageDraw.Draw(mask).ellipse((0, 0, 48, 48), fill=255)
            img.paste(av, (24, 915), mask)
            draw.ellipse([24, 915, 72, 963], outline=(56, 189, 248), width=2)
        except Exception:
            pass

    f_pname = ImageFont.truetype(FONT_BOLD, 17)
    draw.text((82, 920), "CSS 야구센터 × 도봉리틀", fill=(255, 255, 255), font=f_pname)
    
    # CTA badge
    cta_pill = "입단 상담 010-3666-9069" if cut_num < 6 else "50% 혜택 신청 010-3666-9069"
    draw.rounded_rectangle([82, 942, 280, 964], radius=11, fill=(225, 29, 72))
    draw.text((92, 945), cta_pill, fill=(255, 255, 255), font=ImageFont.truetype(FONT_BOLD, 12))

    # Bottom Audio Ticker
    draw.text((26, 1230), "🎵 조승수 센터 공식 사운드트랙 · 모닝 어쿠스틱", fill=(148, 163, 184), font=ImageFont.truetype(FONT_REG, 13))

    return img

def render_vol1_cut(cut_num, title, desc):
    """Render frame for Vol 1 (야구도 잘하고 키도 쑥쑥)."""
    img = create_base_canvas(vol_num=1, cut_num=cut_num)
    draw = ImageDraw.Draw(img)

    card_bg = (10, 15, 30)

    # Image source
    if cut_num == 1:
        ipath = "cardnews/감성매거진_01_표지_야구도키도쑥쑥.png"
    elif cut_num == 2:
        ipath = "cardnews/감성매거진_02_메인_성장판지키며키쑥쑥.png"
    elif cut_num == 3:
        ipath = "cardnews/감성매거진_03_원인_왜또아플까.png"
    elif cut_num == 4:
        ipath = "cardnews/감성매거진_04_솔루션_3단계성장프로세스.png"
    elif cut_num == 5:
        ipath = "cardnews/감성매거진_05_원팀_조승수X박인국.png"
    else:
        ipath = "center_facility_3zones.jpg"

    if os.path.exists(ipath):
        cimg = Image.open(ipath).convert('RGB')
        
        # Rounded frame background
        draw.rounded_rectangle([25, 85, 595, 895], radius=20, fill=card_bg, outline=(56, 189, 248), width=2)
        
        # Fit image
        cimg.thumbnail((550, 740), Image.Resampling.LANCZOS)
        iw, ih = cimg.size
        px = 25 + (570 - iw) // 2
        py = 85 + (810 - ih) // 2
        img.paste(cimg, (px, py))

        # For Cut 6: Add facility zone tags
        if cut_num == 6:
            draw.rounded_rectangle([40, 780, 580, 880], radius=12, fill=(15, 23, 42), outline=(225, 29, 72), width=2)
            f_fac = ImageFont.truetype(FONT_BOLD, 15)
            draw.text((55, 792), "⚾ 3개 존 원스톱 시설 완비", fill=(253, 224, 71), font=f_fac)
            draw.text((55, 818), "• 실내 투구장  • 웨이트 존  • 기능성 트레이닝", fill=(255, 255, 255), font=ImageFont.truetype(FONT_REG, 14))
            draw.text((55, 846), "선수모집 & 첫 방문 50% 특별 혜택 (5만 원)", fill=(244, 63, 94), font=f_fac)

    # Subtitles Box at bottom
    draw.rounded_rectangle([24, 980, 605, 1215], radius=16, fill=(15, 23, 42), outline=(56, 189, 248), width=1)
    
    # Title
    f_stitle = ImageFont.truetype(FONT_BOLD, 22)
    draw.text((40, 995), title, fill=(253, 224, 71), font=f_stitle)
    
    # Desc text wrapped
    f_desc = ImageFont.truetype(FONT_REG, 16)
    lines = wrap_text(desc, 32)
    dy = 1040
    for line in lines[:5]:
        draw.text((40, dy), line, fill=(241, 245, 249), font=f_desc)
        dy += 28

    return img

def render_vol2_cut(cut_num, title, desc):
    """Render frame for Vol 2 (도봉리틀 홍보영상 특강)."""
    img = create_base_canvas(vol_num=2, cut_num=cut_num)
    draw = ImageDraw.Draw(img)

    # Frame
    draw.rounded_rectangle([25, 85, 595, 895], radius=20, fill=(250, 248, 242), outline=(225, 29, 72), width=2)

    f_card_header = ImageFont.truetype(FONT_BOLD, 14)
    f_card_body = ImageFont.truetype(FONT_REG, 16)
    f_card_bold = ImageFont.truetype(FONT_BOLD, 17)

    if cut_num == 1:
        # Cover Graphic
        draw.rounded_rectangle([45, 110, 575, 150], radius=8, fill=(2, 132, 199))
        draw.text((60, 118), "DOBONG LITTLE SPECIAL ISSUE · 2026.10", fill=(255, 255, 255), font=f_card_header)
        
        # Center Banner Box
        draw.rounded_rectangle([45, 175, 575, 520], radius=18, fill=(30, 58, 138))
        draw.text((120, 240), "⚾ 도봉 리틀 꿈나무를 위한", fill=(253, 224, 71), font=ImageFont.truetype(FONT_BOLD, 26))
        draw.text((95, 290), "성장 발육 & 균형 체형 특강", fill=(255, 255, 255), font=ImageFont.truetype(FONT_BOLD, 30))
        draw.text((170, 360), "CSS 야구센터 바이오피치 랩", fill=(191, 219, 254), font=ImageFont.truetype(FONT_BOLD, 18))
        draw.rounded_rectangle([190, 420, 430, 465], radius=20, fill=(225, 29, 72))
        draw.text((215, 432), "★ 6대 움직임 특강 ★", fill=(255, 255, 255), font=f_card_bold)

        # Bottom bullet box
        draw.rounded_rectangle([45, 545, 575, 860], radius=14, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
        draw.text((65, 570), "💡 초등 성장기 왜 밸런스가 중요할까요?", fill=(15, 23, 42), font=f_card_bold)
        pts = [
            "✔ 야구는 한쪽 회전력을 강하게 쓰는 편측 회전 운동!",
            "✔ 반대쪽 밸런스를 균형 있게 채워줄 때 숨은 키 쑥쑥!",
            "✔ 어깨와 팔꿈치 성장판 스트레스 및 충격 과부하 감소",
            "✔ 16년 임상 물리치료사 출신 박인국 실장 1:1 맞춤 코칭",
            "✔ 조승수 대표 전문 야구수업 연계 & 입단 테스트 진행"
        ]
        yy = 615
        for p in pts:
            draw.text((65, yy), p, fill=(30, 41, 59), font=f_card_body)
            yy += 38

    elif cut_num == 2:
        # Park In-guk Profile
        draw.rounded_rectangle([45, 110, 575, 150], radius=8, fill=(5, 150, 105))
        draw.text((60, 118), "EXPERT INTERVIEW · 가동성 컨디셔닝 디렉터", fill=(255, 255, 255), font=f_card_header)

        # Profile card
        draw.rounded_rectangle([45, 175, 575, 430], radius=16, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
        if os.path.exists("park_inguk_profile.jpg"):
            pimg = Image.open("park_inguk_profile.jpg").convert('RGB')
            pimg = pimg.resize((150, 185), Image.Resampling.LANCZOS)
            img.paste(pimg, (65, 205))
            draw.rectangle([65, 205, 215, 390], outline=(37, 99, 235), width=2)

        draw.text((235, 210), "가동성 컨디셔닝 디렉터", fill=(37, 99, 235), font=ImageFont.truetype(FONT_BOLD, 15))
        draw.text((235, 240), "박인국 실장", fill=(15, 23, 42), font=ImageFont.truetype(FONT_BOLD, 30))
        draw.text((235, 290), "16년 임상 경력 물리치료사 출신", fill=(51, 65, 85), font=f_card_bold)
        draw.rounded_rectangle([235, 335, 410, 370], radius=8, fill=(219, 234, 254))
        draw.text((250, 343), "2만여 명 임상 경험", fill=(30, 64, 175), font=f_card_bold)

        # Details
        draw.rounded_rectangle([45, 455, 575, 860], radius=14, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
        draw.text((65, 480), "🛡️ 핵심 전문성 & 임상 코칭 경력", fill=(6, 95, 70), font=ImageFont.truetype(FONT_BOLD, 20))
        pts2 = [
            "✔ 병원 도수치료실 16년 경력 / 2만여 명 임상 케어",
            "✔ 現 유도 엘리트 선수 매뉴얼 코칭 전담 (관절 안정화)",
            "✔ 수술 후 움직임 회복 & 재활 가동성 점진 코칭",
            "✔ 야구 투수 견관절 내회전 결손(GIRD) 특화 교정",
            "✔ 의료법 안심 준수: 안전하고 체계적인 운동 지도"
        ]
        yy = 530
        for p in pts2:
            draw.text((65, yy), p, fill=(4, 120, 87), font=f_card_body)
            yy += 42

    elif cut_num == 3:
        # STEP 1 & 2
        draw.rounded_rectangle([45, 110, 575, 150], radius=8, fill=(2, 132, 199))
        draw.text((60, 118), "DOBONG LESSON 1 · 체형 평가 & 기둥 세우기", fill=(255, 255, 255), font=f_card_header)

        draw.rounded_rectangle([45, 175, 575, 450], radius=16, fill=(15, 23, 42))
        draw.text((70, 210), "하체 제어 & 몸통 안정화", fill=(56, 189, 248), font=ImageFont.truetype(FONT_BOLD, 28))
        draw.text((70, 260), "흔들리지 않는 기둥이 먼저!", fill=(255, 255, 255), font=ImageFont.truetype(FONT_BOLD, 24))
        draw.text((70, 320), "모양은 같아도 쓰는 근육이 다르면", fill=(203, 213, 225), font=f_card_body)
        draw.text((70, 355), "선수의 능력치와 구속이 완전히 달라집니다!", fill=(253, 224, 71), font=f_card_bold)

        draw.rounded_rectangle([45, 475, 575, 860], radius=14, fill=(255, 241, 242), outline=(254, 205, 211), width=1)
        draw.text((65, 500), "🚨 몸통이 무너지면 힘 전달 불가!", fill=(190, 18, 60), font=ImageFont.truetype(FONT_BOLD, 20))
        pts3 = [
            "① 체형 평가: 아이마다 다른 관절 각도 정밀 진단",
            "② 맞춤 폼 찾기: 획일화된 폼 강요 대신 신체 맞춤화",
            "③ 몸통 안정성: 하체가 버텨줘야 손끝까지 온전히 전달",
            "④ 팔꿈치 과부하 방지: 몸통이 힘을 흡수하여 인대 보호",
            "⑤ 성장판 보호: 편측 회전 불균형 사전 차단"
        ]
        yy = 550
        for p in pts3:
            draw.text((65, yy), p, fill=(71, 85, 105), font=f_card_body)
            yy += 42

    elif cut_num == 4:
        # STEP 3 & 4
        draw.rounded_rectangle([45, 110, 575, 150], radius=8, fill=(37, 99, 235))
        draw.text((60, 118), "DOBONG LESSON 2 · 회전 파워 & 지면반력 전달", fill=(255, 255, 255), font=f_card_header)

        draw.rounded_rectangle([45, 175, 575, 450], radius=16, fill=(30, 58, 138))
        draw.text((70, 210), "발끝에서 손끝까지 전달!", fill=(253, 224, 71), font=ImageFont.truetype(FONT_BOLD, 28))
        draw.text((70, 260), "공과 배트에 온전히 힘이 실리는 몸", fill=(255, 255, 255), font=ImageFont.truetype(FONT_BOLD, 22))
        draw.text((70, 320), "팔만 휘두르면 어깨 인대가 다칩니다.", fill=(224, 242, 254), font=f_card_body)
        draw.text((70, 355), "몸통과 고관절의 큰 움직임에서 소근육으로 연결!", fill=(253, 224, 71), font=f_card_bold)

        draw.rounded_rectangle([45, 475, 575, 860], radius=14, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((65, 500), "⚡ 순서 학습 & 폭발적 구속 향상", fill=(30, 64, 175), font=ImageFont.truetype(FONT_BOLD, 20))
        pts4 = [
            "③ 큰 움직임 ➔ 소근육 섬세한 컨트롤 전달",
            "④ 지면반력 학습: 발끝 지면반력 ➔ 고관절 ➔ 척추",
            "⑤ 회전력 증폭: 견갑골 안착 후 손끝 방출 채찍 효과",
            "⑥ 불필요한 힘 제거: 부드러운 투구 폼 완성",
            "⑦ 부상 위험 0% 목표: 관절 가동 범위 최대화"
        ]
        yy = 550
        for p in pts4:
            draw.text((65, yy), p, fill=(30, 41, 59), font=f_card_body)
            yy += 42

    elif cut_num == 5:
        # STEP 5 & 6
        draw.rounded_rectangle([45, 110, 575, 150], radius=8, fill=(5, 150, 105))
        draw.text((60, 118), "DOBONG LESSON 3 · 부상 예방 & 올바른 복귀", fill=(255, 255, 255), font=f_card_header)

        draw.rounded_rectangle([45, 175, 575, 450], radius=16, fill=(6, 95, 70))
        draw.text((70, 210), "물결 파동처럼 스트레스 분산", fill=(110, 231, 183), font=ImageFont.truetype(FONT_BOLD, 28))
        draw.text((70, 260), "관절 스트레스 온몸으로 고르게 흡수", fill=(255, 255, 255), font=ImageFont.truetype(FONT_BOLD, 22))
        draw.text((70, 320), "물에 파동이 일어 잔잔해지듯", fill=(209, 250, 229), font=f_card_body)
        draw.text((70, 355), "충격 부하가 분산되어야 어깨와 팔꿈치 보호!", fill=(253, 224, 71), font=f_card_bold)

        draw.rounded_rectangle([45, 475, 575, 860], radius=14, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
        draw.text((65, 500), "🛡️ 그냥 쉬는 건 해결책이 아니다!", fill=(6, 95, 70), font=ImageFont.truetype(FONT_BOLD, 20))
        pts5 = [
            "⑤ 스트레스 분산: 특정 관절 쏠림 없이 온몸으로 분산",
            "⑥ 통증 원인 개선: 단순 휴식 후 재발하는 악순환 차단",
            "⑦ 가동성 점진 회복: 굳은 관절 유연성 및 안정성 확보",
            "⑧ 바른 움직임 체득: 선수가 스스로 인지하고 컨트롤",
            "⑨ 안심 복귀 솔루션: 실전 마운드 투구 복귀까지 연계"
        ]
        yy = 550
        for p in pts5:
            draw.text((65, yy), p, fill=(4, 120, 87), font=f_card_body)
            yy += 42

    else:
        # Cut 6: Dual Profile (조승수 대표 & 박인국 실장 복원!)
        draw.rounded_rectangle([45, 100, 575, 140], radius=8, fill=(225, 29, 72))
        draw.text((60, 110), "SPECIAL BENEFIT · 도봉 리틀 특별 프로모션", fill=(255, 255, 255), font=f_card_header)

        # Dual Profile Frame
        draw.rounded_rectangle([45, 155, 575, 460], radius=16, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
        
        # Cho Seung-soo photo
        if os.path.exists("cho_seungsoo_real.jpg"):
            cs = Image.open("cho_seungsoo_real.jpg").convert('RGB')
            cs = cs.resize((230, 210), Image.Resampling.LANCZOS)
            img.paste(cs, (65, 175))
            draw.rectangle([65, 175, 295, 385], outline=(15, 23, 42), width=2)
            draw.rectangle([65, 355, 295, 385], fill=(15, 23, 42))
            draw.text((75, 362), "조승수 대표 | 실전 투구", fill=(255, 255, 255), font=f_card_header)

        # Park In-guk photo
        if os.path.exists("park_inguk_profile.jpg"):
            pk = Image.open("park_inguk_profile.jpg").convert('RGB')
            pk = pk.resize((230, 210), Image.Resampling.LANCZOS)
            img.paste(pk, (325, 175))
            draw.rectangle([325, 175, 555, 385], outline=(15, 23, 42), width=2)
            draw.rectangle([325, 355, 555, 385], fill=(15, 23, 42))
            draw.text((335, 362), "박인국 실장 | 16년 임상", fill=(255, 255, 255), font=f_card_header)

        # Price banner
        draw.rounded_rectangle([65, 400, 555, 445], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((80, 412), "조승수 × 박인국 스페셜 맞춤 분석 [50% 지원]", fill=(15, 23, 42), font=f_card_bold)
        draw.text((455, 410), "50,000원", fill=(225, 29, 72), font=ImageFont.truetype(FONT_BOLD, 22))

        # Bottom bullet and CTA
        draw.rounded_rectangle([45, 480, 575, 860], radius=14, fill=(255, 241, 242), outline=(254, 205, 211), width=1)
        draw.text((65, 505), "📢 초등학생 ~ 중1 야구 선수모집!", fill=(190, 18, 60), font=ImageFont.truetype(FONT_BOLD, 22))
        pts6 = [
            "✔ 입단테스트 상시 가능! 1:1 개인레슨 전문 상담",
            "✔ KBO 프로 출신 조승수 대표의 정규 야구 기술 수업",
            "✔ 16년 임상 박인국 실장의 1:1 맞춤 성장판 케어",
            "✔ 도봉 리틀 선수 첫 방문 50% 할인 특별 지원 (5만 원)",
            "※ 조승수 대표 야구 수업과 별개로 1:1 케어가 진행됩니다."
        ]
        yy = 550
        for p in pts6:
            draw.text((65, yy), p, fill=(30, 41, 59), font=f_card_body)
            yy += 38

        # Call Box
        draw.rounded_rectangle([65, 770, 555, 840], radius=12, fill=(225, 29, 72))
        draw.text((100, 792), "📞 입단 & 1:1 케어 문의: 010-3666-9069", fill=(255, 255, 255), font=ImageFont.truetype(FONT_BOLD, 20))

    # Subtitles Box at bottom
    draw.rounded_rectangle([24, 980, 605, 1215], radius=16, fill=(15, 23, 42), outline=(225, 29, 72), width=1)
    
    # Title
    f_stitle = ImageFont.truetype(FONT_BOLD, 21)
    draw.text((40, 995), title, fill=(253, 224, 71), font=f_stitle)
    
    # Desc text wrapped
    f_desc = ImageFont.truetype(FONT_REG, 16)
    lines = wrap_text(desc, 32)
    dy = 1040
    for line in lines[:5]:
        draw.text((40, dy), line, fill=(241, 245, 249), font=f_desc)
        dy += 28

    return img

def wrap_text(text, max_chars=32):
    """Simple Korean text word wrapping."""
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

def build_video_for_volume(vol_num):
    """Build MP4 video for Vol 1 or Vol 2."""
    out_dir = f"temp_frames_vol{vol_num}"
    os.makedirs(out_dir, exist_ok=True)

    if vol_num == 1:
        out_mp4 = "1호_숏츠_야구도키도쑥쑥.mp4"
        cuts_data = [
            ("⚾ 야구도 잘하고 키도 쑥쑥!", "초등 성장기 성장판 보호 & 좌우 밸런스 회복 솔루션! 1호 감성 매거진 숏츠"),
            ("성장판을 지키며 키 쑥쑥! 좌우 밸런스 회복", "야구는 한쪽 회전력을 강하게 쓰는 운동! 반대쪽 밸런스를 균형 있게 채워줄 때 숨은 키와 잠재력이 함께 깨어납니다."),
            ("쉬었는데 왜 또 아플까? 반복되는 통증의 비밀", "반복된 회전 동작으로 굳어진 반대쪽 근육과 틀어진 체형이 통증의 진짜 원인! 단순 휴식만으론 해결되지 않습니다."),
            ("3단계 성장 프로세스: 이완 ➔ 가동성 ➔ 투구", "굳은 근육 이완부터 관절 가동성 회복, 그리고 부드러운 투구 폼 연결까지 체계적으로 케어합니다."),
            ("조승수 × 박인국 스페셜 콜라보 케어", "KBO 프로 출신 조승수 대표의 정규 야구 기술 레슨과 16년 임상 박인국 실장의 1:1 맞춤 성장판 케어의 환상적인 시너지!"),
            ("선수모집 & 첫 방문 50% 특별 혜택 (5만 원)", "초등~중1 선수모집! 실내 투구장 · 웨이트 존 · 기능성 트레이닝 원스톱 시설에서 정밀 분석을 지원합니다. (문의: 010-3666-9069)")
        ]
        audio_prefix = "audio/tts_mag_0"
    else:
        out_mp4 = "2호_숏츠_도봉리틀홍보영상특강.mp4"
        cuts_data = [
            ("⚾ 야구도 잘하고 키도 쑥쑥! 초등 성장 발육", "야구는 한쪽 회전력을 강하게 쓰는 운동! 반대쪽 밸런스를 균형 있게 채워줄 때 숨은 키와 잠재력이 함께 깨어납니다."),
            ("2만여 명 임상 경험 담은 1:1 맞춤형 코칭", "병원 도수치료실 16년 경력을 바탕으로 유도 엘리트 선수 전담 매뉴얼 코칭과 관절 안정화 및 가동성을 전문 지도합니다."),
            ("아이마다 체형이 다른데 왜 폼은 다 같을까요?", "쓰는 근육이 달라지면 선수의 능력치도 달라집니다! 몸통에 안정성이 떨어지면 아무리 세게 던져도 공에 힘이 실리지 않아요."),
            ("몸통·고관절 큰 회전에서 소근육으로 강력하게!", "팔만 휘두르면 인대가 다칩니다. 큰 움직임에서 시작해 소근육으로 부드럽게 이어져야 공에 온전히 힘을 실어줍니다."),
            ("물의 파동처럼 흘러야 예방! 근본 원인 개선", "물에 파동이 일어 잔잔해지듯 관절 충격 부하가 온몸으로 분산되어야 어깨와 팔꿈치를 안전하게 보호할 수 있어요."),
            ('"선수모집 & 특별 혜택" 조승수 × 박인국 콜라보', "초등~중1 선수모집! 조승수 감독의 전문 야구 수업과 연계하여 박인국 실장의 1:1 맞춤 케어를 첫 방문 50% 혜택(5만 원)으로 지원합니다.")
        ]
        audio_prefix = "audio/tts_video_0"

    # Step 1: Render all 6 frames
    print(f"=== Rendering frames for Vol {vol_num} ===")
    frame_files = []
    cut_durations = []
    for c in range(1, 7):
        title, desc = cuts_data[c - 1]
        if vol_num == 1:
            frame_img = render_vol1_cut(c, title, desc)
        else:
            frame_img = render_vol2_cut(c, title, desc)
        
        fpath = os.path.join(out_dir, f"frame_cut_{c}.png")
        frame_img.save(fpath, "PNG")
        frame_files.append(fpath)

        # Get audio length
        audio_path = f"{audio_prefix}{c}.mp3"
        duration = mutagen.mp3.MP3(audio_path).info.length
        cut_durations.append(duration)
        print(f"  Cut {c} frame saved: {fpath}, Audio length: {duration:.2f}s")

    # Step 2: Render each cut video segment
    segment_files = []
    for c in range(1, 7):
        fpath = frame_files[c - 1]
        audio_path = f"{audio_prefix}{c}.mp3"
        seg_mp4 = os.path.join(out_dir, f"seg_{c}.mp4")
        dur = cut_durations[c - 1] + 0.3 # 0.3s pause between cuts

        # Apply smooth zoompan
        total_frames = int(dur * 25)
        vf_filter = (
            f"scale=720:1280,"
            f"zoompan=z='min(zoom+0.0003,1.04)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=720x1280:fps=25"
        )

        cmd = [
            FFMPEG, '-y',
            '-loop', '1', '-i', fpath,
            '-i', audio_path,
            '-vf', vf_filter,
            '-c:v', 'libx264', '-preset', 'fast', '-tune', 'stillimage',
            '-c:a', 'aac', '-b:a', '192k',
            '-pix_fmt', 'yuv420p',
            '-t', str(dur),
            seg_mp4
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Error on cut {c}:", res.stderr[-300:])
            return False
        segment_files.append(seg_mp4)
        print(f"  Segment {c} rendered successfully ({dur:.2f}s)")

    # Step 3: Concat video segments
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

    # Step 4: Mix BGM with volume ducking (bgm at volume 0.11, voice at 1.0)
    bgm_path = "audio/bgm_morning.mp3"
    print("=== Mixing BGM soundtrack ===")
    cmd_final = [
        FFMPEG, '-y',
        '-i', merged_no_bgm,
        '-i', bgm_path,
        '-filter_complex', '[1:a]volume=0.11[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]',
        '-map', '0:v',
        '-map', '[aout]',
        '-c:v', 'copy',
        '-c:a', 'aac', '-b:a', '192k',
        out_mp4
    ]
    subprocess.run(cmd_final, check=True)

    size_mb = os.path.getsize(out_mp4) / (1024 * 1024)
    print(f"[SUCCESS] Generated {out_mp4} ({size_mb:.2f} MB) successfully!")
    return True

if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print("Starting Shorts MP4 Generation for Vol 2...")
    build_video_for_volume(2)
    print("ALL DONE!")
