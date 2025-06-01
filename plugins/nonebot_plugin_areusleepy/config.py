from pydantic import BaseModel


class Config(BaseModel):
    command_areusleepy: str = 'areusleepy' # areusleepy 功能触发命令
    sleepyurl: str # areusleepy 功能的
    sleepygroup: list[str] = ['']
    schedule_enable: bool = False  # 定时任务开关，默认关闭
    schedule_hour: str = '0'  # 定时任务执行的小时，默认每小时执行一次
    timeout: float = 5.0  # 请求超时 (秒)
    retries: int = 3  # 请求失败时的重试次数
