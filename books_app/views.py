from multiprocessing import BoundedSemaphore
from django.shortcuts import render, redirect
from django.contrib import messages
from books_app.models import User, Book
import bcrypt

def index(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name=first_name, last_name=last_name,email= email, password=hash)
            
            request.session['userId'] = user.id         
            return redirect('/books')
    return render(request,'index.html')


def login(request):
    if request.method == "POST":
            email = request.POST["email"]
            password = request.POST["password"]
            try:
                user = User.objects.get(email=email)
                if bcrypt.checkpw(password.encode(), user.password.encode()):
                    request.session["userId"] = user.id
                return redirect('/books')
            except User.DoesNotExist:
                print("User does not exist")
    return redirect('/')

def logout(request):
    del request.session['userId']
    return redirect('/')

def books(request):
    user = User.objects.get(id=request.session["userId"])
    context = {
        "books": Book.objects.all(),
        "user": user
    }
    
    if request.method == "POST":
        errors = Book.objects.basic_validator(request.POST)
        print(errors)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')
        else:
            
            title = request.POST.get("title")
            desc = request.POST.get("desc")
            uploaded_by = User.objects.get(id =request.session['userId'])
            book = Book.objects.create(title=title, desc=desc, uploaded_by=uploaded_by)
            book = Book.objects.last()
            uploaded_by.liked_books.add(book)
            book.save()
        return redirect('/books')
            
    return render(request, 'books.html', context)

def view(request, bookId):
    context = {
        "book": Book.objects.get(id=bookId),
        "user" : User.objects.get(id=request.session["userId"]),
        "users_who_like_this": Book.objects.filter(users_who_like = request.session["userId"])
        
    }
    return render(request,'view.html', context)
    
def delete(request, bookId):
    Book.objects.get(id=bookId).delete()
    return redirect("/books")

def favorite(request, bookId):
    user = User.objects.get(id=request.session["userId"])
    book = Book.objects.get(id=bookId)
    user.liked_books.add(book)
    return redirect(f"/books/{bookId}")

def unfavorite(request, bookId):
    user = User.objects.get(id=request.session["userId"])
    book = Book.objects.get(id=bookId)
    book.users_who_like.remove(user)
    return redirect(f"/books/{bookId}")

def edit(request, bookId):
    if request.method == "GET":
        context = {
            "user" : User.objects.get(id=request.session["userId"]),
            "book": Book.objects.get(id=bookId)
        }
        return render(request, context, "edit.html")
    if request.method == "POST":
        book_to_update: Book.objects.get(id=bookId)
        book_to_update.desc = request.POST['desc']
        book_to_update.save()
        return redirect(f"/books/{bookId}")