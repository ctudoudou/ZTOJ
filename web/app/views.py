from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse

from .forms import UserForm
from .models import Users, Problem, Competition, Submits, Example, CompetitionList
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

from app.tasks import problem_submit
import random
import string
import datetime
import json


# Create your views here.

def flash(request, title, text, level='error'):
    """
    利用django的message系统发送一个信息。
    """
    level_map = {
        'info': messages.INFO,
        'debug': messages.DEBUG,
        'success': messages.SUCCESS,
        'warning': messages.WARNING,
        'error': messages.ERROR
    }
    level = level_map[level]

    messages.add_message(request, level, text, extra_tags=title)
    return 'OK'


def index(request):
    problems = Problem.objects.filter(public=1)
    cons = Competition.objects.all()
    return render(request, 'index.html', {'page': 'index', 'login': 'login', 'problems': problems, 'contests': cons})


def problems(request):
    problems = Problem.objects.filter(public=1)
    return render(request, 'problems.html', {'page': 'problems', 'problems': problems})


def contests(request):
    cons = Competition.objects.all()
    return render(request, 'contests.html', {'page': 'contests', 'contests': cons})


def ranklist(request):
    return render(request, 'ranklist.html', {'page': 'ranklist'})


def do_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('email', '')
        password = request.POST.get('password', '')
        try:
            user = Users.objects.get(email=username)
        except:
            flash(request, '找不到该用户', '找不到该用户')
            return render(request, 'login.html')
        if user and check_password(password, user.password):
            request.session['user'] = str(user.jurisdiction)
            request.session['email'] = username
            return redirect('index')
        flash(request, '邮箱或密码输入错误', '邮箱或密码输入错误')
    return render(request, 'login.html')


def logout(request):
    try:
        request.session['user']
    except KeyError:
        return HttpResponseRedirect('/login/')
    del request.session['user']
    del request.session['email']

    return redirect('index')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        email = request.POST.get('email', None)
        username = request.POST.get('name', None)
        password = request.POST.get('password', None)
        try:
            Users.objects.get(email=email)
            flash(request, '用户已经注册', '用户已经注册')
            return redirect('register')
        except:
            user = Users(email=email, username=username, password=make_password(password, None, 'pbkdf2_sha256')).save()
            return redirect('login')
    return render(request, 'register.html', {'page': 'register'})


def rankist(request):
    pass


def contest(request, cn):
    try:
        request.session['email']
    except KeyError:
        return HttpResponseRedirect('/login/')
    contest = Competition.objects.get(competition_name=cn)
    user = Users.objects.get(email=request.session['email'])
    if request.method == 'POST':
        passwd = request.POST.get('passwd')
        if passwd == contest.passwd:
            CompetitionList(competition_name=contest, email=user).save()
        return redirect(request.get_full_path())
    if CompetitionList.objects.filter(competition_name=contest, email=user):
        problems = Problem.objects.filter(source=cn)
        email = request.session['email']
        submit = []
        rank = []
        users = CompetitionList.objects.all()
        ac = []
        total_time = []
        for i in users:
            try:
                ac.append(Submits.objects.filter(email=i.email, pass_field=1).count())
                times = Submits.objects.filter(email=i.email, pass_field=1)
                time = datetime.datetime.now() - datetime.datetime.now()
                for j in times:
                    time += (datetime.datetime.now() - contest.start_time)
                total_time.append(time)
            except:
                ac.append(0)
                total_time.append(datetime.datetime.max)
        temp = zip(total_time, users, ac)
        # TODO 排序逻辑可能有错
        ranking = sorted(sorted(temp, key=lambda x: (x[0])), key=lambda x: (x[2]), reverse=True)
        num = 0
        mingci = 0
        source = 0
        for i in ranking:
            num += 1
            if i[1].email.email == request.session['email']:
                mingci = num
                source = i[2]
        now = datetime.datetime.now()
        if contest.stop_time <= now:
            finish = 1
        else:
            finish = 0
        for i in problems:
            try:
                submit.append(Submits.objects.filter(problem=i, email=email, pass_field=1)[0])
                rank.append(Submits.objects.filter(problem=i, pass_field=1).order_by('create_time'))
            except:
                submit.append('')
                rank.append('')
        # TODO 排序去重
        result = zip(problems, submit, rank)
        return render(request, 'contest.html',
                      {'page': 'contests', 'list': result, "finish": finish, 'contest': contest,
                       'ranking': ranking, 'source': source, 'mingci': mingci})
    else:
        return render(request, 'confirm_contest.html')


def problem(request, id):
    try:
        request.session['email']
    except KeyError:
        return HttpResponseRedirect('/login/')
    problem = Problem.objects.get(problem_id=id)
    token = ''.join(random.sample(string.ascii_letters + string.digits, 50))
    # TODO  token有问题(测试)
    try:
        request.session['token']
    except:
        request.session['token'] = token
    if request.method == 'POST':
        email = Users.objects.get(email=request.session['email'])
        language = request.POST.get('language')
        content = request.POST.get('code')
        # TODO 128位
        Submits(token=str(request.session['token']), email=email, problem=problem, content=content, pass_field=0).save()
        temp = Submits.objects.get(token=str(request.session['token']))
        example = Example.objects.get(problem=problem)
        # TODO eval
        sample = eval(example.sample)
        sample = '{\"s\":{\"s1\":\"' + sample["s"]["s1"] + '\"}, \"r\":{\"s1\":\"' + example.stdout + '\"}}'
        result=problem_submit(temp.id, language, content, example.time, '', sample)
        del request.session['token']
        return render(request, 'problem.html', {'problem': problem, 'token': token, 'content': content,'result':result})
    return render(request, 'problem.html', {'problem': problem, 'token': None})



def personal(request):
    return render(request, 'personal.html')


def register_login(request):
    return render(request, 'register_login.html')


def profile(request):
    return render(request, 'profile.html')


def contest_rank(request, cn):
    contest = Competition.objects.get(competition_name=cn)
    users = CompetitionList.objects.all()
    ac = []
    total_time = []
    for i in users:
        try:
            ac.append(Submits.objects.filter(email=i.email, pass_field=1).count())
            times = Submits.objects.filter(email=i.email, pass_field=1)
            time = datetime.datetime.now() - datetime.datetime.now()
            for j in times:
                time += (j.create_time - contest.start_time)
            total_time.append(time)
        except:
            ac.append(0)
            total_time.append(datetime.datetime.max)
    temp = zip(total_time, users, ac)
    # TODO 排序逻辑可能有错
    ranking = sorted(sorted(temp, key=lambda x: (x[0])), key=lambda x: (x[2]), reverse=True)

    return render(request, 'contest_rank.html',
                  {'page': 'contestrank', 'ranking': ranking})


def api_goal(request, token):
    try:
        request.session['email']
    except KeyError:
        return
    try:
        submit = Submits.objects.filter(token=token, problem=problem)
        temp = {
            "pass": submit.pass_field,
        }
        data = json.dumps(temp, ensure_ascii=False)
        return HttpResponse(data, content_type="application/json")
    except:
        return
