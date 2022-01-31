from collections import UserList
from random import choice
from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from .models import Theme, Question, Choice, Comment, New_Question, Score 
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import admin
from django.urls import path
from django.contrib.auth.models import User


def theme(request):

    latest_theme_list = Theme.objects.order_by('id')
    # template = loader.get_template('quizz/index.html')
    context = {
        'authenticated':authenticated,
        'latest_theme_list': latest_theme_list,
    }
    # return HttpResponse(template.render(context, request))
    return render(request, 'quizz/theme.html', context)

def question(request, theme_id):
    theme_list = Theme.objects.order_by('id')
    nb_theme = len(theme_list)
    question_list = Question.objects.filter(theme=theme_id)
    context = {
        'theme_id': theme_id,
        'question_list': question_list,
        'authenticated':authenticated,
    }
    if request.method == 'GET':

        return render(request, 'quizz/question.html', context)
    if request.method == 'POST':
        # Selectionner tous les choix et les mettre en déselectionné
        nb_question = len(Question.objects.filter(theme=theme_id))
        for choice in Choice.objects.filter(theme=theme_id):
            choice.selected = False
            choice.save()

        score = 0

        # Liste de tous les choix sélectionnés
        list_selected_choice = []
        for question_id in range(1,nb_question+1):
            if request.POST.get(f'choice_id{question_id}'):
                list_selected_choice.append(request.POST.get(f'choice_id{question_id}'))
        
        for choice_id in list_selected_choice:
            choice_selected = Choice.objects.get(pk=choice_id)
            choice_selected.selected = True
            choice_selected.save()

        context["choice_selected"]=choice_selected
        
        for choice in Choice.objects.filter(theme=theme_id):
            if choice.selected == True and choice.votes == True:
                score += 1
        score = str(score) + "/" + str(nb_question)
        context["score"]=score
        theme_text= Theme.objects.get(pk=theme_id)
        theme_text=theme_text.theme_text 
        score= Score.objects.create(theme=theme_text, score=score, user=username)
        score.save()
        theme_suivant = theme_id + 1
        theme_precedant = theme_id - 1
        if theme_precedant != 0 :
            context["theme_precedant"]=theme_precedant
        if theme_id != nb_theme :
            context["theme_suivant"]=theme_suivant

        return render(request, 'quizz/results.html', context)

#def results(request, theme_id):
    #theme_list = Theme.objects.order_by('id')
    #nb_theme = len(theme_list)
    #question_list = Question.objects.filter(theme=theme_id)
    ##if theme_id == 1 and theme_id != nb_theme:
    #theme_suivant = theme_id + 1
    #    #theme_precedant = "Pas de theme précédant"
    ##if theme_id == nb_theme and theme_id != 1:
    ##    theme_precedant = theme_id - 1
    ##    theme_suivant = "Pas de theme suivant"
#
    #context = {
    #    'question_list': question_list,
    #    'theme_id': theme_id,
    #    'theme_suivant' : theme_suivant,
    #    #'theme_precedant' : theme_precedant
    #}
    #print(theme_suivant)

    #return render(request, 'quizz/results.html')#, context)

#def choice(request, question_id):
#    #question_list = Question.objects.filter(theme=theme_id)
#    choice_list = Choice.objects.filter(question=question_id)
#    context = {
#        #'question_list': question_list,
#        'choice_list': choice_list,
#    }
#    return render(request, 'quizz/choice.html', context)

def home(request):
    try:
        return render(request, 'quizz/home.html', {'authenticated':authenticated})
    except:
        return render(request, 'quizz/home.html')



from django.contrib.auth import authenticate, login


def newuser(request):
    if request.method == 'GET':
        return render(request, 'quizz/newuser.html')
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        new_password = request.POST.get('new_password')
        user = authenticate(username=new_username, password=new_password)
        if user is None:
            user = User.objects.create_user(new_username, '', new_password)
            user.save()
        else :
            return render(request, 'quizz/newuser.html', {"error": "L'utilisateur existe déjà."})
        return redirect('/quizz/loginuser')

def loginuser(request):
    global authenticated
    authenticated = False
    global user
    try:
        logout(request)
    except: 
        pass
    user = authenticate(username="username00000000000", password="password")

    if request.method == "GET":
        return render(request, 'quizz/loginuser.html')
    if request.method == "POST":
        global username
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        
        authenticated = user is not None

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('/admin') 
            else:
                login(request, user)
                return redirect('/quizz/theme')
                #return render(request, 'quizz/theme.html', {"user": user is not None}) 
        else:
            try:
                user_try=User.objects.filter(username=username).values()[0]["username"]
                return render(request, 'quizz/loginuser.html', {"error": "Le mot de passe est incorrect."}) 
            except:
                return render(request, 'quizz/loginuser.html', {"error": "Cet utilisateur n'éxiste pas."})


def score(request):
    try:
        score_list = Score.objects.all().filter(user=username)
    except:
        return render(request, 'quizz/erreur.html')
    theme_list = Theme.objects.order_by('id')
    #score_by_theme=[]
    score_by_theme = {}
    for theme in theme_list: 
        score_by_theme[theme]=score_list.filter(theme=theme.theme_text)
        #score_by_theme.append(score_list.filter(theme=theme.theme_text))

    context={"score_list":score_list, "score_by_theme":score_by_theme,'authenticated':authenticated}
    return render(request, 'quizz/score.html', context)

def contact(request):
    context = {"authenticated" : authenticated}
    if request.method == "GET":
        return render(request, 'quizz/contact.html', context)
    if request.method == "POST":
        comment_txt = request.POST.get('comment')
        question_txt = request.POST.get('question')
        comment = Comment.objects.create(comment=comment_txt)
        comment.save()
        question = New_Question.objects.create(question=question_txt)
        question.save()

        if comment_txt != "" or question_txt !="":
            context["message"] = "Vos requêtes ont bien été transmises à l'administration!"
        else: 
            context["message"] = "Veuillez renseigner un des champs."
        
        return render(request, 'quizz/contact.html', context) 
    