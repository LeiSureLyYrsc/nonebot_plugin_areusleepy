from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from . import __main__ as __main__

from .config import Config

__plugin_meta__ = PluginMetadata(
    name='AreYouSleepy',
    description='基于 Sleepy 的在线状态查询插件',
    usage='/sleepy [服务地址]',
    homepage='https://github.com/Murasame-Dev/nonebot_areusleepy',
    config=Config,
)

config = get_plugin_config(Config)
