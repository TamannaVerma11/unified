import requests
import json
import math, random
from myAdmin.models import OTPDevice
from django.http import *

def generateOTP() :
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def send_otp(request, mobile=None):
    otp = generateOTP()
    OTPDevice.objects.update_or_create(
        mobile = mobile,
        defaults={'mobile' : mobile,'otp' : otp, 'is_verified' : 0}
    )
    url = 'https://www.kit19.com/ComposeSMS.aspx'
    data = {
        'username'      : 'heirloom683678',
        'password'      : '8935',
        'sender'        : 'HRLOOM',
        'to'            : mobile,
        'message'       : otp + ' is your One Time Password (OTP) to verify your phone number on Tabschool. Thank You! HRLOOM',
        'priority'      : '1',
        'dnd'           : '1',
        'unicode'       : '1',
        'dlttemplateid' : '1707167750077393703',
        }
    headers = {}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response)
    return JsonResponse({'otp' : otp}, status = 200)

def verify_otp(mobile, otp):
    device = OTPDevice.objects.get(mobile  = mobile)
    if device.otp == otp:
        return True
    return False


