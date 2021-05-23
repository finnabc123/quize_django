from django.shortcuts import render, get_object_or_404
from .models import Quiz, Question, Response, Payment, ContactUsForm
from .forms import UserForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.core.paginator import Paginator
from django.utils import timezone
from collections import OrderedDict
import json
import operator
import razorpay

# Create your views here.

client = razorpay.Client(
    auth=("rzp_test_uCzWnrEymDyUU5", "yyeXf6bd5iCt2zciiRhBAGB3"))


def index(request):
    quiz = Quiz.objects.all()[::-1]
    paginator = Paginator(quiz, 3)
    page_number = request.GET.get('page')
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'quiz': quiz}
    return render(request, 'index.html', context=context)

    # print(quiz)


class QuizList(generic.ListView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'index.html'


@login_required(login_url='/login/')
def question(request, id):
    quiz = Quiz.objects.get(pk=id)
    question = quiz.question_set.all()
    paginator_list = question
    paginator = Paginator(paginator_list, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    response = Response.objects.filter(quiz=quiz)
    leaderboard = Response.objects.filter(quiz=quiz)
    payment = Payment.objects.filter(quiz=quiz)
    leader_dict = {}
    # time_taken = []
    # for res in response:
    #     print(res)
    for users in leaderboard:
        # print(users,users.scores)

        leader_dict[str(users)] = [str(users.scores), str(users.time_taken)]
    leaderboard_ordered = []
    print(leader_dict)
    for name, value in leader_dict.items():
        score = value[0]
        if len(leaderboard_ordered) == 0:
            leaderboard_ordered.append(name)

        for index, ordered_name in enumerate(leaderboard_ordered):
            ordered_name_score = leader_dict[ordered_name][0]

            if float(score) > float(ordered_name_score):
                leaderboard_ordered.insert(index, name)
                break
        if not name in leaderboard_ordered:
            leaderboard_ordered.append(name)

    dict_ordered = OrderedDict(
        (rank+1, (name, leader_dict[name])) for rank, name in enumerate(leaderboard_ordered))
    # print(dict_ordered)

    # sorted_dict = dict( sorted(leader_dict.items(),
    #                        key=lambda item: item[1],
    #                        reverse=True))

    # print(sorted_dict)

    # for key, value in isPaid.items():
    #     print(key,value)
    # print(quiz.free_quiz)
    users_taken = []
    amount = quiz.quiz_price
    # print(payment)
    for username in response:
        users_taken.append(str(username))

    user_paid = []

    for userpaid in payment:
        user_paid.append(str(userpaid.user))
    # print(user_paid)

    if quiz.free_quiz == True:
        if str(request.user) in users_taken:  # Checks weda user has taken the quiz
            # return leader board if user take
            return render(request, 'question.html', {'quiz': quiz, 'question_list': page_obj, 'isTaken': response, 'leader': dict_ordered})
        else:
            # return question pages if not
            return render(request, 'question.html', {'quiz': quiz, 'question_list': page_obj})

    else:
        if str(request.user) in user_paid:  # Checks weda user pay for the quiz
            if str(request.user) in users_taken:  # Checks weda user has taken the quiz
                # return leader board if user take
                return render(request, 'question.html', {'quiz': quiz, 'question_list': page_obj, 'isTaken': response, 'leader': dict_ordered})
            else:
                # return question pages if not
                return render(request, 'question.html', {'quiz': quiz, 'question_list': page_obj})
        else:  # User hasnt made the payment
            if request.method == 'POST':
                name = request.POST.get('name')
                #amount = quiz.quiz_price

                client = razorpay.Client(
                    auth=("rzp_test_uCzWnrEymDyUU5", "yyeXf6bd5iCt2zciiRhBAGB3"
                          ))

                payment = client.order.create({
                    'amount': amount, 'currency': 'INR',
                    'payment_capture': '1'
                })
                print(payment)
                print('post request initiated for payment')
                if payment:
                    new_payment = Payment(
                        user=request.user, quiz=quiz, isPaid=True)
                    new_payment.save()
                    return render(request, 'question.html', {'quiz': quiz, 'question_list': page_obj})
                return render(request, 'order.html', {'quiz': quiz, 'question_list': page_obj, 'amount': amount})
            return render(request, 'order.html', {'quiz': quiz, 'question_list': page_obj, 'amount': amount})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('landing_page'))


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('landing_page'))
            else:
                return HttpResponse('Acount Not Active')
        else:
            return render(request, 'login.html', context={'error': 'Invalid Login Details, Try Again'})
    else:

        return render(request, 'login.html', context={})


def register(request):
    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()
            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request, 'signup.html',
                  {'user_form': user_form,
                           'registered': registered})


def google_login(request):
    return render(request, 'google.html')


def leaderBoard(request):
    return render(request, 'leaderboard.html', context={})


def answer(request, id):
    quiz = Quiz.objects.get(pk=id)
    print(quiz)
    if request.method == 'POST':
        print('post sdsdsd initiated')
        scores = request.POST.get('my_scores')
        # scores = request.POST.get('individual_scores')
        time_taken = request.POST.get('time_taken')
        # print(time_taken)
        # print(scores)
        response = Response(user=request.user, quiz=quiz,
                            scores=scores, isTaken=True, time_taken=time_taken)
        response.save()


def create_order(request):
    if request.method == 'POST':
        print('post request initiated')

    return render(request, 'order.html', {})


def success(request):
    return render(request, 'success.html')


def about(request):
    return render(request, 'about.html')


def faqs(request):
    return render(request, 'faqs.html')


def contact(request):
    if request.method == 'POST':
        print('post sdsdsd initiated')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('secondname')
        email = request.POST.get('email')
        text = request.POST.get('text')
        print(firstname, lastname, email, text)
        contact_form = ContactUsForm(
            first_name=firstname, last_name=lastname, email=email, text=text)
        contact_form.save()
        return render(request, 'contact.html', context={'isSubmit': 'True'})
    return render(request, 'contact.html')


def responsible_gaming(request):
    return render(request, 'responsible_gaming.html')
