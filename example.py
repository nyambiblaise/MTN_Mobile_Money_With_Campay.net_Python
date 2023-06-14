
from campay.sdk import Client


campay = Client({
    "app_username" : "",
    "app_password" : "",
    "environment" : "DEV" #"DEV" = demo mode, "PROD" = live mode
})


collect = campay.collect({
    "amount": "5",
    "currency": "XAF",
    "from": "237xxxxxxxx",
    "description": "some description"
})


collect = campay.get_payment_link({
    "amount": "5",
    "currency": "XAF",
    "description": "some description",
    "external_reference": "12345678",
    "redirect_url": "https://mysite.com/"
})


disburse = campay.disburse({
    "amount": "5",
    "currency": "XAF",
    "to": "237xxxxxxxx",
    "description": "some description"
})


balance = campay.get_balance()