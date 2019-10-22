from django.shortcuts import render
from django.db.models import Q
from django.core.mail import send_mail
from api.email_notifications import EmailNotification

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_jwt.utils import jwt_payload_handler

from api.serializers import GetClient, GetProject, GetIssues, PutIssueComment, PutPerformedAction, PutProjectClient
# from api import support_functions as SupportFunctions

from api.models import User, Project, Client, IssueTicket, ProjectClient
import datetime, json
from _datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt

class ClientList(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (AllowAny, )
    def post(self, request, format=None):
        # authentication = SupportFunctions.get_authentication_details(request)
        data = request.data.dict()
        
        rd = Client(
            client_name = data['client_name'].title(),
            client_contact = data['client_contact'],
            location = data['location'],
        )
        
        try: 
            rd.save()
            response = {
                'status': 200,
                'message': 'The new Client has been added successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'status': 400,
                'message': 'Something went wrong on our side. Please try again'
            }
            return Response(response, status=status.HTTP_200_OK)
        finally:
            try:
                dnp = ActionPerformed(rd.pk, data['user_id'], 'Added new client', 'New client logged')
                dnp.save()
                
            except:
                pass

    def get(self, request, format=None):
        client_status = request.GET.get('status')
               
        if client_status == 'All':
            clients = Client.objects.all()
            clients = GetClient(clients, many=True)
            return Response(clients.data, status = status.HTTP_200_OK)  

        if client_status != 'Search':
            clients = Client.objects.all()
            clients = GetClient(clients, many=True)
            return Response(clients.data, status = status.HTTP_200_OK)    
        
        if client_status == 'search':
            clients = Client.objects.all()
            client_name = request.GET.get('client_name')
            client_id = request.GET.get('client_id')
            client_location = request.GET.get('client_location')

            if not client_id == None and len(client_id) > 0:
                clients = clients.filter(id = client_id)
            else:
                if not client_name == None and len(client_name) > 0:
                    clients = clients.filter(client_name__icontains = client_name)
                if not client_location == None and len(client_location) > 0:
                    clients = clients.filter(location__icontains = client_location)
                                  
            clients = GetClient(clients, many=True)
            return Response(clients.data, status = status.HTTP_200_OK)


class ProjectList(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (AllowAny, )
    def post(self, request, format=None):
        # authentication = SupportFunctions.get_authentication_details(request)
        data = request.data.dict()
        
        rd = Project(
            project_name = data['project_name'].title(),
            project_description = data['project_description'],
            # attachments = data['attachments'],
        )
        
        try: 
            rd.save()
            response = {
                'status': 200,
                'message': 'The new Project has been added successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'status': 400,
                'message': 'Something went wrong on our side. Please try again'
            }
            return Response(response, status=status.HTTP_200_OK)
        finally:
            try:
                dnp = ActionPerformed(rd.pk, data['user_id'], 'Added new project', 'New project logged')
                dnp.save()
            except:
                pass

    def get(self, request, format=None):
        project_status = request.GET.get('status')
        print(project_status)
               
        if project_status == 'All':
            projects = Project.objects.all()
            print('get details')
            projects = GetProject(projects, many=True)
            return Response(projects.data, status = status.HTTP_200_OK)        

        if project_status != 'search':
            projects = Project.objects.filter(status = project_status)
            projects = GetProject(projects, many=True)
            return Response(projects.data, status = status.HTTP_200_OK)
        
        if project_status == 'search':
            projects = Project.objects.all()
            client_name = request.GET.get('client_name')
            project_name = request.GET.get('project_name')
            project_id = request.GET.get('tickect_id')

            if not project_id == None and len(project_id) > 0:
                projects = projects.filter(id = project_id)
            else:
                if not project_name == None and len(project_name) > 0:
                    projects = projects.filter(project_name__icontains = project_name)
                if not client_name == None and len(client_name) > 0:
                    projects = projects.filter(client_name__icontains = client_name)
                                  
            projects = GetProject(projects, many=True)
            return Response(projects.data, status = status.HTTP_200_OK)

class ProjectClient(APIView):
    permission_classes = (AllowAny, )
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, format=None):
        # authentication = SupportFunctions.get_authentication_details(request)
        data = request.data.dict()

        post_data = {
            'project': data['project_id'],
            'client': data['client_id'],
        }           
        rc = PutProjectClient(data = post_data)

        if rc.is_valid():
            rc.save()
            try:
                response = {
                    'status': 200,
                    'message': 'The project client has been added successfully'
                }
                return Response(response, status=status.HTTP_200_OK)    
            except Exception as e:
                print(e)
                response = {
                    'status': 400,
                    'message': 'Something went wrong on our side. Please try again'
                }
                return Response(response, status=status.HTTP_200_OK)       
        else:
            print('ooops')
            print(rc.errors)
            response = {
                'status': 400,
                'message': 'Something went wrong on our side. Please try again'
            }
            return Response(response, status=status.HTTP_200_OK)


class IssuesList(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (AllowAny, )
    def post(self, request, format=None):
        
        # authentication = SupportFunctions.get_authentication_details(request)
        data = request.data.dict()
        
        rd = IssueTicket (
            number_of_people_impacted = data['number_of_people_impacted'].title(),
            project_with_issue = Project.objects.get(project_name = data['project_name']),
            issue_title = data['issue_title'],
            description = data['description'],
            urgency = data['urgency'],
            attachments = data['attachments'],
            priority_reason = data['priority_reason'],
            submission_comments = data['submission_comments'],
            issue_type = data['issue_type'],
            next_party = 'Admin',
            status = 'New',
            status_reason = 'New Issue Recorded',
            added_by = User.objects.get(username = data['user_id'])
        )
        
        try: 
            rd.save()
            response = {
                'status': 200,
                'message': 'The new Issue has been added successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'status': 400,
                'message': 'Something went wrong on our side. Please try again'
            }
            return Response(response, status=status.HTTP_200_OK)
        finally:
            try:
                dnp = ActionPerformed(rd.pk, data['user_id'], 'Added new issue ticket', 'New issue ticket logged', None)
                dnp.save()
                print('saved action')
            except:
                pass
        # EmailNotification('New Issue has been logged', "Please login to the issue tracker", 'gdexpertsug@gmail.com').send()

    def get(self, request, format=None):
        issue_status = request.GET.get('status')
               
        if issue_status == 'All':
            issues = IssueTicket.objects.all()
            issues = GetIssues(issues, many=True)
            return Response(issues.data, status = status.HTTP_200_OK) 

        if issue_status != 'Search':
            issues = IssueTicket.objects.filter(status=issue_status)
            issues = GetIssues(issues, many=True)
            return Response(issues.data, status = status.HTTP_200_OK)    
        
        if issue_status == 'search':
            issues = Client.objects.all()
            client_name = request.GET.get('client_name')
            issue_id = request.GET.get('client_id')
            issue_name = request.GET.get('issue_name')
            user_name = request.GET.get('user_name')

            if not issue_id == None and len(issue_id) > 0:
                issues = issues.filter(id = issue_id)
            else:
                if not client_name == None and len(client_name) > 0:
                    issues = issues.filter(client_name__icontains = client_name)
                if not issue_name == None and len(issue_name) > 0:
                    issues = issues.filter(issue_title__icontains = issue_name)
                if not user_name == None and len(user_name) > 0:
                    issues = issues.filter(added_by__icontains = user_name)
                                     
            issues = GetIssues(issues, many=True)
            return Response(issues.data, status = status.HTTP_200_OK)


class IssueAction(APIView):
    permission_classes = (AllowAny, )
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, format=None):
        # authentication = SupportFunctions.get_authentication_details(request)
        data = request.data.dict()

        print(data)

        if data['attachment_file'] == "null":
            post_data = {
                
            # 'issue': IssueTicket.objects.get(issue_title = data['issue']),
            'issue': data['issue'],
            'comment': data['action_comments'],
            'assigned_to': data['assigned_to'],
            'user': User.objects.get(email = data['email'])
        } 
        else:
            post_data = {
                # 'issue': IssueTicket.objects.get(issue_title = data['issue']),
                'issue': data['issue'],
                'comment': data['action_comments'],
                'assigned_to': data['assigned_to'],
                'attachments_file': data['attachment_file'],
                'user': User.objects.get(email = data['email'])
            }           
        rc = PutIssueComment(data = post_data)

        if rc.is_valid():
            rc.save()
            try:
                response = {
                    'status': 200,
                    'message': 'Your action has been performed successfully'
                }
                return Response(response, status=status.HTTP_200_OK)
            finally:
                rq = IssueTicket.objects.get(pk=data['issue'])
                rq.status = data['action']
                rq.save()
                if data['action'] == 'Assigned':
                    # send out notifications
                    dnp = ActionPerformed(rq.pk, data['email'], 'Assigned ticket', 
                                            data['action_comments'],data['assigned_to'])
                    print('SAVING')
                    dnp.save()
                elif data['action'] == 'Closed':
                    dnp = ActionPerformed(rq.pk, data['email'], 'Issue closed',
                                          data['action_comments'], None)
                                            

                    dnp.save()
                elif data['action'] == 'Recieved':
                    dnp = ActionPerformed(rq.pk, data['email'], 'Issue is recieved, pending resolution',
                                          data['action_comments'], None)
                    dnp.save()
                elif data['action'] == 'Resolved':
                    dnp = ActionPerformed(rq.pk, data['email'], 'Issue has been resolved ',
                                          data['action_comments'], None)
                                        
                    dnp.save() 

        else:
            print('ooops')
            print(rc.errors)
            response = {
                'status': 400,
                'message': 'Something went wrong on our side. Please try again'
            }
            return Response(response, status=status.HTTP_200_OK)



class ActionPerformed:
    # EmailNotification('GDExperts Support Alert', "Please login to the issue tracker", 'gdexpertsug@gmail.com').send()
    def __init__(self, affected_issue, user_id, action_performed, status_reason, assigned_to, action_comments):
        # self.affected_project = affected_project
        self.affected_issue = affected_issue
        self.user_id = user_id
        self.action_performed = action_performed
        self.status_reason = status_reason
        self.assigned_to =  assigned_to
        # self.action_comments = action_comments
        self.body_string = """
            <head><style>table {
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
            }

            td, th {
            border: 1px solid black;
            text-align: left;
            padding: 8px;
            }

            tr:nth-child(even) {
            background-color: #dddddd;
            }
            </style></head>
            <h2>Hello, There is an update on the issue tracker</h2><br>
            
            <table border="2">
                <tr style = "background-color: yellow">
                    <th>Ticket Id</th>
                    <th>Added by</th>
                    <th>Urgency</th>
                    <th>Request Status</th>
                    <th>Status Reason</th>
                    <th>Action</th>
                </tr>
        """
        




    def save(self):
        print(self.assigned_to)
        pa = PutPerformedAction(
            data = {
                'affected_issue': self.affected_issue,
                'performed_by': self.user_id,
                'action': self.action_performed,
                'assigned_to': self.assigned_to
                # 'action_comments': self.action_comments
            }
        )
        if pa.is_valid():
            try:
                pa.save()

                return True
            except Exception as e:
                print(e)
                return False
            finally:
                print('determining the next party to attend to the request')
                self.determine_next_party()
        else:
            print(pa.errors)
            return False
                    
    def determine_next_party(self):
        """
        Determines the next party to handle the request
        """

        user_roles = ['Client', 'Admin', 'Support']
        
        req = IssueTicket.objects.get(pk = self.affected_issue)

        # attempt to send out the notification
        try:
            self.send_out_notification(req)
        except Exception as e:
            print(e)
            pass
        
        if req.status == 'New':
            req.next_party = user_roles[1]
            req.save()
            return True
        elif req.status == 'Assigned':
            req.status_reason = self.status_reason
            req.next_party = user_roles[2]
            req.save()
        elif req.status == 'Recieved':
            req.next_party = user_roles[2]
            req.save()
            return True
        elif req.status == 'Resolved':
            req.status_reason = self.status_reason
            req.next_party = user_roles[1]
            req.save()
        
        elif req.status == 'Closed':
            req.next_party = 'Closed'
            req.status_reason = self.status_reason
            req.save()
            return True
        else:
            # find the index of the current next_party and increase
            current_party = user_roles.index(req.next_party)
            req.next_party = ''
            req.status_reason = self.status_reason
            req.save()
            return True
    def send_out_notification(self, request_object):
        data = """<tr>
            <td>"""+str(request_object.id)+"""</td>
            <td>"""+str(request_object.added_by)+"""</td>
            <td>"""+str(request_object.urgency)+"""</td>
            <td>"""+str(request_object.status)+"""</td>
            <td>"""+str(request_object.status_reason)+"""</td>            
            <td>"""+str(self.action_performed)+"""</td>            
            </tr>
        """
        try:
            son = SupportFunctions.Notification(
                ['joseph.balikuddembe@gdexperts.com'],
                ['joseph.balikuddembe@gdexperts.com'],
                ['joseph.balikuddembe@gdexperts.com'],
                'Issue Ticket Notification',
                self.body_string + data
            )
            son.send_notification()
            return True
        except Exception as e:
            print(e)
            return False


class GetStatusCount(APIView):
    def get(self, request, format=None):
        # the possible request statuses
        statuses = [
            'New', 
            'Resolved',
            'Recieved', 
            'Assigned',
            'Pending', 
            'Closed',            
            'Rejected'
        ]
        counter = {}
        for x in statuses:
            no = IssueTicket.objects.values('id').filter(status=x).count()
            counter.update({x:no}) 

              
        # counter = str(counter)

        clients_number = Client.objects.values('id').count()
        counter.update({'Clients_number':clients_number})
        projects_number = Project.objects.values('id').count()
        counter.update({'Projects_number':projects_number})

        # support_users_number = User.objects.values('is_staff').count()
        # counter.update({'Support_users_number':support_users_number})
        # client_user_number = User.objects.values('Client').count()
        # counter.update({'Client_users_number':client_users_number})

        user_number = User.objects.values('email').count()
        counter.update({'Users_number':user_number})
        return Response(json.dumps(counter), status=status.HTTP_200_OK)