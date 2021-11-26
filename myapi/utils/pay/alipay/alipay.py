#!/usr/bin/env python
# -*- coding: utf-8 -*-
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradeCreateModel import AlipayTradeCreateModel
from alipay.aop.api.request.AlipayDataDataserviceBillDownloadurlQueryRequest import (
    AlipayDataDataserviceBillDownloadurlQueryRequest,
)
from alipay.aop.api.response.AlipayDataDataserviceBillDownloadurlQueryResponse import (
    AlipayDataDataserviceBillDownloadurlQueryResponse,
)
from .apiclient.config import alipay_client_config, logger


class Alipay:
    def __init__(self, client=None, params=None):
        self.client = client or DefaultAlipayClient(alipay_client_config, logger=logger)
        self.request = None
        self.model = AlipayTradeCreateModel()
        self.params = self.request_params(params)

    def request_params(self, params):
        if isinstance(params, dict):
            for key in params:
                setattr(self.model, key, params[key])
                self.request = AlipayDataDataserviceBillDownloadurlQueryRequest(
                    biz_model=self.model
                )

        return params

    def execute_request(self, params=None):
        if params:
            self.request_params(params)

        if self.request is None:
            return {"code": 400, "message": "请求参数为空"}

        response_content = self.client.execute(self.request)
        response = AlipayDataDataserviceBillDownloadurlQueryResponse()
        response.parse_response_content(response_content)

        if response.is_success():
            return response
        else:
            return {
                "code": response.code,
                "message": f"{response.msg}:{response.sub_msg}",
                "subCode": response.sub_code,
            }


# Alipay(params={"bill_type": "trade", "bill_date": "2021-10-05"}).execute_request()
