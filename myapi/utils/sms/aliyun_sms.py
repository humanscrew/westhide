# -*- coding: utf-8 -*-

from flask import json
from myapi.config import ALIYUN_SMS
from myapi.utils.sms import smsTemplate

from random import randint
from datetime import datetime

from alibabacloud_dysmsapi20170525.client import Client as DysmsapiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_models
from alibabacloud_tea_util.client import Client as UtilClient

from myapi.extensions import db
from myapi.models import SmsAliyun, SmsAliyunDetail
from myapi.api.schemas import SmsAliyunSchema, SmsAliyunDetailSchema


class AliyunSms:
    def __init__(self, access_key_id=None, access_key_secret=None, sign_name=None, template_code=None, template_param={}):
        self.access_key_id = access_key_id or ALIYUN_SMS.get("access_key_id")
        self.access_key_secret = access_key_secret or ALIYUN_SMS.get("access_key_secret")
        self.sign_name = sign_name or smsTemplate["auth"]["signName"]
        self.template_code = template_code or smsTemplate["auth"]["templateCode"]

        if not template_param:
            for param in smsTemplate["auth"]["templateParam"]:
                authCode = ""
                for i in range(6):
                    authCode += str(randint(0, 9))
                template_param[param] = authCode
        self.template_param = template_param

    @staticmethod
    def value2str(value):
        if isinstance(value, list):
            return ",".join(str(item) for item in value)
        else:
            return str(value)

    def create_client(self):
        config = open_api_models.Config()
        config.access_key_id = self.access_key_id
        config.access_key_secret = self.access_key_secret
        return DysmsapiClient(config)

    def send(self, phone_numbers):
        client = self.create_client()
        phone_numbers_str = AliyunSms.value2str(phone_numbers)
        template_param = json.dumps(self.template_param)

        send_req = dysmsapi_models.SendSmsRequest(
            phone_numbers=phone_numbers_str,
            sign_name=self.sign_name,
            template_code=self.template_code,
            template_param=template_param
        )
        send_date = datetime.now().strftime('%Y%m%d')
        send_resp = client.send_sms(send_req)
        # Resquest Response Format
        # send_resp = {
        #     "headers": {
        #         "date": "Wed, 10 Nov 2021 02:29:22 GMT",
        #         "content-type": "application/json;charset=utf-8",
        #         "content-length": "110",
        #         "connection": "keep-alive",
        #         "access-control-allow-origin": "*",
        #         "access-control-allow-methods": "POST, GET, OPTIONS, PUT, DELETE",
        #         "access-control-allow-headers": "X-Requested-With, X-Sequence, _aop_secret, _aop_signature, x-acs-action, x-acs-version, x-acs-date, Content-Type",
        #         "access-control-max-age": "172800",
        #         "x-acs-request-id": "9EDDD03F-E460-56C1-9BCB-C142DD13D38E"
        #     },
        #     "body": {
        #         "BizId": "143307836511361915^0",
        #         "Code": "OK",
        #         "Message": "OK",
        #         "RequestId": "9EDDD03F-E460-56C1-9BCB-C142DD13D38E"
        #     }
        # }

        code = send_resp.body.code
        request_id = send_resp.body.request_id
        biz_id = send_resp.body.biz_id
        message = send_resp.body.message

        smsAliyunMeta = {
            'phone_numbers': phone_numbers_str,
            'sign_name': self.sign_name, "template_code": self.template_code, "template_param": template_param,
            'send_date': send_date,
            'request_id': request_id, "biz_id": biz_id,
            'code': code, "message": message,
        }
        smsAliyunSchema = SmsAliyunSchema(partial=True)
        smsAliyun = smsAliyunSchema.load(smsAliyunMeta)
        db.session.add(smsAliyun)
        db.session.commit()

        if UtilClient.equal_string(code, 'OK'):
            return {"phoneNumbers": phone_numbers, "bizId": biz_id, "sendDate": send_date, "code": 200, "message": "短信验证已发送"}
        else:
            return {"code": 400, "message": message}

    def query(self, **kwargs):
        client = self.create_client()
        phone_numbers = AliyunSms.value2str(kwargs.get("phoneNumbers")).split(',')
        biz_id = kwargs.get("bizId")
        send_date = kwargs.get("sendDate")
        for phone_num in phone_numbers:
            query_req = dysmsapi_models.QuerySendDetailsRequest(
                phone_number=UtilClient.assert_as_string(phone_num),
                biz_id=biz_id,
                send_date=send_date,
                page_size=10,
                current_page=1
            )
            query_resp = client.query_send_details(query_req)
            # Query Response Format
            # {
            #     "headers": {
            #         "date": "Wed, 10 Nov 2021 03:56:12 GMT",
            #         "content-type": "application/json;charset=utf-8",
            #         "content-length": "419",
            #         "connection": "keep-alive",
            #         "access-control-allow-origin": "*",
            #         "access-control-allow-methods": "POST, GET, OPTIONS, PUT, DELETE",
            #         "access-control-allow-headers": "X-Requested-With, X-Sequence, _aop_secret, _aop_signature, x-acs-action, x-acs-version, x-acs-date, Content-Type",
            #         "access-control-max-age": "172800",
            #         "x-acs-request-id": "6BC6A8BE-D546-5415-A48A-FD14E9C050CA"
            #     },
            #     "body": {
            #         "Code": "OK",
            #         "Message": "OK",
            #         "RequestId": "6BC6A8BE-D546-5415-A48A-FD14E9C050CA",
            #         "result": {
            #             "SmsSendDetailDTO": [{
            #                 "Content": "【westhide平台】您的验证码704057，该验证码5分钟内有效，请确认是否本人操作。",
            #                 "ErrCode": "DELIVERED",
            #                 "PhoneNum": "#",
            #                 "ReceiveDate": "2021-11-10 10:29:28",
            #                 "SendDate": "2021-11-10 10:29:22",
            #                 "SendStatus": 3,
            #                 "TemplateCode": "SMS_224280228"
            #             }]
            #         },
            #         "TotalCount": 1
            #     }
            # }
            result = query_resp.body.sms_send_detail_dtos.to_map().get("SmsSendDetailDTO")[0]
            request_id = query_resp.body.request_id
            smsAliyun = SmsAliyun.query.filter_by(biz_id=biz_id).first_or_404()
            smsAliyunDetail = SmsAliyunDetail.query.filter_by(biz_id=biz_id).first()
            if not biz_id:
                smsAliyunDetailMeta = {
                    "biz_id": biz_id,
                    'request_id': request_id,
                    "phone_num": result["PhoneNum"], "context": result["Content"], "send_status": result["SendStatus"],
                    "err_code": result["ErrCode"], "template_code": result["TemplateCode"],
                    "receive_date": result["ReceiveDate"], "send_date": result["SendDate"],
                    "out_id": result.get("OutId"),
                }
                smsAliyunDetailSchema = SmsAliyunDetailSchema(partial=True)
                smsAliyunDetail = smsAliyunDetailSchema.load(smsAliyunDetailMeta)
                db.session.add(smsAliyunDetail)
                db.session.commit()

            if UtilClient.equal_string(query_resp.body.code, 'OK'):
                return {"result": result, "code": 200, "message": "查询成功"}
            else:
                return {"result": {}, "code": 400, "message": query_resp.body.message}
