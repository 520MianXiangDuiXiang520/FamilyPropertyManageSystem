from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    """
    普通用户权限
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True


class ParentPermission(BasePermission):
    message = '您没有访问该接口的权限（You do not have access to the interface）'

    def has_permission(self, request, view):
        """
        先根据用户信息找到他对应的家庭，然后再看这个用户是不是这个家庭的家长
        虽然目前一个用户只能对应一个家庭，可以在家庭成员表中直接判断，但。。。
        """
        # 如果用户都没有家庭，他肯定不具有家长权限
        if not request.user.family1:
            return False
        family_number = request.user.family1.family_member
        for parent_field in ['parent1', 'parent2']:
            parent = getattr(family_number, parent_field)
            if parent:
                return request.user.id == parent.id
        return False

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True
