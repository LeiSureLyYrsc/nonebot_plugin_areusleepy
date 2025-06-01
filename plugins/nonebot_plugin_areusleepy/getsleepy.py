from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.adapters import Event as BaseEvent, Message
from nonebot import get_plugin_config, get_bot

import httpx

from nonebot_plugin_alconna.uniseg import UniMessage
from typing import Optional

from .config import Config

# 获取插件配置
plugin_config: Config = get_plugin_config(Config)

get_other_status = on_command(
    plugin_config.command,
    aliases={"获取其他Sleepy状态"}
)


async def get_status_data(custom_url: Optional[str] = None) -> Optional[tuple[bool, dict | str]]:
    url = f"{custom_url or plugin_config.sleepyurl}/query"
    retries: int = plugin_config.retries
    success = False  # 是否成功
    data = '未知错误'  # 成功: json / 错误: 错误信息
    while retries > 0:
        try:
            async with httpx.AsyncClient(timeout=plugin_config.timeout) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    success = True
                    data = response.json()
                    break
                else:
                    data = f'状态码不为 200: {response.status_code}'
        except Exception as e:
            data = f'错误信息: {e}'
        retries -= 1
    return success, data


def format_device_info(device_data: dict) -> str:
    device_lines = []
    for device_name, info in device_data.items():
        using_status = "✅ 使用中" if info.get('using', False) else "❌ 未使用"
        device_lines.append(
            f"  - {info.get('show_name', device_name)}: {using_status}\n"
            f"    应用: {info.get('app_name')}"
        )
    return "\n".join(device_lines)


async def create_status_message(data: dict, url: Optional[str] = None) -> UniMessage:
    msg = UniMessage()

    # info
    if 'info' in data and isinstance(data['info'], dict):
        info = data['info']
        display_url = url or plugin_config.sleepyurl
        msg += (
            f"👋你好 {display_url}\n"
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


@get_other_status.handle()
async def handle_get_other_status(arg_msg: Message = CommandArg()):
    """处理getsleepy命令"""
    # 获取URL参数
    url = arg_msg.extract_plain_text().strip()
    if not url:
        await get_other_status.send("请提供要查询的URL\n用法: /getsleepy url")
        return

    await get_other_status.send("正在获取状态信息，请稍候...")

    # 获取状态数据
    success, data = await get_status_data(url)

    if success:
        # 生成并发送消息
        msg = await create_status_message(data, url)
        await get_other_status.send(str(msg))
    else:
        # 如果获取数据失败，返回错误信息
        await get_other_status.send(f"获取状态信息失败: {data}")
        return
