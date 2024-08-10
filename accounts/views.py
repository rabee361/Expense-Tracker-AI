from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.permissions import *
from .serializers import *
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from utils.email import *
from utils.permissions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView , RetrieveAPIView , ListCreateAPIView , ListAPIView , RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404


class SignUpView(APIView):
    def post(self, request):
        user_information = request.data
        serializer = SignUpSerializer(data=user_information)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        user_data = serializer.data
        user = CustomUser.objects.get(email=user_data['email'])
        code = generate_code()
        # email_body = 'Hi '+user.username+' Use the code below to verify your email \n'+ str(code)
        data= {'to_email':user.email, 'email_subject':'Verify your email','username':user.username, 'code': str(code)}
        send_email(data)
        OTPCode.objects.create(user=user, code=code) ## generate code for user
        token = RefreshToken.for_user(user)
        tokens = {
            'refresh':str(token),
            'accsess':str(token.access_token)
        }
        return Response({'information_user':user_data,'tokens':tokens})




class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.get(email = request.data['username'])
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['id'] = user.id
        data['image'] = request.build_absolute_uri(user.image.url)
        data['tokens'] = {'refresh':str(token), 'access':str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)



# logout
class LogoutView(APIView):
    permission_classes = (IsAuthenticated, IsVerified,)
    def post(self, request):
        serializer = UserLogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)





##### verify account with generated code #####
class VerifyOTPView(APIView):
    permission_classes = (HaveOTPCode,)

    def post(self, request, pk):
        code = request.data['code']
        user = CustomUser.objects.get(id=pk)
        code_ver = OTPCode.objects.filter(user=user.id).first()
        if code_ver:
            if str(code) == str(code_ver.code):
                if timezone.now() > code_ver.expires_at:
                    return Response({"message":"لقد انتهت صلاحية كود التحقق"}, status=status.HTTP_400_BAD_REQUEST)
                user.is_verified = True
                user.save()
                code_ver.delete()
                return Response({"message":'تمت عملية التحقق بنجاح', 'user_id':user.id},status=status.HTTP_200_OK)
            else:
                return Response({'message':'الرمز خاطئ, يرجى إعادة إدخال الرمز بشكل صحيح'})




##### Reset Password for user ######
class GetOTPCodeView(APIView):
    def post(self, request):
        email = request.data['email']
        try: 
            user = get_object_or_404(CustomUser, email=email)
            existing_code = OTPCode.objects.filter(user=user).first()
            if existing_code:
                existing_code.delete()
            code_verification = generate_code()
            data= {'to_email':user.email, 'email_subject':'Verify your email','username':user.username, 'code': str(code_verification)}
            send_email(data)
            code = OTPCode.objects.create(user=user, code=code_verification)
            return Response({'message':'تم ارسال رمز التحقق',
                                'user_id' : user.id})
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'error':'pleace enter valid email'})
    


# End Points For Verified Account To Reset Password
class VerifyAccountView(APIView):
    permission_classes = (HaveOTPCode, IsVerified,)
    
    def post(self, request, pk):
        code = request.data['code']
        user = CustomUser.objects.get(id=pk)
        code_ver = OTPCode.objects.filter(user=user.id).first()
        if code_ver:
            if str(code) == str(code_ver.code):
                if timezone.now() > code_ver.expires_at:
                    return Response({"message":"لقد انتهت صلاحية كود التحقق"}, status=status.HTTP_400_BAD_REQUEST)
                code_ver.is_verified = True
                code_ver.save()
                return Response({"message":"تم التحقق من الرمز", 'user_id':user.id},status=status.HTTP_200_OK)
            else:
                return Response({'message':'الرمز خاطئ, يرجى إعادة إدخال الرمز بشكل صحيح'})
        

# End Points For Reset Password
class ResetPasswordView(UpdateAPIView):
    permission_classes = (IsVerified,HaveOTPCode,)
    queryset = CustomUser.objects.all()
    serializer_class = ResetPasswordSerializer

    def get_permissions(self):
        self.request.pk = self.kwargs.get('pk')
        return super().get_permissions()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['pk']=self.kwargs.get('pk')
        return context
    


##### get user profile information #####
class ListUserInformationView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.all()
    serializer_class= CustomUserSerializer



class UpdateImageUserView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.all()
    serializer_class = UpdateUserInfoSerializer




class UserAccount(ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


