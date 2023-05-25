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

def send_otp(request):
    mobile = request.POST['mobile']
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
        'message'       : otp + ' is your One-Time-Password (OTP) to login at your Kidly account. Thank You! HRLOOM',
        'priority'      : '1',
        'dnd'           : '1',
        'unicode'       : '0',
        'dlttemplateid' : '1707166745786444045',
        }
    headers = {}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response)
    return JsonResponse({'otp' : otp}, status = 200)

