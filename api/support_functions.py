import jwt
from rest_framework_jwt.utils import jwt_payload_handler
from Issue_tracker import settings
import requests, json

HOST_URL = 'smtp.gmail.com'
# EMAIL_HOST_USER = "baliksjosay@gmail.com"
# EMAIL_HOST_PASSWORD = 'zbpigqqxpnfyewnf'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

def get_authentication_details(request):
    """
    Decodes the authentication token provided.
    Decoding allows to extract the required identifying 
    information of the user as they work with the application.
    It takes in the request from which it attains the 'auth' parameter.
    """
    return jwt.decode(request.auth, settings.SECRET_KEY)

class Notification:
    def __init__(self, to, cc, bcc, subject, message):
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.subject = subject
        self.message = message

    def send_notification(self):
        DATA = {
            'tos': self.to,
            'ccs': self.cc,
            'bccs': self.bcc,
            'subject': self.subject,
            'description': self.message,
            'approval_url': None,
            'reject_url': None
            }
        print(DATA)
        request = requests.post(
            HOST_URL+'/notify/test',
            data = json.dumps(DATA),
            headers = {'Content-type': 'application/json'},
            timeout = None
        )
        response = json.loads(request.text)
        print(response)
        return True

    def get_to(self):
        return ['baliksjosay@gmail.com']
    
    def get_cc(self):
        return ['lemndev@gmail.com']

    def get_bcc(self):
        return ['gdexpertsug@gmail.com']
    

# class AdUser:
#     """
#     The AD users with MTN
#     """
#     def __init__(self, username, password):
#         self.username = username
#         self.password = password

#     def authenticate(self):
#         try:
#             DATA = {
#             "userName": self.username,
#             "Password": self.password
#             }
#             request = requests.post(
#                 HOST_URL+'/auth/user',
#                 data = json.dumps(DATA),
#                 headers = {'Content-type': 'application/json'},
#                 timeout = None
#             )
#             response = json.loads(request.text)
#             if response['authenticated'] == True:
#                 return response
#             else:
#                 return False
#         except Exception as e:
#             print("Exception found:::", str(e))
#             return False
# HOST_URL = 'https://smtp-relay.gmail.com/'

# def get_authentication_details(request):
#     """
#     Decodes the authentication token provided.
#     Decoding allows to extract the required identifying 
#     information of the user as they work with the application.
#     It takes in the request from which it attains the 'auth' parameter.
#     """
#     return jwt.decode(request.auth, settings.SECRET_KEY)

# class Notification:
#     def __init__(self, to, cc, bcc, subject, message):
#         self.to = to
#         self.cc = cc
#         self.bcc = bcc
#         self.subject = subject
#         self.message = message

#     def send_notification(self):
#         DATA = {
#             'tos': self.to,
#             'ccs': self.cc,
#             'bccs': self.bcc,
#             'subject': self.subject,
#             'description': self.message,
#             'approval_url': None,
#             'reject_url': None
#             }
#         print(DATA)
#         request = requests.post(
#             HOST_URL+'/notify/test',
#             data = json.dumps(DATA),
#             headers = {'Content-type': 'application/json'},
#             timeout = None
#         )
#         response = json.loads(request.text)
#         print(response)
#         return True

#     def get_to(self):
#         return ['baliksjosay@gmail.com']
    
#     def get_cc(self):
#         return ['joseph.balikuddembe@gdexperts.com']

#     def get_bcc(self):
#         return ['peace.kikoni@gdexperts.com.com']
    
