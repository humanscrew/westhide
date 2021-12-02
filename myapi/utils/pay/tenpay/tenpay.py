# -*- coding: utf-8 -*-
import os
from datetime import date, timedelta, datetime

import pandas as pd

from sqlalchemy.sql.expression import and_
from myapi.extensions import db
from myapi.models import TenPay

from flask import json
from wechatpayv3 import WeChatPay, WeChatPayType

from .bill_field import BillFieldLabel
from .apiclient.laiu8.config import TenPayConfig as Laiu8Config
from .apiclient.ennova.config import TenPayConfig as EnnovaConfig

DIRPATH = os.path.dirname(os.path.realpath(__file__))

config_map = {"laiu8": Laiu8Config, "ennova": EnnovaConfig}


class Tenpay:
    def __init__(self, platform, bill_date=None):
        self.platform = platform
        self.config = config_map.get(platform)
        self.tenpay = WeChatPay(
            wechatpay_type=WeChatPayType.NATIVE,
            mchid=self.config.MCHID.value,
            private_key=self.config.PRIVATE_KEY.value,
            cert_serial_no=self.config.CERT_SERIAL_NO.value,
            apiv3_key=self.config.APIV3_KEY.value,
            appid=self.config.APPID.value,
            notify_url=self.config.NOTIFY_URL.value,
            cert_dir=self.config.CERT_DIR.value,
            logger=self.config.LOGGER.value,
        )
        self.bill_date = bill_date or (date.today() + timedelta(days=-1)).strftime(
            "%Y-%m-%d"
        )
        self.download_url = None

    def trade_bill(self, bill_date=None):
        # 微信在次日9点启动生成前一天的对账单，建议商户10点后再获取
        self.bill_date = bill_date or self.bill_date
        code, message = getattr(self.tenpay, "trade_bill")(bill_date=self.bill_date)
        result = json.loads(message)
        if code in range(200, 300):
            self.download_url = result.get("download_url")
            return {"code": code, "result": result}
        else:
            return {"code": code, "result": {}, "message": result.get("message")}

    def download_bill(self, download_url=None, bill_date=None):
        self.download_url = download_url or self.download_url
        self.bill_date = bill_date or self.bill_date
        code, message = getattr(self.tenpay, "download_bill")(self.download_url)
        if code in range(200, 300) and isinstance(message, bytes):
            bill_file_path = os.path.join(
                DIRPATH,
                "bill_file",
                f"tenpay_bill_{self.bill_date}_{self.platform}.csv.gz",
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
            ten_pay = TenPay.query.filter(
                and_(
                    getattr(TenPay, "trade_time").like(self.bill_date + "%"),
                    getattr(TenPay, "mchid") == self.config.MCHID.value,
                )
            ).first()
            if ten_pay:
                return {"code": 400, "message": "已存在该日账单明细"}

            self.trade_bill()
            self.download_bill()

            bill_file_path = os.path.join(
                DIRPATH,
                "bill_file",
                f"tenpay_bill_{self.bill_date}_{self.platform}.csv.gz",
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
