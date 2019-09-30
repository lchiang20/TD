from django.shortcuts import render
from .models import Student, Session, Tutor, Pair
from datetime import date
from django.views.decorators.csrf import ensure_csrf_cookie


from django.http import HttpResponse
# Create your views here.


# Create your views here.
# @ensure_csrf_cookie
def tutorview(request):
    ## TEST VALUE
    tutor = 2
    pairSelect = Pair.objects.filter(idtutor__exact = tutor)
    studentLst = []
    for i in pairSelect:
        perStudent = Student.objects.filter(pk = i.idstudent.idstudent)
        studentLst.append(perStudent[0])

    if request.method == 'POST':
        if request.POST.get('profScore') and request.POST.get('idStudent')\
                and request.POST.get('coopScore') and request.POST.get('report'):
            #email = request.session('email')
            rpt = request.POST.get('report')
            coop = request.POST.get('coopScore')
            student = request.POST.get('idStudent')
            prof = request.POST.get('profScore')
            pair = getPairID(student, tutor)

            ### NEED TO GET TUTOR ID FOR
            # VAR tutor BELOW
            coopChange = updateCS(coop, student)
            profChange = updatePS(prof, student)
            updateSession(rpt, pair, profChange, coopChange)
            return render(request, 'studentrpt.html', {'students' : studentLst})
        else:
            return render(request, 'studentrpt.html', {'students': studentLst})
    else:
        return render(request, 'studentrpt.html', {'students' : studentLst})

def getPairID(student, tutor):
    '''queries database with student and tutor and returns the pair ID'''
    pair = Pair.objects.filter(idtutor__exact = tutor, idstudent__exact = student)[0].idpair
    return pair

def updateSession(rpt, pair, profchange, coopchange):
    '''
    attempts to update report based on entered information -- a query is made first to make
    sure that the current session doesn't exist.
    '''
    ddmmyyyy = date.today().strftime("%d%m%Y")
    pairInstance = Pair(pk=pair)

    # insert into database
    try:
        Session.objects.update_or_create(idpair=pairInstance, date=ddmmyyyy, progressreport=rpt,
                                         profchange=profchange, coopchange=coopchange)
    except:
        sessionObj = Session.objects.filter(idpair = pair, date = ddmmyyyy)
        sessionObj.update(progressreport = rpt, profchange = profchange, coopchange = coopchange)
    print("SUCCESS")
    return None

def updateCS(newScore, student):
    '''updates new cooperation score based on passed value'''

    oldScore = Student.objects.filter(idstudent__exact = student)[0].coopscore
    if len(str(oldScore)) < 9:
        current = '100100100'
    else:
        current = str(oldScore)
    ## gets last three numbers
    num_1 = int(current[6:9].lstrip('0'))
    ## gets middle three numbers
    num_2 = int(current[3:6].lstrip('0'))
    ## gets first three numbers
    num_3 = int(current[0:3].lstrip('0'))
    oldAvg = (num_1+num_2+num_3)/3
    newScore = int(newScore) + 95
    ## updates score /w new input
    result = str(newScore) + current[:6]
    print(current)
    print(result)
    ## updates average and cumulative change
    newAvg = (num_2+num_3+newScore)/3
    profChange = newAvg - oldAvg
    print(num_1, num_2, num_3, oldAvg, newAvg, newScore, oldScore)
    ## making updates
    Student.objects.filter(pk=student).update(coopscore = result)
    return profChange

def updatePS(newScore, idstudent):
    '''updates the current proficiency score based on passed value'''
    base = 45
    oldScore = int(Student.objects.get(pk=idstudent).profscore)
    ## creates base value
    if oldScore == 0:
        oldScore = 100
    result = 1.8*(base+int(newScore)) + 0.2*(oldScore/2)
    print(newScore)
    cpChange = result - oldScore
    Student.objects.filter(pk=idstudent).update(profscore = result)
    return cpChange

