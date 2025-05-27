from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.adapters import Event as BaseEvent, Message
from nonebot import get_plugin_config, get_bot
from nonebot_plugin_apscheduler import scheduler

import httpx

from nonebot_plugin_alconna.uniseg import UniMessage
from typing import Optional

from .config import Config

# 获取插件配置
plugin_config = get_plugin_config(Config)

fetch_status = on_command(
    "areusleepy",
    aliases={"获取Sleepy状态"}
)

async def get_status_data() -> Optional[dict]:
    url = f"{plugin_config.sleepyurl}/query"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            if response.status_code == 200:
                return response.json()
            return None
    except Exception as e:
        return None


def format_device_info(device_data: dict) -> str:
    device_lines = []
    for device_name, info in device_data.items():
        using_status = "✅ 使用中" if info.get('using', False) else "❌ 未使用"
        device_lines.append(
            f"  - {info.get('show_name', device_name)}: {using_status}\n"
            f"    应用: {info.get('app_name')}"
        )
    return "\n".join(device_lines)

async def create_status_message(data: dict) -> UniMessage:
    msg = UniMessage()

    # info
    if 'info' in data and isinstance(data['info'], dict):
        info = data['info']
        msg += (
            f"👋你好，{plugin_config.sleepyurl}\n"
            f"🌐 个人信息:\n"
            f"  状态: {info.get('name')}\n"
            f"  {info.get('desc')}\n"
        )

    # device info
    if 'device' in data and isinstance(data['device'], dict):
        msg += "\n\n📱 设备使用情况:\n"
        msg += format_device_info(data['device'])

    # 最后更新时间
    if 'last_updated' in data:
        msg += f"\n\n⏱ 最后更新: {data['last_updated']}"
    
    return msg

@fetch_status.handle()
async def _(arg_msg: Message = CommandArg()):
    """处理queryFetch命令"""
    await fetch_status.send("正在获取状态信息，请稍候...")

    # 获取状态数据
    data = await get_status_data()
    
    # 如果获取数据失败，返回错误信息
    if data is None:
        await fetch_status.send("获取状态信息失败，请稍后重试")
        return

    # 生成并发送消息
    msg = await create_status_message(data)
    await fetch_status.send(str(msg))
