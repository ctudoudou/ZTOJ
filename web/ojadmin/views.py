from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from app.models import Problem, Users, Example, Competition
from app.tasks import problem_add

import datetime

# Create your views here.


def admin(request):
    try:
        request.session['user']
    except KeyError:
        return HttpResponseRedirect('/login/')
    return render(request, 'admin/admin.html')


def add_problem(request):
    if request.method == 'GET':
        return render(request, 'admin/create_problem.html')
    elif request.method == 'POST':
        name = request.session['email']
        user = Users.objects.get(email=name)
        title = request.POST.get('title', '')
        explain = request.POST.get('my-editormd-html-code', '')
        cinput = request.POST.get('cinput')
        coutput = request.POST.get('coutput')
        sinput = request.POST.get('sinput')
        soutput = request.POST.get('soutput')
        hint = request.POST.get('hint')
        source = request.POST.get('source')
        public = request.POST.get('public')
        label = request.POST.get('label')
        problem = Problem(email=user, title=title, description=explain, cinput=cinput, coutput=coutput, sinput=sinput,
                          soutput=soutput,
                          hint=hint, source=source, public=public, label=label).save()
        return redirect('add_problem')
    return render(request, 'admin/create_problem.html')


def problem_list(request):
    problems = Problem.objects.filter(public=1)
    return render(request, 'admin/problem_list.html', {'problems': problems})


def problem_add_example(request, id=None):
    try:
        request.session['email']
    except KeyError:
        return HttpResponseRedirect('/login/')
    request.session['pid'] = id

    if request.method == 'POST':
        problem = Problem.objects.filter(problem_id=request.session['pid'])[0]
        language = request.POST.get('language')
        code = request.POST.get('code', '')
        sin = request.POST.get('sinput')
        sout = request.POST.get('soutput')
        sample = '{\"s\":{\"s1\":\"' + sin + '\"}}'  # {"s": {"s1": sin}}
        Example(problem=problem, language=language, code=code, sample=sample).save()
        example = Example.objects.filter(problem=problem, language=language, code=code, sample=sample)[0]
        del request.session['pid']
        # problem_add.delay(example.id, language, code, sample)
        problem_add(example.id, language, code, sample)
        return HttpResponse('提交成功，请关闭窗口'.encode())
    return render(request, 'admin/problem_add.html')


def add_contest(request):
    try:
        request.session['email']
    except KeyError:
        return HttpResponseRedirect('/login/')
    if request.method == 'GET':
        return render(request, 'admin/create contest.html')
    elif request.method == 'POST':
        user = Users.objects.get(email=request.session['email'])
        competition_name = request.POST.get('title')
        explain = request.POST.get('my-editormd-html-code')
        start_time = request.POST.get('starttime')
        stop_time = request.POST.get('stoptime')
        password = request.POST.get('password')
        contest = Competition(email=user, competition_name=competition_name, description=explain, passwd=password,
                          start_time=start_time, stop_time=stop_time).save()

        return redirect('add_contest')
    return render(request, 'admin/create contest.html')

def contest_list(request):
    contests = Competition.objects.all()
    return render(request, 'admin/contest_list.html', {'contests': contests})
