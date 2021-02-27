from .db import search_user_by_role
from ._http import get_ys_finance_info


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
    except BaseException as f:
        pass

def parse_ys_info(resp_data):
    data = resp_data['data']
    return data


def parse_abyss_data(resp_data):
    data = resp_data['data']
    return data


async def parse_raw_data(bbsInfoData, ysInfoData, ysAbyssData, sender_qq: int):
    raw_data = {}
    user_info = prase_user_info(bbsInfoData)
    ys_info = parse_ys_info(ysInfoData)
    abyss_data = parse_abyss_data(ysAbyssData)
    raw_data['sender_qq'] = sender_qq
    raw_data['info'] = {}
    raw_data['info']['player_nickname'] = user_info['game_name']
    raw_data['info']['game_role_id'] = user_info['game_role_id']
    raw_data['info']['level'] = user_info['level']
    raw_data['info']['region'] = user_info['region']
    raw_data['info']['region_name'] = user_info['region_name']
    raw_data['info']['achievement_number'] = user_info['achievement']
    raw_data['info']['spiral_abyss'] = user_info['abyss_s']
    raw_data['info']['active_day_number'] = user_info['login_days']
    if user_info['login_days'] != ys_info['stats']['active_day_number']:
        raw_data['info']['active_day_number'] = ys_info['stats']['active_day_number']
    else:
        pass
    raw_data['info']['achievement_number'] = ys_info['stats']['achievement_number']
    raw_data['info']['anemoculus_number'] = ys_info['stats']['anemoculus_number']
    raw_data['info']['geoculus_number'] = ys_info['stats']['geoculus_number']
    raw_data['info']['common_chest_number'] = ys_info['stats']['common_chest_number']
    raw_data['info']['exquisite_chest_number'] = ys_info['stats']['exquisite_chest_number']
    raw_data['info']['luxurious_chest_number'] = ys_info['stats']['luxurious_chest_number']
    raw_data['info']['precious_chest_number'] = ys_info['stats']['precious_chest_number']
    raw_data['info']['spiral_abyss'] = ys_info['stats']['spiral_abyss']

    raw_data['char'] = {}
    raw_data['char'] = ys_info['avatars']
    
    db_info = search_user_by_role(user_info['game_role_id'])
    if db_info:
        raw_data['is_login'] = True
        account_id = db_info[4]
        game_role_id = db_info[1]
        region = db_info[6]
        cookie_token = db_info[5]
        financeData = await get_ys_finance_info(account_id, game_role_id, region, cookie_token)
        
        raw_data['finance'] = {}
        raw_data['finance']['data'] = {}

        raw_data['finance']['highest'] = financeData['data']['month_data']['group_by'][0]['action']
        raw_data['finance']['data'][0] = financeData['data']['month_data']['group_by'][0]['percent']
        raw_data['finance']['data'][1] = financeData['data']['month_data']['group_by'][1]['percent']
        raw_data['finance']['data'][2] = financeData['data']['month_data']['group_by'][2]['percent']
        raw_data['finance']['data'][3] = financeData['data']['month_data']['group_by'][3]['percent']
        raw_data['finance']['data'][4] = financeData['data']['month_data']['group_by'][4]['percent']
        raw_data['finance']['data'][5] = financeData['data']['month_data']['group_by'][5]['percent']
        raw_data['finance']['data'][6] = financeData['data']['month_data']['group_by'][6]['percent']
        raw_data['finance']['today_mora'] = financeData['data']["day_data"]["current_mora"]
        raw_data['finance']['today_primogems'] = financeData['data']["day_data"]["current_primogems"]
        raw_data['finance']['month_mora'] = financeData['data']["month_data"]["current_mora"]
        raw_data['finance']['month_primogems'] = financeData['data']["month_data"]["current_primogems"]


    else:
        raw_data['is_login'] = False
        raw_data['finance'] = None


    if abyss_data['total_win_times'] == 0 and len(abyss_data['floors']) == 0:
        raw_data['is_abyss'] = False
    else:
        raw_data['is_abyss'] = True
        raw_data['abyss'] = {}
        raw_data['abyss']['abyss_current_star'] = abyss_data['floors'][-1]['star']
        raw_data['abyss']['abyss_floor'] = abyss_data['floors'][-1]['index']
        raw_data['abyss']['abyss_room'] = abyss_data['floors'][-1]['levels'][-1]['index']
        raw_data['abyss']['abyss_current_time'] = abyss_data['floors'][-1]['levels'][-1]['battles'][-1]['timestamp']
        raw_data['abyss_char'] = abyss_data['floors'][-1]['levels'][-1]['battles'][-1]['avatars']


    return raw_data