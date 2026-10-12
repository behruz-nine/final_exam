from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import SignUpSerializer, UPdateUserPropertiesSerializer, TransactionSerializer
from rest_framework.response import Response
from datetime import datetime
from .models import CODE_VERIFY, NEW, DONE
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

class SignUpView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = SignUpSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
class VerifyView(APIView):
    def post(self, request):
        code = request.data.get('code')
        user = request.user
        codes = user.codes.all().filter(code = code, used = False, expired_time__gte = datetime.now()).first()

        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFY
            codes.used = True

        user.save()
        codes.save()
        return Response(
            {
                'msg': 'Kod muvaffaqiyatli saqlandi',
                'code status': codes.used
            }
        )
    
class UpdateUserPropertiesView(APIView):
    def post(self, request):
        serializer = UPdateUserPropertiesSerializer(instance = request.user, data = request.data,  partial = True)
        if serializer.is_valid():
            serializer.save()
            user = request.user
            if user.auth_status == CODE_VERIFY:
                user.auth_status = DONE
            user.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

class TransactionView(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data = request.data, context = {'request': request})
        if serializer.is_valid():
            serializer.save(user = request.user)
            request.user.refresh_from_db(fields=['balance'])
            return Response(serializer.data)
        return Response(serializer.errors)
    

class TokenRefreshView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        refresh_t = request.data.get('refresh_token')
        refresh_token = RefreshToken(refresh_t)
        return Response(
            {
                "access_token": str(refresh_token.access_token)
            }
        )