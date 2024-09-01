import os
import qianfan
from models.model_interface import ModelInterface


class QianfanModel(ModelInterface):
    def __init__(self):
        # ���û�������
        os.environ["QIANFAN_AK"] = "QcJI8LwewQ4Z3ayP3IRejTAN"
        os.environ["QIANFAN_SK"] = "NYbSGzrfVuY2ebVI4s2fTlzIvLpOD0Zk"
        # ��ʼ��Qianfanģ��
        self.chat_comp = qianfan.ChatCompletion()

    def get_response(self, messages):
        response = self.chat_comp.do(model="ERNIE-4.0-8K", messages=messages)
        return response["body"]["result"]
