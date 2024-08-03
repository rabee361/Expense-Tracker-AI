from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from accounts.models import *

class IsVerified(BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs.get('pk', None)
        if pk is not None:
            user = CustomUser.objects.filter(id=pk).first()
            if user and not user.is_verified:
                raise PermissionDenied("الحساب غير مؤكد الرجاء تأكيد الحساب والمحاولة من جديد")
            return True
        else:
            return False





class HaveOTPCode(BasePermission):
    def has_permission(self, request, view):
        user_id = request.pk
        code_verification = OTPCode.objects.filter(user__id=user_id).first()
        if not code_verification:
            raise PermissionDenied("الرجاء طلب رمز التحقق والمحاولة من جديد")
        return True