from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from . import __main__ as __main__
from nonebot_plugin_apscheduler import scheduler
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="AreYouSleepy",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

