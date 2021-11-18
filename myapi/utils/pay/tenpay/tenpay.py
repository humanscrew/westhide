# -*- coding: utf-8 -*-
import os
from random import sample
from datetime import date, timedelta, datetime
from string import digits, ascii_letters

import pandas as pd

from myapi.extensions import db
from myapi.models import TenPay

from flask import jsonify, request, json
from wechatpayv3 import WeChatPay, WeChatPayType

from .apiclient.config import TenPayConfig, BillFieldLabel

MCHID = TenPayConfig.MCHID.value
CERT_DIR = TenPayConfig.CERT_DIR.value
PRIVATE_KEY = TenPayConfig.PRIVATE_KEY.value
CERT_SERIAL_NO = TenPayConfig.CERT_SERIAL_NO.value
APIV3_KEY = TenPayConfig.APIV3_KEY.value
APPID = TenPayConfig.APPID.value
NOTIFY_URL = TenPayConfig.NOTIFY_URL.value
LOGGER = TenPayConfig.LOGGER.value

DIRPATH = os.path.dirname(os.path.realpath(__file__))


class Tenpay:
    def __init__(self, bill_date=None):
        self.tenpay = WeChatPay(
            wechatpay_type=WeChatPayType.NATIVE,
            mchid=MCHID,
            private_key=PRIVATE_KEY,
            cert_serial_no=CERT_SERIAL_NO,
            apiv3_key=APIV3_KEY,
            appid=APPID,
            notify_url=NOTIFY_URL,
            cert_dir=CERT_DIR,
            # logger=LOGGER
        )
        self.bill_date = bill_date
        self.download_url = None

    def pay_native(self):
        # 以native下单为例，下单成功后即可获取到'code_url'，将'code_url'转换为二维码，并用微信扫码即可进行支付测试。
        out_trade_no = "".join(sample(ascii_letters + digits, 8))
        description = "demo-description"
        amount = 1
        code, message = self.tenpay.pay(
            description=description,
            out_trade_no=out_trade_no,
            amount={"total": amount, "currency": "CNY"},
        )
        result = json.loads(message)
        return {"code": code, "result": result}

    def pay_jsapi(self):
        # jsApi下单，tenpay初始化的时候，wechatpay_type设置为WeChatPayType.JSAPI。
        # 下单成功后，将prepay_id和其他必须的参数组合传递给JS SDK的wx.choosetenpay接口唤起支付
        out_trade_no = "".join(sample(ascii_letters + digits, 8))
        description = "demo-description"
        amount = 1
        payer = {"openid": "demo-openid"}
        code, message = self.tenpay.pay(
            description=description,
            out_trade_no=out_trade_no,
            amount={"total": amount, "currency": "CNY"},
            payer=payer,
        )
        result = json.loads(message)
        if code in range(200, 300):
            prepay_id = result.get("prepay_id")
            timestamp = "demo-timestamp"
            nonce_str = "demo-nonce_str"
            package = "prepay_id=" + prepay_id
            pay_sign = self.tenpay.sign([APPID, timestamp, nonce_str, package])
            sign_type = "RSA"
            return {
                "code": 0,
                "result": {
                    "appId": APPID,
                    "timestamp": timestamp,
                    "nonceStr": nonce_str,
                    "package": "prepay_id=%s" % prepay_id,
                    "signType": sign_type,
                    "paySign": pay_sign,
                },
            }
        else:
            return {"code": -1, "result": {"reason": result.get("code")}}

    def pay_h5(self):
        # h5支付下单，tenpay初始化的时候，wechatpay_type设置为WeChatPayType.H5。
        # 下单成功后，将获取的的h5_url传递给前端跳转唤起支付。
        out_trade_no = "".join(sample(ascii_letters + digits, 8))
        description = "demo-description"
        amount = 1
        scene_info = {"payer_client_ip": "1.2.3.4", "h5_info": {"type": "Wap"}}
        code, message = self.tenpay.pay(
            description=description,
            out_trade_no=out_trade_no,
            amount={"total": amount, "currency": "CNY"},
            scene_info=scene_info,
        )
        result = json.loads(message)
        return {"code": code, "result": result}

    def pay_mini_program(self):
        # 小程序支付下单，tenpay初始化的时候，wechatpay_type设置为WeChatPayType.MINIPROG。
        # 下单成功后，将prepay_id和其他必须的参数组合传递给小程序的wx.requestPayment接口唤起支付
        out_trade_no = "".join(sample(ascii_letters + digits, 8))
        description = "demo-description"
        amount = 1
        payer = {"openid": "demo-openid"}
        code, message = self.tenpay.pay(
            description=description,
            out_trade_no=out_trade_no,
            amount={"total": amount, "currency": "CNY"},
            payer=payer,
        )
        result = json.loads(message)
        if code in range(200, 300):
            prepay_id = result.get("prepay_id")
            timestamp = "demo-time_stamp"
            nonce_str = "demo-nonce_str"
            package = "prepay_id=" + prepay_id
            pay_sign = self.tenpay.sign([APPID, timestamp, nonce_str, package])
            sign_type = "RSA"
            return jsonify(
                {
                    "code": 0,
                    "result": {
                        "appId": APPID,
                        "timestamp": timestamp,
                        "nonceStr": nonce_str,
                        "package": "prepay_id=%s" % prepay_id,
                        "signType": sign_type,
                        "paySign": pay_sign,
                    },
                }
            )
        else:
            return {"code": -1, "result": {"reason": result.get("code")}}

    def pay_app(self):
        # app支付下单，tenpay初始化的时候，wechatpay_type设置为WeChatPayType.APP。
        # 下单成功后，将prepay_id和其他必须的参数组合传递给IOS或ANDROID SDK接口唤起支付
        out_trade_no = "".join(sample(ascii_letters + digits, 8))
        description = "demo-description"
        amount = 1
        code, message = self.tenpay.pay(
            description=description,
            out_trade_no=out_trade_no,
            amount={"total": amount, "currency": "CNY"},
        )
        result = json.loads(message)
        if code in range(200, 300):
            prepay_id = result.get("prepay_id")
            timestamp = "demo-timestamp"
            nonce_str = "demo-nonce_str"
            package = "Sign=tenpay"
            pay_sign = "demo-pay_sign"
            return {
                "code": 0,
                "result": {
                    "appId": APPID,
                    "partnerId": MCHID,
                    "prepayId": prepay_id,
                    "package": package,
                    "nonceStr": nonce_str,
                    "timestamp": timestamp,
                    "sign": pay_sign,
                },
            }
        else:
            return {"code": -1, "result": {"reason": result.get("code")}}

    def notify(self):
        result = self.tenpay.decrypt_callback(request.headers, request.data)
        if result:
            resp = json.loads(result)
            appid = resp.get("appid")
            mchid = resp.get("mchid")
            out_trade_no = resp.get("out_trade_no")
            transaction_id = resp.get("transaction_id")
            trade_type = resp.get("trade_type")
            trade_state = resp.get("trade_state")
            trade_state_desc = resp.get("trade_state_desc")
            bank_type = resp.get("bank_type")
            attach = resp.get("attach")
            success_time = resp.get("success_time")
            payer = resp.get("payer")
            amount = resp.get("amount").get("total")
            # TODO: 根据返回参数进行必要的业务处理，处理完后返回200或204
            return {"code": "200", "message": "支付接口回调成功"}
        else:
            return {"code": "400", "message": "支付接口回调失败"}

    def trade_bill(self, bill_date=None):
        # 微信在次日9点启动生成前一天的对账单，建议商户10点后再获取
        self.bill_date = (
            bill_date
            or self.bill_date
            or (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
        )
        code, message = self.tenpay.trade_bill(bill_date=self.bill_date)
        result = json.loads(message)
        if code in range(200, 300):
            self.download_url = result.get("download_url")
            return {"code": code, "result": result}
        else:
            return {"code": code, "result": {}, "message": result.get("message")}

    def download_bill(self, download_url=None, bill_date=None):
        self.download_url = download_url or self.download_url
        self.bill_date = bill_date or self.bill_date
        code, message = self.tenpay.download_bill(self.download_url)
        if code in range(200, 300) and isinstance(message, bytes):
            bill_file_path = os.path.join(
                DIRPATH, "bill_file", f"tenpay_bill_{self.bill_date}.csv.gz"
            )
            with open(bill_file_path, "wb") as f:
                f.write(message)
            return {"code": code, "bill": message}
        else:
            result = json.loads(message)
            return {"code": code, "result": {}, "message": result.get("message")}

    def transfer_bill2db(self, bill_date=None):
        try:
            self.bill_date = bill_date or self.bill_date
            if TenPay.query.first():
                ten_pay = TenPay.query.filter(
                    getattr(TenPay, "trade_time").like(self.bill_date + "%")
                ).first()
                if ten_pay:
                    return {"code": 400, "message": "已存在该日账单明细"}

            self.trade_bill()
            self.download_bill()

            bill_file_path = os.path.join(
                DIRPATH, "bill_file", f"tenpay_bill_{self.bill_date}.csv.gz"
            )
            df = pd.read_csv(bill_file_path, compression="gzip", header=0, sep=",")
            # df.columns.values = [BillFieldLabel(col).name for col in df.columns.values]
            df.rename(columns=lambda x: BillFieldLabel(x).name, inplace=True)
            df = df[:-2]
            for col in df.columns.values:
                # df[col] = df[col].apply(lambda x: x[1:])
                df[col] = df[col].str.strip(r"`")

            df["create_time"] = datetime.now()
            df["update_time"] = datetime.now()
            df.to_sql(
                name="tenpay_bill",
                con=db.get_engine(),
                chunksize=500,
                if_exists="append",
                index=False,
            )
            return {"code": 200, "bill": df.to_dict(orient="records")}
        except:
            return {"code": 400, "message": "账单传输失败"}


# from io import BytesIO
# import gzip
# buff = BytesIO(resp)
# gf = gzip.GzipFile(fileobj=buff)
# content = gf.read().decode('utf-8')
