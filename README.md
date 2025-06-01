# Are U Sleepy???

用来~~视剑~~查看在线状态的 NoneBot 插件

## 安装

```sh
pip install pdm
pdm install
```

## 配置

将 `.env.example` 重命名 / 复制为 `.env.prod`, 按照说明修改配置即可

## 启动

```sh
nb run
```

使用: `/sleepy` (`sleepy 为你配置的触发命令`)

或 `/sleepy [服务地址]`

> [!IMPORTANT]
> 服务地址必须以 `http://` 或 `https:// 开头` <br/>
> 如未指定服务地址则使用配置中的 `sleepy_url`

## 关于

[作者的视剑网站](https://status.0d000721.xin)

[Sleepy 服务](https://github.com/sleepy-project/sleepy)
