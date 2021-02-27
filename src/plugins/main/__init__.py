from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.adapters.cqhttp import MessageSegment
from nonebot.rule import to_me
from nonebot.log import logger
from ._http import get_ys_info, get_account_info, get_abyss_info, post_bbsReward
from .genshin import draw_pic
from .db import search_user_by_qq
from .ys_data_parser import parse_raw_data, prase_user_info
from .download_err import get_err_pic


genshin = on_command("stat", rule=None, priority=3, aliases=set(['statme']))
genshinReward = on_command("签到", rule=to_me(), priority=5)
Genshinsign = on_command("绑定", rule=to_me(), priority=7, aliases=set(['sign']))
GenshinChars = on_command("avainfo", rule=to_me(), priority=7)


async def try_draw_img(rawData):
    try:
        im_b64 = await draw_pic(rawData)
    except IOError as f:
        print(f.filename[8:16])
        await get_err_pic(rawData['info']['region'], rawData['info']['game_role_id'], f.filename[8:16])
        await genshin.finish('素材文件缺失，已加入下载队列，请稍后重新使用命令')
        im_b64 = None
    return im_b64




@genshin.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    try:
        args = str(event.message).strip()
        if args:
            state['account_id'] = args
            bbsInfoData = await get_account_info(state['account_id'])
            bbsInfo = prase_user_info(bbsInfoData)
            try:
                state['region'] = bbsInfo['region']
                state['game_role_id'] = bbsInfo['game_role_id']
            except TypeError:
                await genshin.finish('没这个人')
            ysInfoData = await get_ys_info(state['region'], state['game_role_id'])
            ysAbyssData = await get_abyss_info(state['region'], state['game_role_id'], 2)
            rawData = await parse_raw_data(bbsInfoData, ysInfoData, ysAbyssData, event.sender['user_id'])
            rawData['ava_flag'] = 0
            im_b64 = await try_draw_img(rawData)
            pic_message = MessageSegment.image(f'base64://{im_b64}')
            await genshin.finish(pic_message)
        else:

            user_data = search_user_by_qq(event.sender['user_id'])
            if user_data:
                state['user_id'] = str(event.sender['user_id'])
                state['game_role_id'] = str(user_data[1])
                state['game_name'] = user_data[0]
                state['user_name'] = user_data[3]
                state['account_id'] = str(user_data[4])
                state['cookie_token'] = user_data[5]
                state['region'] = user_data[6]
                state['is_login'] = True

                await bot.send(event,f'已绑定用户：{state["game_name"]}\n米游社ID:{state["account_id"]}')
                bbsInfoData = await get_account_info(state['account_id'])
                ysInfoData = await get_ys_info(state['region'], state['game_role_id'])
                ysAbyssData = await get_abyss_info(state['region'], state['game_role_id'], 2)
                rawData = await parse_raw_data(bbsInfoData, ysInfoData, ysAbyssData, event.sender['user_id'])
                rawData['ava_flag'] = 1
                im_b64 = await try_draw_img(rawData)
                pic_message = MessageSegment.image(f'base64://{im_b64}')

                await genshin.finish(pic_message)
            else:
                logger.info('no such user in db')
    except TypeError as f:
        await genshin.finish(f'fatal error msg:{f.with_traceback} 如检查命令参数无误请将这个错误反馈给开发者')


@genshin.got("account_id", prompt='未绑定\n请输入米游社ID')
async def handle_unlogin(bot: Bot, event: Event, state: dict):
    try:
        bbsInfoData = await get_account_info(state['account_id'])
        bbsInfo = prase_user_info(bbsInfoData)
        state['region'] = bbsInfo['region']
        state['game_role_id'] = bbsInfo['game_role_id']
        ysInfoData = await get_ys_info(state['region'], state['game_role_id'])
        ysAbyssData = await get_abyss_info(state['region'], state['game_role_id'], 2)
        rawData = await parse_raw_data(bbsInfoData, ysInfoData, ysAbyssData, event.sender['user_id'])
        rawData['ava_flag'] = 1
        im_b64 = await try_draw_img(rawData)
        pic_message = MessageSegment.image(f'base64://{im_b64}')
    except BaseException as f:
        pic_message = None
        await genshin.finish(f'fatal error msg:{f} 如检查命令参数无误请将这个错误反馈给开发者')
    await genshin.finish(pic_message)

@genshinReward.handle()
async def handle_reward(bot: Bot, event: Event, state: dict):
    user_data = search_user_by_qq(event.sender['user_id'])
    if user_data:
        info = await post_bbsReward(user_data[4], user_data[1], user_data[6], user_data[5])
        info = (f'游戏昵称: {user_data[0]}\n状态消息：' + info["message"])
    else:
        info = '未绑定'

    await genshinReward.finish(info)

@GenshinChars.handle()
async def handle_char_info(bot: Bot, event: Event, state: dict):
    pass