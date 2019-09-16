from django.shortcuts import render
from django.contrib.auth import authenticate
from Issue_tracker import settings
from api.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_jwt.utils import jwt_payload_handler

from api import support_functions as SF
from api.serializers import GetUsers 
from django.db import transaction
import jwt, datetime


class UserLogin(APIView):
    """
    Login of users
    """
    permission_classes = (AllowAny, )
    def post(self, request, format=None):

        
        auth_user = User.objects.get(email = request.data['user_email'])
        payload = jwt_payload_handler(auth_user)

        response = {}
        
        token = jwt.encode(payload, settings.SECRET_KEY)
        response['token'] = token
        response['username'] = auth_user.user_name
        response['email'] = auth_user.email
        response['message'] = "Welcome"
        response['user_role'] = auth_user.user_role
        response['code'] = 200

        return Response(response, status = status.HTTP_200_OK)
        

class UserMgt(APIView):
    # parser_classes = (MultiPartParser, FormParser)
    permission_classes = (AllowAny, )

    def post(self, request, format=None):

        data = request.data.dict()
        user_name = data['user_name']
        company_name = data['client_name']
        user_email = data['user_email']
        user_role = data['user_role']
        password = data['signup_password']

        if data['gde_staff'] == 'Support':
            is_staff = True
        else:
             is_staff = False
           
        
        try:
            reg = ApplicationUser(user_email, password, user_name, user_role, company_name, is_staff)
            reg.register_user()
            print(data)

            response = {}
            auth_user = User.objects.get(email=user_email)
            print(auth_user)

            response['username'] = auth_user.user_name
            response['email'] = auth_user.email
            response['isGDE_staff'] = auth_user.is_staff
            response['user_role'] = auth_user.user_role
            response['message'] = "User Successfully created"
            response['code'] = 200
            # print(response)
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(str(e))
            response = {}
            response['message'] = str(e)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        except KeyError as e:
            print(e)
        response = {}
        response['message'] = 'Please provide login credentials'
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
        # return Response(status=status.HTTP_409_CONFLICT)

    def get(self, request, format=None):
        user_status = request.GET.get('status')
        print(user_status)
               
        if user_status == 'All':
            users = User.objects.all()
            users = GetUsers(users, many=True)
            return Response(users.data, status = status.HTTP_200_OK)        
        
        if user_status == 'Client':
            users = User.objects.filter(is_staff = False)
            users = GetUsers(users, many=True)
            return Response(users.data, status = status.HTTP_200_OK)        

        if user_status == 'Support':
            users = User.objects.filter(is_staff = True)
            users = GetUsers(users, many=True)
            return Response(users.data, status = status.HTTP_200_OK) 
            
        if user_status == 'Admin':
            users = User.objects.filter(is_staff = False)
            users = GetUsers(users, many=True)
            return Response(users.data, status = status.HTTP_200_OK)         
        
        if user_status != 'search':
            users = User.objects.all()
            users = GetUsers(users, many=True)
            return Response(users.data, status = status.HTTP_200_OK)
        
        if user_status == 'search':
            users = User.objects.all()
            user_role = request.GET.get('user_role')
            user_name = request.GET.get('user_name')
            user_id = request.GET.get('user_id')

            if not user_id == None and len(user_id) > 0:
                users = users.filter(id = user_id)
            else:
                if not user_name == None and len(user_name) > 0:
                    users = users.filter(user_name__icontains = user_name)
                if not user_role == None and len(user_role) > 0:
                    users = users.filter(user_role__icontains = user_role)
                                  
            users = GetUsers(users, many=True)
            return Response(users.data, status = status.HTTP_200_OK)


        
class ApplicationUser:
    def __init__(self, user_email, password, user_name, user_role, company_name, is_staff):
        self.user_email = user_email
        self.password = password
        self.user_name = user_name
        self.user_role = user_role
        self.company_name = company_name
        self.isGDEStaff = is_staff
    
    def register_user(self):
        # check if the user is already on the application
        if self.user_already_added():
            return True
        else:
            try:
                # password = data['validated_password']
                # set the default password for all users, this is not their AD password
                User.objects.create_user(self.user_email, self.user_email, self.password)
                user = User.objects.get(email=self.user_email)
                user.username = self.user_name
                user.user_role = self.user_role
                user.client_name = self.company_name
                user.isGDEStaff = self.is_staff

                user.save()
                return True
            except Exception as e:
                print(e)
                return False

    def user_already_added(self):
        try:
            user = User.objects.get(email=self.user_email)
            return True
        except Exception as e:
            print(e)
            return False
