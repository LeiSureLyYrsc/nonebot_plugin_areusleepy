# coding: utf-8

# --- 导入模块

from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.adapters import Event as BaseEvent, Message
from nonebot import get_plugin_config, get_bot
from nonebot_plugin_alconna.uniseg import UniMessage

import requests
from urllib.parse import urljoin

from .config import Config

# --- 获取配置

config: Config = get_plugin_config(Config)

# --- 处理函数


def get_data(base_url: str, retries: int = config.sleepy_retries) -> tuple[bool, (dict | str)]:
    '''
    请求 api 获取数据

    :param base_url: 服务地址
    :param retries: 重试次数
    :return bool: 是否成功
    :return dict | str: 返回数据 (如成功则为返回数据 (dict), 如失败则为错误信息 (str))
    '''
    success = False
    data = '未知错误'
    while retries > 0:
        try:
            query_url = urljoin(base_url, '/query?version=1')  # version=1 -> 为未来 (可能) 的 Sleepy /query API 修改提供兼容
            resp: requests.Response = requests.get(
                url=query_url,
                timeout=config.sleepy_timeout,
                allow_redirects=True
            )
            data = resp.json()
            success = True
            break
        except Exception as e:
            data = f'请求 {query_url} 出错: {e}'
            retries -= 1
    return success, data


def slice_text(text: str, max_length: int) -> str:
    '''
    截取指定长度文本

    :param text: 原文本
    :param max_length: 最大长度

    :return str: 处理后文本
    '''
    if (
        len(text) <= max_length or  # 文本长度小于指定截取长度
        max_length == 0  # 截取长度设置为 0 (禁用)
    ):
        return text
    else:
        return f'{text[:max_length-3]}...'


def parse_data(url: str, data: dict) -> str:
    '''
    处理返回的数据

    :param url: 网站地址
    :param data: /query 返回数据
    :return str: 处理后的消息文本
    '''
    devices = []
    n = '\n'
    if data.get('device'):
        raw_devices: dict = data.get('device')
        status_slice: int = data.get('device_status_slice')
        for i in raw_devices.keys():
            device: dict = raw_devices[i]
            devices.append(f'''
 - {device['show_name']}{f" ({i})" if config.sleepy_show_details else ""}
   * 状态: {"✅" if device['using'] else "❌"}
   * 应用: {slice_text(device['app_name'], status_slice)}
'''[1:-1])
    ret = f'''
🌐 网站: {url}

👀 在线状态
状态: {data['info']['name']}{f" ({data['status']})" if config.sleepy_show_details else ""}
详细信息: {data['info']['desc']}

📱 设备状态
{n.join(devices) if devices else '无'}

⏱ 最后更新: {data['last_updated']}{f" ({data['timezone']})" if config.sleepy_show_details else ""}
'''[1:-1]
    return ret

# --- 定义命令


ctx = on_command(
    cmd=config.sleepy_command
)


@ctx.handle()
async def handle_status(msg: Message = CommandArg()):
    '''
    处理 /sleepy (默认) 命令
    '''
    # 获取参数
    query_url = msg.extract_plain_text().strip() or config.sleepy_url

    # 提示获取中
    if config.sleepy_prompt_loading:
        await ctx.send(f'正在从 {query_url} 获取状态, 请稍候...')

    success, data = get_data(query_url)
    if success:
        # 成功 -> 处理数据
        try:
            parsed = parse_data(query_url, data)
        except Exception as e:
            parsed = f'处理状态信息失败: {e}'
        await ctx.send(parsed)
    else:
        # 失败 -> 返回错误
        await ctx.send(f'获取状态信息失败: {data}')
