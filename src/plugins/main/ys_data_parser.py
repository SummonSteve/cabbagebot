from .db import get_user_by
from ._http import get_ys_finance_info
from nonebot.log import logger


def prase_user_info(resp_data):
    data = resp_data['data']['list']
    try:
        for k in data:
            if k['game_id'] == 2:
                resp_data = {}
                resp_data['game_role_id'] = k['game_role_id']
                resp_data['game_name'] = k['nickname']
                resp_data['region'] = k['region']
                resp_data['region_name'] = k['region_name']
                resp_data['level'] = k['level']
                resp_data['login_days'] = k['data'][0]['value']
                resp_data['char_num'] = k['data'][1]['value']
                resp_data['achievement'] = k['data'][2]['value']
                resp_data['abyss_s'] = k['data'][3]['value']
                return resp_data
    except KeyError:
        logger.log('no genshin character')


async def parse_raw_data(bbs_info_data, ys_info_data, ys_abyss_data):
    data_pack = {}
    user_info = bbs_info_data
    ys_info = ys_info_data['data']
    abyss_data = ys_abyss_data['data']
    data_pack['info'] = {}
    data_pack['info']['player_nickname'] = user_info['game_name']
    data_pack['info']['game_role_id'] = user_info['game_role_id']
    data_pack['info']['level'] = user_info['level']
    data_pack['info']['region'] = user_info['region']
    data_pack['info']['region_name'] = user_info['region_name']
    data_pack['info']['achievement_number'] = user_info['achievement']
    data_pack['info']['spiral_abyss'] = user_info['abyss_s']
    data_pack['info']['active_day_number'] = user_info['login_days']
    data_pack['info']['achievement_number'] = ys_info['stats']['achievement_number']
    data_pack['info']['anemoculus_number'] = ys_info['stats']['anemoculus_number']
    data_pack['info']['geoculus_number'] = ys_info['stats']['geoculus_number']
    data_pack['info']['common_chest_number'] = ys_info['stats']['common_chest_number']
    data_pack['info']['exquisite_chest_number'] = ys_info['stats']['exquisite_chest_number']
    data_pack['info']['luxurious_chest_number'] = ys_info['stats']['luxurious_chest_number']
    data_pack['info']['precious_chest_number'] = ys_info['stats']['precious_chest_number']
    data_pack['info']['spiral_abyss'] = ys_info['stats']['spiral_abyss']

    data_pack['char'] = {}
    data_pack['char'] = ys_info['avatars']
    db_info = await get_user_by('game_id', user_info['game_role_id'])
    if db_info['cookie_token'] != '':
        data_pack['is_login'] = True
        account_id = db_info['account_id']
        game_role_id = db_info['game_id']
        region = db_info['region']
        cookie_token = db_info['cookie_token']
        finance_data = await get_ys_finance_info(account_id, game_role_id, region, cookie_token)
        data_pack['finance'] = {}
        data_pack['finance']['data'] = {}
        data_pack['finance']['highest'] = finance_data['data']['month_data']['group_by'][0]['action']
        data_pack['finance']['data'][0] = finance_data['data']['month_data']['group_by'][0]['percent']
        data_pack['finance']['data'][1] = finance_data['data']['month_data']['group_by'][1]['percent']
        data_pack['finance']['data'][2] = finance_data['data']['month_data']['group_by'][2]['percent']
        data_pack['finance']['data'][3] = finance_data['data']['month_data']['group_by'][3]['percent']
        data_pack['finance']['data'][4] = finance_data['data']['month_data']['group_by'][4]['percent']
        data_pack['finance']['data'][5] = finance_data['data']['month_data']['group_by'][5]['percent']
        data_pack['finance']['data'][6] = finance_data['data']['month_data']['group_by'][6]['percent']
        data_pack['finance']['today_mora'] = finance_data['data']["day_data"]["current_mora"]
        data_pack['finance']['today_primogems'] = finance_data['data']["day_data"]["current_primogems"]
        data_pack['finance']['month_mora'] = finance_data['data']["month_data"]["current_mora"]
        data_pack['finance']['month_primogems'] = finance_data['data']["month_data"]["current_primogems"]
    else:
        data_pack['is_login'] = False
        data_pack['finance'] = None


    if abyss_data['total_win_times'] == 0 and len(abyss_data['floors']) == 0:
    #判断有没有参与深渊
        data_pack['is_abyss'] = False
    else:
        data_pack['is_abyss'] = True
        data_pack['abyss'] = {}
        data_pack['abyss']['abyss_current_star'] = abyss_data['floors'][-1]['star']
        data_pack['abyss']['abyss_floor'] = abyss_data['floors'][-1]['index']
        data_pack['abyss']['abyss_room'] = abyss_data['floors'][-1]['levels'][-1]['index']
        data_pack['abyss']['abyss_current_time'] = abyss_data['floors'][-1]['levels'][-1]['battles'][-1]['timestamp']
        data_pack['abyss_char'] = abyss_data['floors'][-1]['levels'][-1]['battles'][-1]['avatars']


    return data_pack