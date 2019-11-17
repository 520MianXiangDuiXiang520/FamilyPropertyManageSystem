from rest_framework.permissions import BasePermission


class CommonPermission(BasePermission):
    """
    普通用户权限，作用于全局
    """
    def has_permission(self, request, view):
        print(request.user)
        if request.user.user_type == 1:
            return True

    def has_object_permission(self, request, view, obj):
        """
        一旦获得View权限，将获得所有object权限
        :return: True
        """
        return True


class VipPermission(BasePermission):
    """
    VIP 用户权限
    """
    message = '您首先要称为VIP才能访问'

    def has_permission(self, request, view):
        print(request.user)
        if request.user.user_type == 2:
            return True

    def has_object_permission(self, request, view, obj):
        return True
