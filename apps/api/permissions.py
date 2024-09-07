from rest_framework.permissions import BasePermission, IsAuthenticated

from apps.users.models import Waiter, Cashier, Manager, Admin


class AllowAny(BasePermission):
    """ Allow any permission class"""
    message = 'Not allowed'

    def has_permission(self, request, view):
        return True


class IsWaiter(BasePermission):
    """ Waiter permission class"""
    message = 'Not a Waiter'

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        return Waiter.objects.filter(user__id=request.user.id).exists()


class IsCashier(BasePermission):
    """ Cashier permission class"""
    message = 'Not a Cashier'

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        return Cashier.objects.filter(user__id=request.user.id).exists()


class IsKitchen(BasePermission):
    """ IsKitchen permission class"""
    message = 'Not a Kitchen user'

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        return IsKitchen.objects.filter(user__id=request.user.id).exists()


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