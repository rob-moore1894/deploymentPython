from django.db import models
import re
import bcrypt

# Create your models here.
class userManager(models.Manager):
    def regValidator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['first_name']) == 0:
            errors['fnamereq'] = 'Register: First name is required'
        if len(postData['last_name']) == 0:
            errors['lnamereq'] = 'Register: Last name is required'
        if len(postData['email']) == 0:
            errors['emailreq'] = 'Register: Email is required'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Register: Invalid email address!"
        else:
            repeatEmail = Users.objects.filter(email = postData['email'])
            if len(repeatEmail) > 0:
                errors['emailTaken'] = "Register: This email is already in use"
        if len(postData['password']) < 4:
            errors['pwreq'] = 'Register: Password must contain at least 4 characters'
        if postData['password'] != postData['confirmPassword']:
            errors['nomatchpw'] = 'Register: Passwords must match'
        return errors

    def loginValidator(self, postData):
        print(postData)
        errors = {}
        userByEmail = Users.objects.filter(email=postData['emailLogin'])
        if len(postData['emailLogin']) == 0:
            errors['emailReq'] = "Login: Please enter your email"
        elif len(userByEmail) == 0:
            errors['noEmailExists'] = "Login: Email is not registered"
        else: 
            user = userByEmail[0]
            if bcrypt.checkpw(postData['passwordLogin'].encode(), userByEmail[0].password.encode()):
                print('Passwords Match')
            else: 
                errors['wrongPw'] = "Login: Incorrect Password"
        return errors
    
    def quoteValidator(self, postData):
        print(postData)
        errors ={}
        if len(postData['author']) < 3:
            errors['authorError'] = "Author must have more than 3 characters"
        if len(postData['quote']) < 10:
            errors['quoteError'] = "Quote must have more than 10 characters"
        return errors

    def updateValidator(self, postData):
        print(postData)
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['newFname']) == 0:
            errors['newFnameReq'] = "Please enter a new First Name"
        if len(postData['newLname']) == 0:
            errors['newLnameReq'] = "Please enter a new Last Name"
        if len(postData['newEmail']) == 0:
            errors['newEmailReq'] = "Please enter a new Email"
        elif not EMAIL_REGEX.match(postData['newEmail']):
            errors['newEmailInvalid'] = "Invalid email address!"
        else:
            repeatEmail = Users.objects.filter(email = postData['email'])
            if len(repeatEmail) > 0:
                errors['emailTaken'] = "This email is already in use"
        return errors

class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()

class Quotes(models.Model):
    author = models.CharField(max_length=255, default="Anonymous")
    content = models.TextField()
    uploader = models.ForeignKey(Users, related_name="quotes_uploaded", on_delete = models.CASCADE)
    favoriters = models.ManyToManyField(Users, related_name="quotes_favorited")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)