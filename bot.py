import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)

config = driver.config
nonebot.load_builtin_plugins()
nonebot.load_plugin('nonebot_plugin_navicat')
nonebot.load_plugins("src/plugins")

if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")