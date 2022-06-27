from django.db import models

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if not postData["first_name"]:
            errors["first_name"] = "Please enter your first name"
        elif len(postData['first_name']) < 2:
            errors["first_name"] = "first name should be at least 2 characters"
        if not postData["last_name"]:
            errors["last_name"] = "Please enter your last name"
        elif len(postData['last_name']) < 2:
            errors["last_name"] = "last name should be at least 2 characters"
        if not postData["password"]:
            errors["password"] = "Please enter password"
        elif postData["password"]  != postData["con-password"]:
            errors["password"] = "password don't match"
        elif len(postData['password']) < 8:
            errors["password"] = "password should be at least 8 characters"
        

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class BookManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if not postData["title"]:
            errors["title"] = "please enter book title"
        if not postData["desc"]:
            errors["desc"] = "please enter book description"
        elif len(postData["desc"]) < 5:
            errors['desc']= "book description should be at least 5 characters"
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, related_name= "book_uploaded",on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    objects = BookManager()

