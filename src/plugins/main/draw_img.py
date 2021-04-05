from .genshin import draw_pic
from .ys_data_parser import parse_raw_data, prase_user_info
from .db import get_user_by
from . _http import get_account_info, get_ys_info, get_abyss_info
from .download_err import get_err_pic
from nonebot.log import logger



async def process(account_info, is_login: bool):
    account_id = account_info['account_id']
    bbs_info_data = prase_user_info(await get_account_info(account_id))
    server = bbs_info_data['region']
    role_id = bbs_info_data['game_role_id']
    ys_info_data = await get_ys_info(server=server, role_id=role_id)
    ys_abyss_data = await get_abyss_info(server=server, role_id=role_id, schedule_type=2)
    data = await parse_raw_data(bbs_info_data, ys_info_data, ys_abyss_data)
    return data

async def start_draw(account_info, is_login, user_id):
    data = await process(account_info, is_login)
    if user_id:
        data['ava_type'] = 1
        data['sender_qq'] = user_id
    else:
        data['ava_type'] = 0
    try:
        im_b64 = await draw_pic(data)
    except IOError as f:
        logger.info(f'downloading{f.filename[8:16]}')
        await get_err_pic(data['info']['region'], data['info']['game_role_id'], f.filename[8:16])
        im_b64 = None
    return im_b64