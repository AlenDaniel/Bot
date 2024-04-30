from typing import List, Optional, Union
from wechaty_puppet import FileBox  # type: ignore
from wechaty import Wechaty, Contact
from wechaty.user import Message, Room
from server.http import *
from loguru import logger as log
from http import HTTPStatus
import dashscope
import re

#bot 
class MyBot(Wechaty):
    def __init__(self,config):
        self.http = Http()
        self.key = config['api_key']
        self.model_list = config['model_list']
        self.model_slect = config['model_select']
        self.mode = config['mode']
        self.model_url = config['model_url']
        self.ignore = config['ignore_list']
        dashscope.api_key=self.key
        super().__init__()
    async def on_message(self, msg: Message):
        from_contact: Optional[Contact] = msg.talker()
        text = msg.text()
        if self.contains_xml_like_structure(text):
            return
        if from_contact.contact_id in self.ignore:
            return
        room: Optional[Room] = msg.room()
        # 业务逻辑放在这里
        if msg.is_self():
            return
        # tag = msg.from()
        if text == 'ding':
            conversation: Union[Room, Contact] = from_contact if room is None else room
            await conversation.ready()
            await conversation.say('dong')
        else:
            conversation: Union[Room, Contact] = from_contact if room is None else room
            await conversation.ready()
            bulid = self.togger(self.mode)
            data = bulid(text)
            await conversation.say(f'{data}')
    #   选择模型
    def togger(self,bool):
        if bool == 0:
            return self.llama2_local
        else:
            if bool == 1:
                return self.tongwen
            else:
                return self.tongwen
        
    #  ali model
    def tongwen(self,prompt_text):
        model = self.model_list[self.mode][self.model_slect]
        resp = dashscope.Generation.call(
            # models=self.model_list[self.model_slect],
            model=model,
            prompt=prompt_text
        )
        if resp.status_code == HTTPStatus.OK:
            return resp.output['text']
        else:
            log.error(resp.code)  # The error code.
            log.error(resp.message)  # The error message.
            return '对不起，网络故障,请重新提问！'
    
    # localmodel
    def llama2_local(self,prompt):
        data = self.http.post(self.model_url,{'key':prompt})
        if data.status_code == HTTPStatus.OK:
            return data['text']
        else:
           log.error(data.code)  # The error code.
           return '对不起，网络故障！请重新提问！'
    import re

    def contains_xml_like_structure(self,s):
        pattern = r'<[^>]+>'
        return bool(re.search(pattern, s))