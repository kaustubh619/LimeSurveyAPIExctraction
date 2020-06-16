from rest_framework import serializers
from .models import *


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = "__all__"

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = "__all__"


class ProjectPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['subscribed_plan','razorpay_order_id']