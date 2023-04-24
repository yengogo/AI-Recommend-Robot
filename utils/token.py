"""取Token

取得Token。
"""

from datetime import datetime
import hashlib
import json
import requests
import uuid


CONTENT_TYPE_JSON = "application/json"
# Token
TOKEN_API_KEY = "608269248"
TOKEN_API_SECRET = "754559343"
TOKEN_API_DOMAIN = "https://uauth.api.liontravel.com"

class Token(object):
    """
    一個用來取得token的class

    Attributes
    ----------
    session : class
        設定連線網頁所要使用的Session
    utc_api_url : str
        與主機時間校時使用的URL
    guid : str
        UUID
    api_key : str
        系統或API的ApiKey
    api_secret : str
        系統或API的ApiSecret
    token_domain : str
        Token API Domain
    token_api : str
        Token API路徑

    Methods
    -------
    get_token()
        取得Token
    """

    def __init__(self):
        self.session = requests.Session()
        self.utc_api_url = "https://auth.api.liontravel.com/api/ServerTime/Check"
        self.guid = uuid.uuid4().hex
        self.api_key = TOKEN_API_KEY
        self.api_secret = TOKEN_API_SECRET
        self.token_domain = TOKEN_API_DOMAIN
        self.token_api = "/v2/token/generator"  # Token API路徑

    def get_token(self):
        """取得Token

        使用POST方法取得Token的值。

        Returns
        -------
        str or None
            Token的值
        """
        # 與主機時間校時
        utc_response = self.session.get(self.utc_api_url)
        utc_result = json.loads(utc_response.text)

        if "DateTimeUtc" in utc_result.keys():
            utc_now = utc_result["DateTimeUtc"].split(
                "T")[1].split("Z")[0].replace(":", "")
        else:
            utc_now = str(datetime.utcnow()).split(
                " ")[1].split(".")[0].replace(":", "")

        # 驗證碼規則：MD5(guid + ApiKey + ApiSecret + HHmmss) + guid
        md5 = hashlib.md5()
        md5.update((self.guid + self.api_key + self.api_secret +
                   utc_now).encode(encoding='utf-8'))
        check_sum = str(md5.hexdigest()) + self.guid

        token_api_url = self.token_domain + self.token_api
        token_payload = {
            "ApiKey": self.api_key,
            "ApiSecret": self.api_secret,
            "CheckSum": check_sum
        }
        token_headers = {
            "Content-Type": CONTENT_TYPE_JSON,
        }
        token_response = self.session.post(
            token_api_url, data=json.dumps(token_payload), headers=token_headers)
        token_result = json.loads(token_response.text)
        token = None

        if token_result.get("rCode") == "0000":
            token = token_result.get("Data").get("AccessToken")
        else:
            print(token_response.text)

        self.session.close()
        return token
