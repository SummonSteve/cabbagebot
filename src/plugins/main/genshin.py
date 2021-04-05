from PIL import Image, ImageDraw, ImageFont, ImageFilter
import matplotlib.pyplot as plt
import time
from io import BytesIO
from base64 import b64encode
from .avatar import get_qq_profile_pic

def circle_corner(radimg, radii):
        circle = Image.new('L', (radii * 2, radii * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)

        radimg = radimg.convert("RGBA")
        w, h = radimg.size

        alpha = Image.new('L', radimg.size, 255)
        alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))
        alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))
        alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))
        alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))

        radimg.putalpha(alpha)
        return radimg

def ys_font(size):
    return ImageFont.truetype("yuanshen.ttf", size=size, encoding="utf-8")



async def draw_pic(raw_data):
    bg_path = './texture2d/bg_1.jpg'

    char1_id = raw_data['char'][0]['id']
    char2_id = raw_data['char'][1]['id']
    char3_id = raw_data['char'][2]['id']
    char4_id = raw_data['char'][3]['id']
    char5_id = raw_data['char'][4]['id']
    char6_id = raw_data['char'][5]['id']

    char1 = f'./chars/{char1_id}.png'
    char2 = f'./chars/{char2_id}.png'
    char3 = f'./chars/{char3_id}.png'
    char4 = f'./chars/{char4_id}.png'
    char5 = f'./chars/{char5_id}.png'
    char6 = f'./chars/{char6_id}.png'

    img = Image.open(bg_path)
    im_blur = img.filter(ImageFilter.GaussianBlur)
    base_img = Image.new("RGB", img.size, (255, 255, 255))
    canvas_img = Image.new("RGB", (int(img.size[0] * 0.95), int(img.size[1] * 0.98)), "black")
    paste_box_x = base_img.size[0] - canvas_img.size[0]
    paste_box_y = base_img.size[1] - canvas_img.size[1]
    paste_box = (int(paste_box_x / 2), int(paste_box_y / 2))
    base_img.paste(canvas_img, paste_box)
    img_canvas = Image.blend(im_blur, base_img, 0.2)

    text_draw = ImageDraw.Draw(img_canvas)

    if raw_data['ava_type'] == 1:
        ava_img = Image.open(await get_qq_profile_pic(raw_data['sender_qq'])).resize((127, 127), Image.BILINEAR)
    else:
        ava_img = Image.open('./texture2d/default_ava.png').resize((127, 127), Image.BILINEAR)

    ava_holder = Image.open('./texture2d/ba.png').resize((200, 200), Image.BILINEAR)
    id_img = Image.open("./texture2d/level.png").resize((250, 155), Image.BILINEAR).convert("RGBA")
    level_img = Image.open("./texture2d/level2.png").resize((180, 180), Image.BILINEAR).convert("RGBA")
    p1_img = Image.open("./texture2d/p1.png").resize((600, 300), Image.BILINEAR).convert("RGBA")
    emoji = Image.open('./texture2d/UI_EmotionIcon5.png')
    bar = Image.open("./texture2d/bar.png").convert("RGBA").resize((580, 40), Image.BILINEAR)
    wind_img = Image.open("./texture2d/wind.png").convert("RGBA")
    earth_img = Image.open("./texture2d/earth.png").convert("RGBA")
    
    char1_img = Image.open(char1).convert("RGBA").resize((95, 95), Image.BILINEAR)
    char2_img = Image.open(char2).convert("RGBA").resize((95, 95), Image.BILINEAR)
    char3_img = Image.open(char3).convert("RGBA").resize((95, 95), Image.BILINEAR)
    char4_img = Image.open(char4).convert("RGBA").resize((95, 95), Image.BILINEAR)
    char5_img = Image.open(char5).convert("RGBA").resize((95, 95), Image.BILINEAR)
    char6_img = Image.open(char6).convert("RGBA").resize((95, 95), Image.BILINEAR)


    cover_img = Image.open("./texture2d/cover.png").convert("RGBA").resize((105, 105), Image.BILINEAR)
    ava_rad = circle_corner(ava_img, 15)
    primogems_img = Image.open("./texture2d/h.png").convert("RGBA").resize((50, 50), Image.BILINEAR)
    mora_img = Image.open("./texture2d/l.png").convert("RGBA").resize((50, 50), Image.BILINEAR)
    cover_bg = Image.open("./texture2d/wlevel.png").convert("RGBA").resize((200, 120), Image.BILINEAR).convert("RGBA")
    luoxuan_bg = Image.open("./texture2d/luoxuan.png").convert("RGBA").resize((345, 140), Image.BILINEAR).convert("RGBA")
    staron = Image.open("./texture2d/staron.png").convert("RGBA").resize((50, 50), Image.BILINEAR).convert("RGBA")
    luoxuan_bg = circle_corner(luoxuan_bg, 15)
    img_canvas.paste(ava_holder, (15, 20), ava_holder)
    img_canvas.paste(ava_rad, (50, 55), ava_rad)
    img_canvas.paste(id_img, (210, 45), id_img)
    img_canvas.paste(level_img, (465, 30), level_img)
    img_canvas.paste(p1_img, (41, 230), p1_img)
    img_canvas.paste(bar, (45, 480), bar)
    img_canvas.paste(wind_img, (308, 240), wind_img)
    img_canvas.paste(earth_img, (480, 245), earth_img)
    img_canvas.paste(char1_img, (40, 560), char1_img)
    img_canvas.paste(char2_img, (140, 560), char2_img)
    img_canvas.paste(char3_img, (240, 560), char3_img)
    img_canvas.paste(char4_img, (340, 560), char4_img)
    img_canvas.paste(char5_img, (440, 560), char5_img)
    img_canvas.paste(char6_img, (540, 560), char6_img)
    
    if raw_data['is_login']:

        sizes = [0, 0, 0, 0, 0, 0, 0]
        highest = 'None'
        try:
            highest = raw_data['finance']['highest']
            d1 = raw_data['finance']['data'][0]
            d2 = raw_data['finance']['data'][1]
            d3 = raw_data['finance']['data'][2]
            d4 = raw_data['finance']['data'][3]
            d5 = raw_data['finance']['data'][4]
            d6 = raw_data['finance']['data'][5]
            d7 = raw_data['finance']['data'][6]
            sizes = [d1, d2, d3, d4, d5, d6, d7]
        except BaseException:
            pass

        x_0 = [1, 0, 0, 0, 0, 0, 0]
        colors = ['hotpink', 'slateblue', 'goldenrod', 'olivedrab', 'lightcyan', 'limegreen']
        plt.pie(sizes, shadow=False, colors=colors, startangle=150)
        plt.pie(x_0, radius=0.6, colors='w')
        f1 = plt.axis('equal')
        buffer = BytesIO()
        plt.savefig(buffer, bbox_inches=0, transparent=True, format='png')
        stat_img = Image.open(buffer).convert("RGBA").resize((250, 180), Image.BILINEAR)

        img_canvas.paste(stat_img, (420, 720), stat_img)
        img_canvas.paste(cover_img, (496, 758), cover_img)
        img_canvas.paste(cover_bg, (50, 750), cover_bg)
        img_canvas.paste(cover_bg, (260, 750), cover_bg)
        img_canvas.paste(primogems_img, (60, 755), primogems_img)
        img_canvas.paste(mora_img, (270, 755), mora_img)

        text_draw.text((520, 795), f'占比最高\n{highest}', 'black', ys_font(15))
        text_draw.text((110, 760), f"今日获得原石\n{str(raw_data['finance']['today_primogems'])}", 'black', ys_font(20))
        text_draw.text((110, 810), f"当月获得原石\n{str(raw_data['finance']['month_primogems'])}", 'black', ys_font(20))
        text_draw.text((320, 760), f"今日获得摩拉\n{str(raw_data['finance']['today_mora'])}", 'black', ys_font(20))
        text_draw.text((320, 810), f"当月获得摩拉\n{str(raw_data['finance']['month_mora'])}", 'black', ys_font(20))
    else:
        text_draw.text((140, 800), '未绑定账号信息，追踪暂不可用', 'black', ys_font(30))


    img_canvas.paste(luoxuan_bg, (50, 880), luoxuan_bg)
    if raw_data['is_abyss']:
        img_canvas.paste(staron, (270, 885), staron)
        abyss_char1_id = raw_data['abyss_char'][0]['id']
        abyss_char2_id = raw_data['abyss_char'][1]['id']
        abyss_char3_id = raw_data['abyss_char'][2]['id']
        abyss_char4_id = raw_data['abyss_char'][3]['id']
        abyss_char1 = f'./chars/{abyss_char1_id}.png'
        abyss_char2 = f'./chars/{abyss_char2_id}.png'
        abyss_char3 = f'./chars/{abyss_char3_id}.png'
        abyss_char4 = f'./chars/{abyss_char4_id}.png'
        abyss_char1_img = Image.open(abyss_char1).convert("RGBA").resize((70, 70), Image.BILINEAR)
        abyss_char2_img = Image.open(abyss_char2).convert("RGBA").resize((70, 70), Image.BILINEAR)
        abyss_char3_img = Image.open(abyss_char3).convert("RGBA").resize((70, 70), Image.BILINEAR)
        abyss_char4_img = Image.open(abyss_char4).convert("RGBA").resize((70, 70), Image.BILINEAR)
        img_canvas.paste(abyss_char1_img, (60, 945), abyss_char1_img)
        img_canvas.paste(abyss_char2_img, (130, 945), abyss_char2_img)
        img_canvas.paste(abyss_char3_img, (200, 945), abyss_char3_img)
        img_canvas.paste(abyss_char4_img, (270, 945), abyss_char4_img)

        abyss_floor = raw_data['abyss']['abyss_floor']
        abyss_current_star = raw_data['abyss']['abyss_current_star']
        abyss_room = raw_data['abyss']['abyss_room']
        abyss_current_timeStamp = raw_data['abyss']['abyss_current_time']
        timeArray = time.localtime(int(abyss_current_timeStamp))
        abyss_current_time = time.strftime("%Y.%m.%d %H:%M:%S", timeArray)


        text_draw.text((60, 890), f'深境螺旋第{abyss_floor}层', 'lightcyan', ys_font(25))
        text_draw.text((320, 895), f'{abyss_current_star}/9', 'lightcyan', ys_font(25))
        text_draw.text((60, 920), f'第{abyss_room}间 ' + abyss_current_time, 'lightcyan', ys_font(15))
    else:
        text_draw.text((115, 930), '未参与深境螺旋', 'lightcyan', ys_font(30))


    img_canvas.paste(emoji, (400, 870), emoji)

    level = raw_data['info']['level']
    if level <= 20:
        w_level = 1
    else:
        w_level = int((level - 20) / 5) + 1

    text_draw.text((240, 80), raw_data['info']['player_nickname'], 'lightcyan', ys_font(23))
    text_draw.text((240, 120), 'ID ' + str(raw_data['info']['game_role_id']), 'limegreen', ys_font(18))
    text_draw.text((240, 150), '服务器 ' + raw_data['info']['region_name'], 'lightcyan', ys_font(18))
    text_draw.text((520, 90), f'{str(level)}级', (0, 0, 0), ys_font(30))
    text_draw.text((510, 125), f'世界等级 {w_level}', (0, 0, 0), ys_font(18))

    wind_num = raw_data['info']['anemoculus_number']
    earth_num = raw_data['info']['geoculus_number']

    char_data = raw_data["char"]

    text_draw.text((80, 245), '活跃天数   ' + str(raw_data['info']['active_day_number']), (0, 0, 0), ys_font(23))
    text_draw.text((80, 285), '成就解锁   ' + str(raw_data['info']['achievement_number']), (0, 0, 0), ys_font(23))
    text_draw.text((80, 325), '华丽宝箱   ' + str(raw_data['info']['luxurious_chest_number']), (0, 0, 0), ys_font(23))
    text_draw.text((80, 365), '珍贵宝箱   ' + str(raw_data['info']['precious_chest_number']), (0, 0, 0), ys_font(23))
    text_draw.text((80, 405), '精致宝箱   ' + str(raw_data['info']['exquisite_chest_number']), (0, 0, 0), ys_font(23))
    text_draw.text((80, 445), '普通宝箱   ' + str(raw_data['info']['common_chest_number']), (0, 0, 0), ys_font(23))
    text_draw.text((250, 485), '深境螺旋  ' + raw_data['info']['spiral_abyss'], 'lightcyan', ys_font(25))
    text_draw.text((320, 365), f'风神瞳\n{wind_num}/66', (0, 0, 0), ys_font(27))
    text_draw.text((490, 365), f'岩神瞳\n{earth_num}/131', (0, 0, 0), ys_font(27))
    text_draw.text((60, 680), f'{char_data[0]["name"]}\nLv.{str(char_data[0]["level"])}\n好感等级{str(char_data[0]["fetter"])}', 'lightcyan', ys_font(17))
    text_draw.text((156, 680), f'{char_data[1]["name"]}\nLv.{str(char_data[1]["level"])}\n好感等级{str(char_data[1]["fetter"])}', 'lightcyan', ys_font(17))
    text_draw.text((254, 680), f'{char_data[2]["name"]}\nLv.{str(char_data[2]["level"])}\n好感等级{str(char_data[2]["fetter"])}', 'lightcyan', ys_font(17))
    text_draw.text((352, 680), f'{char_data[3]["name"]}\nLv.{str(char_data[3]["level"])}\n好感等级{str(char_data[3]["fetter"])}', 'lightcyan', ys_font(17))
    text_draw.text((450, 680), f'{char_data[4]["name"]}\nLv.{str(char_data[4]["level"])}\n好感等级{str(char_data[4]["fetter"])}', 'lightcyan', ys_font(17))
    text_draw.text((548, 680), f'{char_data[5]["name"]}\nLv.{str(char_data[5]["level"])}\n好感等级{str(char_data[5]["fetter"])}', 'lightcyan', ys_font(17))
    text_draw.text((55, 1040), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' by CabbageBot', 'black', ys_font(18))


    result_buffer = BytesIO()
    img_canvas.save(result_buffer, format='png')

    return b64encode(result_buffer.getvalue()).decode()



async def draw_char_info():
    pass