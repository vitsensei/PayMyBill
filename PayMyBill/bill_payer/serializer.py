from copy import deepcopy
from datetime import datetime

from rest_framework import serializers
from .models import Company, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["name", "bsb", "account_num", "amount",
                  "created_date", "paid_date", "status"]

    def create(self, validated_data):
        data = deepcopy(validated_data)  # deepcopy just in case
        # this instance is used down the line
        user = self.context['request'].user
        company = user.company
        data["company_id"] = company.id
        data["created_date"] = datetime.now()

        return Payment.objects.create(**data)

    def update(self, instance, validated_data):
        # Don't allow to edit company id, payment id and created_date
        company = Company.objects.get(pk=instance.company_id)
        instance.name = company.name
        instance.bsb = validated_data.get("bsb", instance.bsb)
        instance.account_num = validated_data.get("account_num", instance.account_num)
        instance.amount = validated_data.get("amount", instance.amount)
        instance.paid_date = validated_data.get("paid_date", instance.paid_date)
        instance.status = validated_data.get("status", instance.status)

        instance.save()
        return instance


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["name", "bsb", "account_num", "signup_date"]

