from typing import Dict
import aiohttp
import json
from .mhy_http_header import get_header

base_url = 'https://api-takumi.mihoyo.com'


async def get_account_info(account_id: str):
    url = base_url + f'/game_record/card/wapi/getGameRecordCard?uid={account_id}'
    header = get_header(account_id, False, "2.3.0")
    async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=header) as resp:
                return json.loads(await resp.text())


async def get_ys_info(server: str, role_id: str):
    account_id = None
    url = base_url + f'/game_record/genshin/api/index?server={server}&role_id={role_id}'
    header = get_header(account_id, False, "2.3.0")
    async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=header) as resp:
                return json.loads(await resp.text())


async def get_abyss_info(server: str, role_id: str, schedule_type: int):
    account_id = None
    url = base_url + f'/game_record/genshin/api/spiralAbyss?server={server}&role_id={role_id}&schedule_type={schedule_type}'
    header = get_header(account_id, False, "2.3.0")
    async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=header) as resp:
                return json.loads(await resp.text())


async def post_bbsReward(account_id: str, game_role_id: str, region: str, cookie_token: str):
    url = base_url + '/event/bbs_sign_reward/sign'
    header = get_header(account_id, cookie_token, "2.3.0")
    postContent = '{{"act_id": "e202009291139501","region": "{}","uid": "{}"}}'.format(region, game_role_id)
    data = json.loads(postContent)
    async with aiohttp.ClientSession()as session:
        async with session.post(url, json=data, headers=header) as resp:
            return json.loads(await resp.text())


async def get_ys_finance_info(account_id, game_role_id, region, cookie_token):
    url = f'https://hk4e-api.mihoyo.com/event/ys_ledger/monthInfo?month=0&bind_uid={game_role_id}&bind_region={region}&bbs_presentation_style=fullscreen&bbs_auth_required=true&utm_source=icon&utm_medium=ys&utm_campaign=GameRecord'
    header = get_header(account_id, cookie_token, "2.3.0")
    async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=header) as resp:
                return json.loads(await resp.text())