from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from chat.models import User

class MyAdapter(DefaultSocialAccountAdapter):
    def populate_user(self,request,sociallogin,data):
        
        super().populate_user(request,sociallogin,data)
        user_exists = User.objects.filter(email=data['email'])
        if not user_exists:
            is_admin = data['email'] in ['sforrego@uc.cl', 'sbehrmann@uc.cl', 'seorregom@gmail.com']
            user = User(email=data['email'],username=data['first_name']+' '+data['last_name'],is_admin=is_admin)
            user.save()


