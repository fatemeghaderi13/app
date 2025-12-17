# accounts/views.py
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from database.redis import set_data, get_data
from .serializers import RequestOTPSerializer, VerifyOTPSerializer
from .services import create_phone_otp


class RequestOTPAPIView(APIView):
    serializer_class = RequestOTPSerializer

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile_number']
        result = create_phone_otp(mobile)

        if not result["status"]:
            return Response({"message": "خطا در ارسال کد! مجدد تلاش کنید."}, status=status.HTTP_400_BAD_REQUEST)

        set_data(mobile, result["code"], ex=120)
        return Response({"message": "کد ارسال شد"}, status=status.HTTP_200_OK)


class VerifyOTPAPIView(APIView):
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile_number']
        code = serializer.validated_data['code']

        otp = get_data(mobile)

        if not otp or not otp == code:
            return Response({"error": "OTP invalid"}, status=400)

        user, created = get_user_model().objects.get_or_create(
            mobile_number=mobile
        )

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "is_new_user": created
        })
