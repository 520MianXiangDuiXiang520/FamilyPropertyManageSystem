# from familyManage.models import Family, FamilyMembers
# from messageManage.models import Message
# from userManage.models import User
#
#
#
# class GetInfo:
#     def __init__(self, data):
#         self.data = data
#
#     def get_info(self):
#         type_list = [User, Family, FamilyMembers, Message]
#         result = {}
#         for i in self.data._meta.fields:
#             get_info = getattr(self.data, i.name)
#             for type_check in type_list:
#                 if isinstance(get_info, type_check):
#                     # 递归
#                     pass
#                 else:


