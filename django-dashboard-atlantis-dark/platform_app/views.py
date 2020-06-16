from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib.auth import authenticate, login
from .models import *
from django.forms.utils import ErrorList
# from .forms import LoginForm, SignUpForm
from datetime import datetime
# import razorpay
# import requests
from rest_framework import viewsets, generics, status
from .serializers import *
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.http import HttpResponse, Http404
from rest_framework.views import APIView
import razorpay
import requests

now = datetime.now()

@login_required(login_url="/login/")
def projects(request):
    try:
        org = Organization.objects.get(user=request.user.id)
        proj = Project.objects.filter(organization=org.id)
        print(proj)
        proj_id_list = []
        for x in proj:
            proj_id_list.append(x.id)
        context = {
            # "org": Organization.objects.get(user=request.user.id),
            # "subscriptions": Subscription.objects.filter(project__in=proj_id_list),
            # "project": proj
        }
        return render(request, "projects.html", {"project": proj})
    except:
        return render(request, "projects.html")


def create_project(request):
    try:
        org = Organization.objects.get(user = request.user)
        plans = SubscriptionPlan.objects.all()
        print(plans)
        return render(request, "create_project.html", {"org": org, "plans": plans})
    except:
        plans = SubscriptionPlan.objects.all()
        print(plans)
        return render(request, "create_project.html", {"plans": plans})


class CreateOrg(viewsets.ViewSet):
    def list(self, request):
        queryset = Organization.objects.all()
        serializer = OrganizationSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateProj(viewsets.ViewSet):
    def list(self, request):
        queryset = Project.objects.all()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectSubscription(APIView):
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectPlanSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        new_dict = dict(request.data)
        sub_id = new_dict['subscribed_plan']
        sub_price = SubscriptionPlan.objects.get(id=int(sub_id[0])).price
        client=razorpay.Client(auth=("rzp_test_2tx97L0V09FUM6","QOWTRaArqW2Gj8O6rUxtEVwR"))
        Data = {'amount':str(int(sub_price)*100),"currency":'INR',"receipt":'order_rcptid_11',"payment_capture":1}
        val = client.order.create(data=Data)
        order_id = val['id']
        new_dict['razorpay_order_id'] = order_id
        new_dict.update({'subscribed_plan':int(sub_id[0])})
        serializer = ProjectPlanSerializer(project, data=new_dict)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def addCard(request):
    context = {
        "sub": Project.objects.last()
    }
    return render(request, "card_deatils.html", context)

def payment_redirect(request):
    return render(request, "payment_redirect_page.html")

def postMEdetails(request, pk):
    project_obj = Project.objects.get(id=pk)

    API_ENDPOINT = "http://localhost:9000/register_user"

    data = {'username': request.user.username,
            'email':request.user.email,
            'title':project_obj.title,
            'summary': project_obj.description,
            'start': project_obj.start_date,
            'end': project_obj.end_date,
            'status': "New"            
            }

    r = requests.post(url = API_ENDPOINT, data = data)

    print(data)

    return redirect("/payment_redirect")