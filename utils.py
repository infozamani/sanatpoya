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
   