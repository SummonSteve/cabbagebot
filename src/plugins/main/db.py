import nonebot
import traceback

export = nonebot.require("nonebot_plugin_navicat") 
connection = export.sqlite_pool


async def create_table(game_role_id: str):
    try:
        await connection.execute("CREATE TABLE user_cookie(game_name TEXT,game_id INTEGER ,user_id INTEGER,user_name TEXT,account_id INTEGER,cookie_token TEXT, region TEXT)")
        return True
    except Exception:
        return False


async def get_user_by(para, value):
    try:
        data =  await connection.fetch_one(f"SELECT * from user_cookie WHERE {para} = {value}")
        user_dict = {}
        user_dict['game_name'] = data[0]
        user_dict['game_id'] = data[1]
        user_dict['user_id'] = data[2]
        user_dict['user_name'] = data[3]
        user_dict['account_id'] = data[4]
        user_dict['cookie_token'] = data[5]
        user_dict['region'] = data[6]
        return user_dict
    except Exception:
        print(traceback.format_exc())
        return False


async def add_user(data):
    #data may like ('Neko', 107705948, 1824272506, 'Saya', 71230697, 'Lf0wrCOIug2QErcnozKZ1RVLaotbChUaoc4q7QuB', 'cn_gf01')
    await connection.execute(f"INSERT INTO user_cookie (game_name, game_id, user_id, user_name, account_id, cookie_token, region) VALUES {data}")