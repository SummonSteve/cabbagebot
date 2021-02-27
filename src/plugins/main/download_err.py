from ._http import get_ys_info
import aiohttp
import aiofiles

async def get_err_pic(sever, game_role_id, err_char_id):
    data = await get_ys_info(sever, game_role_id)
    ava_data = data['data']['avatars']
    for avatar in ava_data:
        if str(avatar['id']) == err_char_id:
            async with aiohttp.ClientSession() as session:
                async with session.get(avatar['image']) as resp:
                    f = await aiofiles.open('./chars/{}.png'.format(err_char_id),mode='wb')
                    await f.write(await resp.read())
                    await f.close()
        else:
            pass
