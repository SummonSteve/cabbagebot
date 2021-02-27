import aiohttp
from io import BytesIO


async def get_qq_profile_pic(sender_qq):
    url = avaurl = f"http://q1.qlogo.cn/g?b=qq&nk={sender_qq}&s=640"
    async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return BytesIO(await resp.content.read())
