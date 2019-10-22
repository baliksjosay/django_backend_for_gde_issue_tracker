from rest_framework import serializers
from api.models import User, Client, Project, PerformedAction, IssueTicket, IssueComment, ProjectClient
from Issue_tracker.settings import DOMAIN


class PutClient(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('__all__')

class PutProject(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('__all__')

class PutIssueComment(serializers.ModelSerializer):
    class Meta:
        model = IssueComment
        fields = ('__all__')

class PutProjectClient(serializers.ModelSerializer):
    class Meta:
        model = ProjectClient
        fields = ('__all__')

class GetProjectClient(serializers.ModelSerializer):
    client_projects = serializers.SerializerMethodField()
    class Meta:
        model =ProjectClient
        fields = ('__all__')


class PutIssue(serializers.ModelSerializer):
    class Meta:
        model = IssueTicket
        fields = ('__all__')

class GetUsers(serializers.ModelSerializer):
    audit_trail = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('__all__')
    def get_audit_trail(self, assigned_to_id):
        pas = PerformedAction.objects.filter(assigned_to = assigned_to_id.pk)
        pas = PutPerformedAction(pas, many=True)
        return pas.data

class GetIssue(serializers.ModelSerializer):
    audit_trail = serializers.SerializerMethodField()
    class Meta:
        model = IssueTicket
        fields = ('__all__')
    def get_audit_trail(self, issue):
        pas = PerformedAction.objects.filter(affected_issue = issue.pk)
        pas = PutPerformedAction(pas, many=True)
        return pas.data



class GetClient(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('__all__')

class GetProjectClient(serializers.ModelSerializer):
    client = GetClient(read_only=True)
    class Meta:
        model = ProjectClient
        fields = ('__all__')

class GetProject(serializers.ModelSerializer):
    attachments = serializers.SerializerMethodField()
    activity_log = serializers.SerializerMethodField()
    client_details = serializers.SerializerMethodField() #GetProjectClient(read_only=True)
    project_issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('__all__')
    def get_attachments(self, req):
        try:
            return DOMAIN + "/media/" + str(req.attachments)
        except:
            return None
    def get_activity_log(self, req):
        pas = PerformedAction.objects.filter(affected_issue = req.pk)
        pas = PutPerformedAction(pas, many=True)
        return pas.data
    def get_project_issues(self, req):
        rcs = IssueTicket.objects.filter(project_with_issue = req.pk)
        rcs = GetIssue(rcs, many=True)
        return rcs.data
    def get_client_details(self, req):
        gcd = ProjectClient.objects.filter(client_id = req.pk)
        gcd = GetProjectClient(gcd, many=True)
        return gcd.data


class GetIssues(serializers.ModelSerializer):
    project_with_issue = serializers.SerializerMethodField()
    audit_trail = serializers.SerializerMethodField()
    class Meta:
        model = IssueTicket
        fields = ('__all__')
    def get_project_with_issue(self, req):
        rcs = Project.objects.filter(project_name = req.pk)
        rcs = GetProject(rcs, many=True)
        return rcs.data
    def get_audit_trail(self, issue):
        pas = PerformedAction.objects.filter(affected_issue = issue.pk)
        pas = PutPerformedAction(pas, many=True)
        return pas.data


class PutPerformedAction(serializers.ModelSerializer):
    class Meta:
        model = PerformedAction
        fields = ('__all__')

class GetAction(serializers.ModelSerializer):
    class Meta:
        model = PerformedAction
        fields = ('__all__')

