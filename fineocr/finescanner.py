
import aiohttp
import uuid
import json
import os
import string
import random

from .urlreader import URLReader
from .doc import DocLangType, DocExportType


base_url = "https://webapi.finereaderonline.com"
token_url = base_url + "/OAuth2/Token"
users_url = base_url + "/Users"
task_source_url = base_url + "/TaskSources"
tasks_url = base_url + "/Tasks"

default_pass = "PBRF6Y4ScY7_!AQfU9NscANU5"

client_creds = {
    "ClientSecret": os.getenv('ClientSecret', "SGgo4TwLFhHJyIgoft9DTa3wVH2tygvRyTlHYnlzyHpOx"),
    "ClientId": os.getenv('ClientId', "1ebc2c2d-1ad5-49d1-b087-51a45b98bcdf")
}




def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


class FineUser:

    def __init__(self, uuid, fine_scanner_session):
        self.uuid = uuid
        self.token = None
        self.fine_scanner_session = fine_scanner_session

    @staticmethod
    async def create_new(fine_scanner_session):
        # get auth token to create new user
        auth_data = client_creds.copy()
        auth_data["GrantType"] = "ClientCredentials"
        token_req = await fine_scanner_session.post(token_url,
                                                    data=json.dumps(auth_data),
                                                    headers={
                                        "accept": "*/*",
                                        "content-type": "application/json",
                                        "user-agent": "FineScanner/7.14 (iPhone; iOS 13.5; Scale/2.00)",
                                        "accept-language": "en-US;q=1",
                                        "accept-encoding": "gzip, deflate, br"})
        token_resp = await token_req.json()
        create_user_token = token_resp.get('AccessToken')
        if not create_user_token:
            raise Exception(token_resp.get('ErrorCode'))

        # create new user
        fu = FineUser(str(uuid.uuid1()).upper(), fine_scanner_session)
        req_data = {"CountryAlpha2Code": "US",
                     "IsPromotionalEmailsAllowed": False,
                     "Email": fu.uuid + "@abbyyfsbestscanner.com",
                     "ClientCultureName": "en-US",
                     "Password": default_pass,
                     "RegistrationType": "Free"}
        create_user_req = await fine_scanner_session.post(users_url,
                                                    data=json.dumps(req_data),
                                                    headers={
                                                        "accept": "*/*",
                                                        "content-type": "application/json",
                                                        "authorization": "Bearer " + create_user_token,
                                                        "user-agent": "FineScanner/7.14 (iPhone; iOS 13.5; Scale/2.00)",
                                                        "accept-language": "en-US;q=1",
                                                        "accept-encoding": "gzip, deflate, br"})
        create_user_resp = await create_user_req.json()
        user_acc_token = create_user_resp.get('AccessToken')
        if not user_acc_token:
            raise Exception(create_user_resp.get('ErrorCode'))
        fu.token = user_acc_token

        return fu

    async def get_token(self):
        if self.token:
            return self.token

        # get new token from server
        auth_data = client_creds.copy()
        auth_data["GrantType"] = "Password"
        auth_data["Username"] = self.uuid + "@abbyyfsbestscanner.com"
        auth_data["Password"] = default_pass
        # req_data = urllib.parse.urlencode(auth_data)
        token_req = await self.fine_scanner_session.post(token_url,
                                                    data=auth_data,
                                                    headers={
                                                        "Content-Type": "application/x-www-form-urlencoded",
                                                        "Connection": "keep-alive",
                                                        "Accept": "*/*",
                                                        "User-Agent": "FineScanner/7.14.0.0 CFNetwork/1126 Darwin/19.5.0",
                                                        "Accept-Language": "en-us",
                                                        "Accept-Encoding": "gzip, deflate, br"})
        token_resp = await token_req.json()
        access_token = token_resp.get('AccessToken')
        if not access_token:
            raise Exception(token_resp.get('ErrorCode'))

        self.token = access_token
        return access_token


class FineScannerTask:
    def __init__(self, access_token, fine_scanner_session):
        self.token = access_token
        self.file_name = None
        self.task_source_id = None
        self.task_id = None
        self.fine_scanner_session = fine_scanner_session

    async def upload_file(self, body, filename, size):
        self.file_name = filename
        # task_source_url = 'http://127.0.0.1:8000/Test'
        mpwriter = aiohttp.MultipartWriter('form-data')
        # payload = aiohttp.payload.get_payload(body)
        # mp_item = mpwriter.append_payload(payload)
        mp_item = mpwriter.append(body)
        mp_item.set_content_disposition('form-data', filename=filename)
        mp_item._size = size
        cont_disp = ";".join(mp_item._headers[aiohttp.hdrs.CONTENT_DISPOSITION].split(";")[:-1])
        mp_item._headers[aiohttp.hdrs.CONTENT_DISPOSITION] = cont_disp
        del mp_item._headers[aiohttp.hdrs.CONTENT_TYPE]


        # fd = aiohttp.FormData()
        # fd.add_field('file', body, filename=filename)
        # mpw = fd._gen_form_data()
        # payload, encoding, te_encoding = mpw._parts[0]
        # del payload._headers[aiohttp.hdrs.CONTENT_TYPE]
        # # payload._headers[aiohttp.hdrs.CONTENT_LENGTH] = str(size)
        # mpw._parts[0] = (payload, encoding, te_encoding)
        upload_resp = await self.fine_scanner_session.post(task_source_url,
                                                      data=mpwriter,
                                                      headers={
                                                          "Content-Length": str(mpwriter.size),
                                                          "Connection": "close",
                                                          "Accept": "*/*",
                                                          "User-Agent": "FineScanner/7.14.0.0 CFNetwork/1126 Darwin/19.5.0",
                                                          "Authorization": "Bearer " + self.token,
                                                          "Accept-Language": "en-us",
                                                          "Accept-Encoding": "gzip, deflate"})
        upload_resp.raise_for_status()
        self.task_source_id = (await upload_resp.text()).replace("\"", "")
        return self.task_source_id

    async def run_task(self, export_type: DocExportType, langs: [DocLangType]):
        filename_no_ext = os.path.splitext(self.file_name)[0]
        if not filename_no_ext.isascii():
            filename_no_ext = get_random_string(8)
        else:
            filename_no_ext = "".join([c if c.isalnum() else "" for c in filename_no_ext])[:100]
        lang_map = {}
        for i, l in enumerate(langs):
            lang_map[f"Languages[{i}]"] = l.value
        data = {
            "ResultName": filename_no_ext,
            "ResultFileType": export_type.value,
            **lang_map,
            "TaskSourceIds[0]": self.task_source_id,
            "IsFreeQueue": False
        }

        run_task_resp = await self.fine_scanner_session.post(tasks_url,
                                                      data=data,
                                                      headers={
                                                          "Connection": "keep-alive",
                                                          "Accept": "*/*",
                                                          "User-Agent": "FineScanner/7.14.0.0 CFNetwork/1126 Darwin/19.5.0",
                                                          "Authorization": "Bearer " + self.token,
                                                          "Accept-Language": "en-us",
                                                          "Accept-Encoding": "gzip, deflate, br"})
        run_task_resp.raise_for_status()
        self.task_id = (await run_task_resp.text()).replace("\"", "")
        return self.task_id

    async def task_status(self):
        status_resp = await self.fine_scanner_session.get(tasks_url+"/"+self.task_id,
                                                        headers={
                                                            "Connection": "keep-alive",
                                                            "Accept": "*/*",
                                                            "User-Agent": "FineScanner/7.14.0.0 CFNetwork/1126 Darwin/19.5.0",
                                                            "Authorization": "Bearer " + self.token,
                                                            "Accept-Language": "en-us",
                                                            "Accept-Encoding": "gzip, deflate, br"})
        status = await status_resp.json()
        return status

    async def get_result(self):
        return await URLReader.create(tasks_url+"/"+self.task_id+"/Result",
                                      self.fine_scanner_session,
                               headers={"Accept": "*/*",
                                   "User-Agent": "FineScanner/7.14.0.0 CFNetwork/1126 Darwin/19.5.0",
                                   "Authorization": "Bearer " + self.token,
                                   "Accept-Language": "en-us"})


async def new_recognition(uuid):
    fuser = FineUser(uuid)
    access_token = await fuser.get_token()
    return FineScannerTask(access_token)



