import http.client
import json
from social.settings.development import MSG91_AUTH_KEY

def send_reset_link(user, reset_url):

    conn = http.client.HTTPSConnection("control.msg91.com")

    payload = {
        "recipients": [
            {
            "to": [
                {
                "email": user.email,
                "name": user.name
                }
            ],
            "variables": {
                "VAR1": user.username,
                "username": user.username,
                "reset_link": reset_url
            }
            }
        ],
        "from": {
            "email": "no-reply@r8eikb.mailer91.com"
        },
        "domain": "r8eikb.mailer91.com",
        "template_id": "password_reset_55"
        }

    headers = {
        'accept': "application/json",
        'authkey': MSG91_AUTH_KEY,
        'content-type': "application/JSON"
    }

    conn.request("POST", "/api/v5/email/send", json.dumps(payload), headers)

    res = conn.getresponse()
    data = res.read()

    return

def verify_otp_mail(user):

    conn = http.client.HTTPSConnection("control.msg91.com")

    payload = {
        "recipients": [
            {
            "to": [
                {
                "email": user.email,
                "name": user.name
                }
            ],
            "variables": {
                "company_name": "Social",
                "otp": user.otp
            }
            }
        ],
        "from": {
            "email": "no-reply@r8eikb.mailer91.com"
        },
        "domain": "r8eikb.mailer91.com",
        "template_id": "global_otp"
        }

    headers = {
        'accept': "application/json",
        'authkey': MSG91_AUTH_KEY,
        'content-type': "application/JSON"
    }

    conn.request("POST", "/api/v5/email/send", json.dumps(payload), headers)

    res = conn.getresponse()
    data = res.read()

    return