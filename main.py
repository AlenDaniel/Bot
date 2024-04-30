import asyncio, os
from src.core import MyBot
import yaml
from config import *
# 读取配置文件
def readyaml():
    with open(os.path.abspath(pyconfig.configpath), 'r', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
    return config

configdata = readyaml()
os.environ['TOKEN'] = configdata['token']
os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT'] = configdata['host']
asyncio.run(MyBot(configdata).start())
