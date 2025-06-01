from pydantic import BaseModel


class Config(BaseModel):
    # 基本配置
    sleepy_command: str = 'sleepy'  # 触发命令
    sleepy_prompt_loading: bool = True  # 是否提示获取中
    sleepy_show_details: bool = False  # 是否显示详细信息

    # Sleepy 服务配置
    sleepy_url: str = 'https://sleepy-preview.wyf9.top'  # Sleepy 服务地址
    sleepy_timeout: float = 5.0  # 请求超时 (秒)
    sleepy_retries: int = 3  # 请求失败时的重试次数
