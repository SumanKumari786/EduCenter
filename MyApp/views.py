from django.contrib import messages, auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from MyApp.models import Feedback, Question, Post
from .forms import *


def login(request):
    if request.method == 'POST':
        n = request.POST['name']
        pass1 = request.POST['pass']

        user = auth.authenticate(username=n, password=pass1)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('/register')
    else:
         return render(request, 'MyApp/login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    if request.method == 'POST':
        fn = request.POST['fname']
        ln = request.POST['lname']
        un = request.POST['usname']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        em = request.POST['email']

        if pass1 == pass2:

            if User.objects.filter(username=un).exists():
                messages.info(request, 'Username already Taken')
                return redirect('/register')
            elif User.objects.filter(email=em).exists():
                messages.info(request, 'Email already Taken')
                return redirect('/register')
            else:
                user = User.objects.create_user(first_name=fn, last_name=ln, username=un, password=pass1, email=em, )
                user.save()
                messages.info(request, 'You are register succesfully please LOGIN')
                return redirect('/login')
        else:
            messages.info(request, 'Password does not match')

        return redirect('/register')

    else:
        return render(request, 'MyApp/register.html')


@login_required(login_url='/login/')
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        msg = request.POST.get('message', '')
        feedback = Feedback(name=name, email=email, message=msg)
        feedback.save()
        messages.info(request, 'Thanks for your Valuable Feedback')
    return render(request, 'MyApp/contact.html')


def aboutus(request):
    return render(request, 'MyApp/About.html')


def galary(request):
    return render(request, 'MyApp/galary.html')


# Question Views
def home(request):
    ques = Question.objects.all()
    context = {'ques': ques}
    return render(request, "MyApp/AskQuesHome.html", context)


@login_required(login_url='/login/')
def create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, "MyApp/AskQuestion.html", context)


@login_required(login_url='/login/')
def chooseans(request, ques_id):
    ans = Question.objects.get(pk=ques_id)
    if request.method == 'POST':
        selected_option = request.POST['poll']
        if selected_option == 'option1':
            ans.option_one_count += 1
        elif selected_option == 'option2':
            ans.option_two_count += 1
        elif selected_option == 'option3':
            ans.option_three_count += 1
        else:
            return HttpResponse(400, 'invalid form')
        ans.save()

        return redirect('results', ans.id)
    context = {'ans': ans}
    return render(request, "MyApp/ViewQuestion.html", context)


@login_required(login_url='/login/')
def results(request, ques_id):
    ans = Question.objects.get(pk=ques_id)
    context = {'ans': ans}
    return render(request, "MyApp/ViewResults.html", context)


@login_required(login_url='/login/')
def view_profile(request):
    return render(request, "MyApp/View_Profile.html")


@login_required(login_url='/login/')
def update_profile(request):
    if request.method == 'POST':

       u_form = UserUpdate(request.POST, instance=request.user)
       p_form = ProfileUpdate(request.POST, request.FILES, instance=request.user.myprofile)

       if u_form.is_valid() and p_form.is_valid():
          u_form.save()
          p_form.save()
          messages.success(request, 'Your Profile is updated Successfully')
          return redirect('/view_profile')
       else:
           messages.error(request, 'Something wrong:')
    else:
       u_form = UserUpdate(instance=request.user)
       p_form = ProfileUpdate(instance=request.user.myprofile)
    context = {
       'u_form': u_form,
       'p_form': p_form
    }
    return render(request, "MyApp/Update_Profile.html", context)


@login_required(login_url='/login/')
def changePass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            v = form.save()
            update_session_auth_hash(request, v)
            messages.success(request, 'Your password change successfully')
    else:
        form = PasswordChangeForm(request.user)
    params = {
        'form': form,
    }
    return render(request, "MyApp/changePass.html", params)


@login_required(login_url='/login/')
def course(request):
    return render(request, "MyApp/courses.html")


def blog(request):
    return render(request, "MyApp/blog.html")


def html(request):
    return render(request, "MyApp/htmlcourse.html")


def htmldetails(request):
    return render(request, "MyApp/htmldetails.html")


def css(request):
    return render(request, "MyApp/csscourse.html")


def cssdetails(request):
    return render(request, "MyApp/cssdetails.html")


def js(request):
    return render(request, "MyApp/jscourse.html")


def boot(request):
    return render(request, "MyApp/bootcourse.html")


def python(request):
    return render(request, "MyApp/pythoncourse.html")


def django(request):
    return render(request, "MyApp/djangocourse.html")


@login_required(login_url='/login/')
def continuepost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = PostComment.objects.filter(post=post, reply=None)

    is_favourite = False

    if post.favourite.filter(id=request.user.id).exists():
        is_favourite = True

    if request.method == 'POST':
        commentform = CommentForm(request.POST or None)
        if commentform.is_valid():
            comment = request.POST.get('comment')
            reply_id = request.POST.get('comment_sno')
            comment_qs = None
            if reply_id:
                comment_qs = PostComment.objects.get(sno=reply_id)
            postcomment = PostComment.objects.create(post=post, user=request.user, comment=comment, reply=comment_qs)
            postcomment.save()
    else:
        commentform = CommentForm()

    context = {'post': post, 'comments': comments, 'commentform': commentform, 'is_favourite': is_favourite}
    return render(request, "MyApp/continue.html", context)


class PostListView(ListView):
    model = Post
    template_name = 'MyApp/blog.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 1


@login_required(login_url='/login/')
def favourite_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.favourite.filter(id=request.user.id).exists():
        post.favourite.remove(request.user)
    else:
        post.favourite.add(request.user)
    return redirect('/favourite_post_list')


@login_required(login_url='/login/')
def post_favourite_list(request):
    user = request.user
    favourite_posts = user.favourite.all()
    context = {'favourite_posts': favourite_posts}
    return render(request, "MyApp/favourite.html", context)


@login_required(login_url='/login/')
def compiler(request):
    return render(request, "MyApp/compiler.html")


def search(request):
    query = request.GET['query']
    if len(query) > 50:
        posts = Post.objects.none()
    else:
        postsTitle = Post.objects.filter(title__icontains=query)
        postsCategory = Post.objects.filter(category__icontains=query)
        posts = postsTitle.union(postsCategory)
    if posts.count() == 0:
        messages.warning(request, 'No Search Results, Please Refine Your Query')
    params = {'posts': posts, 'query': query}
    return render(request, "MyApp/search.html", params)


def index(request):
    return render(request, "MyApp/index.html")
