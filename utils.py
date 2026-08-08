from kavenegar import *
import random  

def create_random_code(count):  
    import random  
    count-= 1  
    return random.randint(10**count, 10**(count+1)-1)  


def send_sms(mobile_number, active_code ): 
    try:
        api = KavenegarAPI('30444D474A55744A6C3771636450346767742B766F565A41476B74573242707849497268444B315A5448773D')
        token = create_random_code(5)
        params = {
        'receptor': mobile_number,
        'template': 'codeverify',
        'message': f'کد فعال سازی حساب کاربری شما {active_code } می‌باشد.',
        'token': str(active_code ), # Convert the random number to a string for token
        'token2': '',
        'token3': '',
        'type': 'sms', # sms vs call
        }
        response = api.verify_lookup(params)
        if response is None:  
            print("Failed to send SMS.")  
        else:  
            print("SMS sent successfully:", response) 
   
        return response  
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e) 

    
#-----------------------------------------------------------
## creat class for image upload_to all models
import os
from uuid import uuid4
class FileUpload :
    def __init__(self, dir, prefix) -> None:
        self.dir = dir
        self.prefix = prefix
    def upload_to(self, instance, filename) :
        filename, ext = os.path.splitext(filename)
        return f"{self.dir}/{self.prefix}/{uuid4()}{ext}"
# -*- coding: utf-8 -*-
# from kavenegar import *
# import random
# import os
# from uuid import uuid4
 
 
# import requests
# import json

# def send_sms(mobile_number, active_code):
#     """
#     ارسال کد فعال‌سازی با استفاده از API مستقیم Kavenegar
#     """
#     if not mobile_number or not active_code:
#         print("❌ شماره موبایل یا کد فعال‌سازی معتبر نیست")
#         return False
    
#     print(f"📱 ارسال کد به شماره: {mobile_number}")
#     print(f"🔑 کد فعال‌سازی: {active_code}")
    
#     # ====== برای تست در محیط محلی ======
#     import os
#     if os.getenv('DJANGO_ENV') == 'local':
#         print("🔄 حالت تست: پیامک ارسال نشد (محیط لوکال)")
#         return True
    
#     try:
#         API_KEY = '30444D474A55744A6C3771636450346767742B766F565A41476B74573242707849497268444B315A5448773D'
        
#         # API مستقیم کاوه‌نگار
#         url = f'https://api.kavenegar.com/v1/{API_KEY}/verify/lookup.json'
        
#         params = {
#             'receptor': str(mobile_number),
#             'token': str(active_code),
#             'template': 'codeverify',
#             'type': 'sms',
#         }
        
#         response = requests.post(url, data=params)
        
#         if response.status_code == 200:
#             print(f"✅ پیامک با موفقیت ارسال شد: {response.json()}")
#             return True
#         else:
#             print(f"❌ خطا در ارسال: {response.text}")
#             return False
            
#     except Exception as e:
#         print(f"❌ خطا: {e}")
#         return False





# #     from utils import send_sms, create_random_code

# # # ایجاد کد 5 رقمی
# # code = create_random_code(5)
# # print(f"کد: {code}")

# # # ارسال پیامک به شماره خودتان
# # result = send_sms('09123281009', code)  # شماره خود را وارد کنید
# # print(f"نتیجه: {result}")