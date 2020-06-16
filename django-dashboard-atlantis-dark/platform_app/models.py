from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    org_name = models.CharField(max_length=150)
    comm_address1 = models.TextField()
    comm_address2 = models.TextField()
    comm_country = models.CharField(max_length=150)
    comm_state = models.CharField(max_length=150)
    comm_city = models.CharField(max_length=150)
    comm_phone = models.BigIntegerField()
    comm_email = models.EmailField()
    comm_gstin = models.CharField(max_length=150)
    bill_address1 = models.TextField()
    bill_address2 = models.TextField()
    bill_country = models.CharField(max_length=150)
    bill_state = models.CharField(max_length=150)
    bill_city = models.CharField(max_length=150)
    bill_phone = models.BigIntegerField()
    bill_email = models.EmailField()
    bill_gstin = models.CharField(max_length=150)

    def __str__(self):
        return str(self.org_name)


class SubscriptionPlan(models.Model):
    plan = models.CharField(max_length=150)
    description = models.TextField()
    number_of_stakeholders = models.IntegerField()
    price = models.BigIntegerField()
    created = models.DateTimeField()
    validity = models.IntegerField()

    def __str__(self):
        return str(self.plan)


class Project(models.Model):
    organization = models.ForeignKey(Organization, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    start_date = models.CharField(max_length=200)
    end_date = models.CharField(max_length=200)
    duration = models.IntegerField(blank = True, null = True)
    subscribed_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, blank = True, null = True)
    razorpay_order_id = models.CharField(max_length = 100, null=True, blank= True)

    def __str__(self):
        return str(self.title)


class Card(models.Model):
    organization = models.ForeignKey(Organization, on_delete = models.CASCADE)
    card_number = models.BigIntegerField()
    name_on_card = models.CharField(max_length = 100)
    expiry_date = models.CharField(max_length=4)
    
    def __str__(self):
        return str(self.organization)
