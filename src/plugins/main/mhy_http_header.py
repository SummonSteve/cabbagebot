import hashlib
import time
import random
import string
import uuid
import nonebot

config: nonebot.config.Config = nonebot.get_driver().config

cookie_token = config.bot_genshin_cookie
bot_cookie = f'account_id={config.genshin_account};cookie_token={cookie_token}'

def md5(text):
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()


def get_ds(mhyVersion):
    if (mhyVersion == "2.1.0"):
        n = md5(mhyVersion)
    elif (mhyVersion == "2.3.0"):
        n = "h8w582wxwgqvahcdkpvdhbh2w9casgfl"
    else:
        mhyVersion = "2.4.0"
        n = "pbcfcvnfsm5s2w4x3lsq8caor7v8nlqm"
    i = str(int(time.time()))
    r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
    c = md5(f"salt={n}&t={i}&r={r}")
    return f"{i},{r},{c}"


def get_header(account_id, user_cookie_token, mhyVersion):
    header = {
        'Accept': 'application/json, text/plain, */*',
        'DS': get_ds(mhyVersion),
        'Origin': 'https://webstatic.mihoyo.com',
        'x-rpc-app_version': mhyVersion,
        'User-Agent': f'Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 miHoYoBBS/{mhyVersion}',
        'x-rpc-client_type': '5',
        'Referer': 'https://webstatic.mihoyo.com/app/community-game-records/index.html?v=6',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.mihoyo.hyperion',
        'cookie': bot_cookie
    }

    if user_cookie_token:
        header['cookie'] = f'account_id={account_id};cookie_token={user_cookie_token}'
        header['x-rpc-device_id'] = str(uuid.uuid3(uuid.NAMESPACE_URL, user_cookie_token))
    else:
        pass
    return header

