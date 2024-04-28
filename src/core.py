from typing import List, Optional, Union
from wechaty_puppet import FileBox  # type: ignore
from wechaty import Wechaty, Contact
from wechaty.user import Message, Room
from server.http import *

#bot 
class MyBot(Wechaty):
    def __init__(self):
        self.http = Http()
        super().__init__()
    async def on_message(self, msg: Message):
        """
        listen for message event
        """
        from_contact: Optional[Contact] = msg.talker()
        text = msg.text()
        room: Optional[Room] = msg.room()
        # 业务逻辑放在这里
        if text == 'ding':
            conversation: Union[Room, Contact] = from_contact if room is None else room
            await conversation.ready()

            await conversation.say('dong')

            data = self.http.post('http://192.168.10.8:8055/send/data/',{'key':text})
            await conversation.say(f'{data}')

