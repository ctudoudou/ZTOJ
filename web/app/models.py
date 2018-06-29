# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Competition(models.Model):
    competition_name = models.CharField(primary_key=True, max_length=45)
    email = models.ForeignKey('Users', models.DO_NOTHING, db_column='email')
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField()
    passwd = models.IntegerField(blank=True, null=True)
    description = models.TextField()

    class Meta:
        db_table = 'competition'


class CompetitionHistory(models.Model):
    probelm = models.ForeignKey('Problem', models.DO_NOTHING)
    competition_name = models.ForeignKey(Competition, models.DO_NOTHING, db_column='competition_name')
    email = models.ForeignKey('Users', models.DO_NOTHING, db_column='email')
    pass_field = models.FloatField(db_column='pass')  # Field renamed because it was a Python reserved word.
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'competition_history'


class CompetitionList(models.Model):
    competition_name = models.ForeignKey(Competition, models.DO_NOTHING, db_column='competition_name')
    email = models.ForeignKey('Users', models.DO_NOTHING, db_column='email')

    class Meta:
        db_table = 'competition_list'


class Example(models.Model):
    problem = models.ForeignKey('Problem', models.DO_NOTHING)
    language = models.CharField(max_length=45)
    code = models.TextField()
    sample = models.TextField()
    stdout = models.TextField(blank=True, null=True)
    time = models.CharField(max_length=45, blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    memory = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'example'


class Forum(models.Model):
    competition_name = models.ForeignKey(Competition, models.DO_NOTHING, db_column='competition_name')
    email = models.ForeignKey('Users', models.DO_NOTHING, db_column='email')
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    likeint = models.IntegerField(default=0)
    hide = models.IntegerField(default=1)

    class Meta:
        db_table = 'forum'


class IntegralHistory(models.Model):
    integral = models.IntegerField()
    email = models.ForeignKey('Users', models.DO_NOTHING, db_column='email')
    create_time = models.DateTimeField(auto_now_add=True)
    operation = models.TextField()

    class Meta:
        db_table = 'integral_history'


class News(models.Model):
    id = models.IntegerField(primary_key=True)
    receive = models.CharField(max_length=45)
    send = models.CharField(max_length=45)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    read = models.IntegerField(default=0)

    class Meta:
        db_table = 'news'


class Organization(models.Model):
    organization_name = models.CharField(primary_key=True, max_length=45)
    email = models.ForeignKey('Users', models.DO_NOTHING, db_column='email')
    create_time = models.DateTimeField(auto_now_add=True)
    is_use = models.IntegerField(default=1)

    class Meta:
        db_table = 'organization'


class Problem(models.Model):
    problem_id = models.AutoField(primary_key=True)
    email = models.ForeignKey('Users', models.DO_NOTHING, db_column='email')
    title = models.CharField(max_length=45)
    description = models.TextField()
    cinput = models.TextField()
    coutput = models.TextField()
    sinput = models.TextField()
    soutput = models.TextField()
    hint = models.TextField()
    source = models.TextField()
    label = models.CharField(max_length=45)
    public = models.IntegerField(default=1)

    class Meta:
        db_table = 'problem'


class Submits(models.Model):
    token = models.CharField(unique=True, max_length=128)
    email = models.ForeignKey('Users', models.DO_NOTHING, db_column='email')
    problem = models.ForeignKey(Problem, models.DO_NOTHING)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    pass_field = models.FloatField(db_column='pass')  # Field renamed because it was a Python reserved word.
    similarity = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'submits'


class UserOriginization(models.Model):
    origanization_name = models.ForeignKey(Organization, models.DO_NOTHING, db_column='origanization_name')
    email = models.ForeignKey('Users', models.DO_NOTHING, db_column='email')
    creat_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_originization'


class Users(models.Model):
    email = models.CharField(primary_key=True, max_length=45)
    username = models.CharField(unique=True, max_length=45)
    password = models.CharField(max_length=90)
    school = models.CharField(max_length=45, blank=True, null=True)
    ip = models.CharField(max_length=45, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    jurisdiction = models.IntegerField(default=0)
    use = models.IntegerField(default=0)
    integral = models.IntegerField(default=0)
    image = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'users'
