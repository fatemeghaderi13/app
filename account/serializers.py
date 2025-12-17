# accounts/serializers.py
from rest_framework import serializers


class RequestOTPSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=11)


class VerifyOTPSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=6)
