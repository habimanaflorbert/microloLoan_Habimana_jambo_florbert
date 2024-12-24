
from accounts.models import User



class IsEndUser():
    message = "You are not the end user"
    
    def has_permission(self, request, view):
        if request.user.user_type==User.END_USER:
            return True
        else:
            return False



class IsAdmin():
    message = "You are not the admin"
    
    def has_permission(self, request, view):
        if request.user.user_type==User.ADMIN:
            return True
        else:
            return False
    
