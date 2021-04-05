import nonebot
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.adapters.cqhttp import MessageSegment
from nonebot.rule import to_me
from nonebot.log import logger
from .db import get_user_by, add_user, create_table
from sqlite3 import OperationalError
from ._http import get_account_info
from .ys_data_parser import prase_user_info
from .draw_img import start_draw


driver: nonebot.Driver = nonebot.get_driver()
config: nonebot.config.Config = nonebot.get_driver().config


@driver.on_startup
async def check_db():
    db_type = config.genshindb
    if db_type == 'sqlite' or db_type == 'mysql':
        try:
            await get_user_by("account_id", config.genshin_account)
            logger.info(f'started genshin plugin with account {config.genshin_account}')
        except OperationalError:
            await create_table()


genshin_stat = on_command("asdf", rule=None, priority=3, block=True)


@genshin_stat.handle()
async def handle_all(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    sender = event.sender.user_id
    self_user = await get_user_by("user_id", sender)

    if args and args != 'me':
        if 'CQ:at' in args:
            at_user_id = str.split(str.split(args, 'qq=')[1], ']')[0]
            at_user_info = await get_user_by("user_id", at_user_id)
            if at_user_info:
                if at_user_info['cookie_token'] != '':
                    is_login = True
                else:
                    is_login = False
                im_b64 =  await start_draw(at_user_info, is_login, user_id=at_user_id)
                pic_message = MessageSegment.image(f'base64://{im_b64}')
                await genshin_stat.finish(pic_message)
            else:
                await genshin_stat.finish('查询用户未绑定')
        else:
            stat_user_info = await get_user_by("account_id", args)
            if not stat_user_info:
                account_info = prase_user_info(await get_account_info(args))
                db_data = (account_info['game_name'], 
                            account_info['game_role_id'], 
                            sender,
                            event.sender.nickname,
                            args,
                            '', 
                            account_info['region'])
                await add_user(db_data)
            else:
                if stat_user_info['cookie_token'] != '':
                    is_login = True
                else:
                    is_login = False
                im_b64 =  await start_draw(stat_user_info, is_login, user_id=sender)
                pic_message = MessageSegment.image(f'base64://{im_b64}')
                await genshin_stat.finish(pic_message)

    elif args == 'me':
        stat_user_info = await get_user_by("user_id", sender)
        if stat_user_info:
            if stat_user_info['cookie_token'] != '':
                is_login = True
            else:
                is_login = False
            im_b64 =  await start_draw(stat_user_info, is_login, user_id=sender)
            pic_message = MessageSegment.image(f'base64://{im_b64}')
            await genshin_stat.finish(pic_message)
        else:
            await genshin_stat.finish('未绑定，请使用/stat <id>')


    else:
        await genshin_stat.finish('缺少参数\n米游社ID或已绑定用户')