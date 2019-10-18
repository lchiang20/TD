from django.db import models


class Pair(models.Model):
    idpair = models.AutoField(db_column='idPair', primary_key=True)  # Field name made lowercase.
    idstudent = models.ForeignKey('Student', models.DO_NOTHING, db_column='idStudent')  # Field name made lowercase.
    idtutor = models.ForeignKey('Tutor', models.DO_NOTHING, db_column='idTutor')  # Field name made lowercase.

    # add here code when u print u can see info detail of Pair
    def __unicode__(self):
        return "{}, {} {}".format(self.idpair, self.idstudent, self.idtutor)

    class Meta:
        managed = False
        db_table = 'Pair'
    

class SessionManager(models.Manager):
    def createSession(self, id, date, rpt, profchange, coopchange):
        session = self.update_or_create(idpair=id, date=date, progressreport=rpt, profchange=profchange, coopchange=coopchange)
        return session

class Session(models.Model):
    idpair = models.ForeignKey(Pair, models.DO_NOTHING, db_column='idPair')  # Field name made lowercase.
    date = models.IntegerField(primary_key=True)
    progressreport = models.TextField(db_column='progressReport')  # Field name made lowercase.
    profchange = models.IntegerField(db_column='profChange')  # Field name made lowercase.
    coopchange = models.IntegerField(db_column='coopChange')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Session'
        unique_together = ('date', 'idpair')

    objects = SessionManager()


class Student(models.Model):
    idstudent = models.AutoField(db_column='idStudent', primary_key=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName', max_length=50)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=45)  # Field name made lowercase.
    email = models.CharField(max_length=45)
    absences = models.IntegerField()
    profscore = models.IntegerField(db_column='profScore')  # Field name made lowercase.
    coopscore = models.IntegerField(db_column='coopScore')  # Field name made lowercase.
    parentemail = models.CharField(db_column='parentEmail', max_length=45, blank=True, null=True)  # Field name made lowercase.
    teacher = models.CharField(max_length=45)
    # u need add more field to show any field u want
    def __unicode__(self):
        return "{}, {} {}".format(self.idstudent, self.firstname, self.lastname)
    class Meta:
        managed = False
        db_table = 'Student'


class Tutor(models.Model):
    idtutor = models.AutoField(db_column='idTutor', primary_key=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName', max_length=50)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=45)  # Field name made lowercase.
    email = models.CharField(max_length=45)
    admin = models.IntegerField()
    def __unicode__(self):
        return "{}, {} {} {}".format(self.idtutor, self.firstname, self.lastname, self.email)
    class Meta:
        managed = False
        db_table = 'Tutor'


