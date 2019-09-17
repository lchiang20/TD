from django.shortcuts import render
from .models import Student, Session, Tutor, Pair
from datetime import date
from django.views.decorators.csrf import ensure_csrf_cookie


from django.http import HttpResponse
# Create your views here.


# Create your views here.
# @ensure_csrf_cookie
def tutorview(request):
    students = Student.objects.all() ## NEED TO RESTRAIN TO INDIVIDUAL TUTOR
    if request.method == 'POST':
        if request.POST.get('profScore') and request.POST.get('idStudent')\
                and request.POST.get('coopScore') and request.POST.get('report'):
            rpt = request.POST.get('report')
            coop = request.POST.get('coopScore')
            id = request.POST.get('idStudent')
            prof = request.POST.get('profScore')

            ### NEED TO GET TUTOR ID FOR VAR tutor BELOW
            #pair = getPairID(id, tutor)
            if updateRT(rpt, id) == "err":
                return render(request, 'studentrpt.html', {'students' : students})

            #updateCS(coop, pair)
            updatePS(prof, id)
            return render(request, 'studentrpt.html', {'students' : students})
        else:
            print('checking')
            return render(request, 'studentrpt.html', {'students': students})
    else:
        return render(request, 'studentrpt.html', {'students' : students})

def getPairID(student, tutor):
    '''queries database with student and tutor and returns the pair ID'''
    pair = Pair.objects.filter(idtutor__exact = tutor, idstudent__exact = student)[0].idpair
    return pair

def updateRT(rpt, id):
    '''
    attempts to update report based on entered information -- a query is made first to make
    sure that the current session doesn't exist.
    '''
    ddmmyyyy = date.today().strftime("%d%m%Y")
    if Session.objects.filter(idpair__exact = id, date__exact = ddmmyyyy).exists() == True:
        return "err"

    return None

def updateCS(newScore, id):
    '''updates new cooperation score based on passed value'''

    oldScore = Student.objects.filter(idstudent__exact = id)[0].profscore
    if len(str(oldScore)) < 9:
        current = '100100100'
    ## gets last three numbers
    num_1 = int(current[6:9].lstrip('0'))
    ## gets middle three numbers
    num_2 = int(current[3:6].lstrip('0'))
    ## gets first three numbers
    num_3 = int(current[0:3].lstrip('0'))
    oldAvg = (num_1+num_2+num_3)/3

    ## updates score /w new input
    result = str(95+int(newScore)) + current[:-3]
    ## updates average and cumulative change
    newAvg = (num_2+num_3+int(newScore))/3
    profChange = newAvg - oldAvg
    ## making updates
    Student.objects.filter(pk=id).update(coopscore = result)

    #    Student.objects.filter(idstudent__exact = id)[0].coopscore = result
#    Student().save()
    return

def updatePS(newScore, id):
    '''updates the current proficiency score based on passed value'''
    student = Student()
    base = 45
    oldScore = int(Student.objects.get(pk=id).profscore)
    ## creates base value
    if oldScore == 0:
        oldScore = 100
    result = 1.8*(base+int(newScore)) + 0.2*(oldScore/2)
    print(newScore)
    cpChange = result - oldScore

    ## save to database
    #    Session.coopchange = cpChange
    #    Session.save()

    ## save to database
#    Session.profchange = profChange
#    Session.save()
    Student.objects.filter(pk=id).update(profscore = result)
    return

