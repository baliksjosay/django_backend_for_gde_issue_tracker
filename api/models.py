from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class Client(models.Model):
    id = models.BigAutoField(primary_key=True)
    location = models.CharField(max_length=250)
    client_name = models.CharField(max_length=250)
    client_contact = models.CharField(max_length=250)
    status = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'clients'

class User(AbstractUser):
    email = models.EmailField(primary_key=True)
    user_email = models.EmailField()
    # client_name = models.CharField(max_length=250)
    client_name = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    password = models.CharField(max_length=250)
    user_name = models.CharField(max_length=250)
    user_role = models.CharField(max_length=150)
    # isGDEstaff = models.CharField(max_length=150)
    # assignments = 
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    class Meta:
        db_table = 'users'


class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    project_name = models.CharField(max_length=250)
    project_description = models.CharField(max_length=250)
    # attachments = models.FileField(upload_to='projects')
    status = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'projects'

class ProjectClient(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'project_clients'

class IssueTicket(models.Model):
    id = models.BigAutoField(primary_key=True)
    number_of_people_impacted = models.CharField(max_length=250)
    project_with_issue = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    issue_title = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    urgency = models.CharField(max_length=250)
    priority_reason = models.CharField(max_length=250)
    submission_comments = models.CharField(max_length=250)
    issue_type = models.CharField(max_length=250)
    attachments = models.FileField(upload_to='issues')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=250)
    next_party = models.CharField(max_length=250)
    status_reason = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'issue_tickets'

class IssueComment(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    # project_with_issue = models.ForeignKey(Project, on_delete=models.CASCADE)
    issue = models.ForeignKey(IssueTicket, on_delete=models.CASCADE)
    comment = models.TextField(null=False)
    attachments_file = models.FileField(upload_to='issue_attachments', null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'issue_comments'


class EditLog(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    affected_column = models.CharField(max_length = 200, null=True)
    affected_project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    old_value = models.CharField(max_length=200, null=True)
    new_value = models.CharField(max_length=200, null=True)
    description = models.TextField()
    edit_by = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'edit_logs'



class PerformedAction(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    affected_project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    affected_issue = models.ForeignKey(IssueTicket, on_delete=models.CASCADE, null=True)
    performed_by = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'performed_actions'
