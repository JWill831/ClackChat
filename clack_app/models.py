from django.db import models
from datetime import datetime
import re
import bcrypt

class UserManager(models.Manager):
    def r_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least 2 characters"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['password'] != postData['password_confirmation']:
            errors['password_confirmation'] = "Passwords do not match"
        # uniqueness [] or [{}...] check for length
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['email'] = "Email exists"
        # date in past
        # if datetime.strptime(postData['birthday'], '%Y-%m-%d') > datetime.today():
        #     errors['birthday'] = "Date must be in the past. DESTROY!"
        return errors
    def l_validator(self, postData):
        errors = {}
        if len(User.objects.filter(email=postData['login_email'])) == 0:
            errors['login_email'] = "Email does not exist"
        else:
            u = User.objects.filter(email=postData['login_email'])[0]
            if not bcrypt.checkpw(postData['login_password'].encode(), u.password.encode()):
                errors['login_password'] = "Invalid Password and Email Combination"
        return errors
    def a_validator(self, postData):
        errors = {}
        # if User.objects.admin_level==0:
        if len(User.objects.filter(email=postData['login_email'])) == 0:
            errors['login_email'] = "Email does not exist"
        else:
            u = User.objects.filter(email=postData['login_email'])[0]
            if u.admin_level==0:
                errors['login_not_admin']="You are not an admin!"
            
            if not bcrypt.checkpw(postData['login_password'].encode(), u.password.encode()):
                errors['login_password'] = "Invalid Password and Email Combination"

        return errors

class User(models.Model):
    # birthday = models.DateField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    user_name=models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    #Relationships?
    admin_level=models.BooleanField(default=False, null=True)
    objects = UserManager()
    
class Message(models.Model):
    user = models.ForeignKey(User, related_name='messages', on_delete = models.CASCADE)
    message = models.TextField()
    image=models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete = models.CASCADE)
    message = models.ForeignKey(Message, related_name='comments', on_delete = models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
# class Admin_manager(models.Manager):
#     def admin_validator(self, post_data):
#         admin_errors={}  
#         stored_userman=['KeebLord']
#         stored_password=['Fogtown831']
#         if post_data['admin_username'] not in stored_username:
#             admin_error['admin_username']="No admin access!"
#         if post_data['admin_password'] not in stored_password:
#             admin_error['admin_password']="No admin access!"
#         return errors
    
# class Admin(models.Model):
#         admin_username=models.CharField(max_length=255)
#         admin_password=models.CharField(max_length=255)
#         objects=Admin_manager()