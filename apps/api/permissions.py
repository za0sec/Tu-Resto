from rest_framework.permissions import BasePermission, IsAuthenticated

from apps.users.models import Manager, Admin, BranchStaff


class AllowAny(BasePermission):
    """ Allow any permission class"""
    message = 'Not allowed'

    def has_permission(self, request, view):
        return True


class IsManager(BasePermission):
    """ IsManager permission class"""
    message = 'Not a Manager'

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        return Manager.objects.filter(user__id=request.user.id).exists()


class IsAdmin(BasePermission):
    """ IsAdmin permission class"""
    message = 'Not an Admin'

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        return Admin.objects.filter(user__id=request.user.id).exists()


class IsBranchStaff(BasePermission):
    """ IsBranchStaff permission class"""
    message = 'Not a Branch Staff'

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        return BranchStaff.objects.filter(user__id=request.user.id).exists()