from copy import deepcopy
from datetime import datetime

from rest_framework import serializers
from .models import Company, Payment, Hook


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["name", "bsb", "account_num", "amount", "status"]

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
        instance.status = validated_data.get("status", instance.status)

        instance.save()
        return instance


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["name", "bsb", "account_num", "signup_date"]


class HookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hook
        fields = ["url"]

    def create(self, validated_data):
        data = deepcopy(validated_data)  # deepcopy just in case
        # this instance is used down the line
        user = self.context['request'].user
        company = user.company

        data["company_id"] = company.id
        return Hook.objects.create(**data)

    def update(self, instance, validated_data):
        instance.url = validated_data.get("url", instance.url)
        instance.is_subscribed_name = validated_data.get("is_subscribed_name", instance.is_subscribed_name)
        instance.is_subscribed_bsb = validated_data.get("is_subscribed_bsb", instance.is_subscribed_bsb)
        instance.is_subscribed_account_num = validated_data.get("is_subscribed_account_num", instance.is_subscribed_account_num)
        instance.is_subscribed_amount = validated_data.get("is_subscribed_amount", instance.is_subscribed_amount)
        instance.is_subscribed_status = validated_data.get("is_subscribed_status", instance.is_subscribed_status)

        instance.save()
        return instance
