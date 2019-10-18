from django.shortcuts import render
from .models import Student, Session, Tutor, Pair
from datetime import date
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template import RequestContext

from django.http import HttpResponse
# Create your views here.

def index(request):

    if request.POST:
        email = request.POST.get('email')
        print(email)
        request.session['email'] = email
        return render(request, 'index.html', {'logged' : True})
    else:
        print("AHHHHH")
        email = request.POST.get('email')
        print(email)
        return render(request, 'index.html', {'logged':False})



def adminview(request):
    studentLst = Student.objects.all()
    tutorLst = Tutor.objects.all()
    sessionLst = []
    search = request.POST.get('search')

    if request.method  == 'POST':
        searchType = request.POST.get('searchby')
        print(searchType)
        ## Student name
        if searchType == "0":
            searchedLst = []
            for i in studentLst:
                if search in i.firstname or search in i.lastname:
                    searchedLst.append(i.idstudent)
            print("list of student id's: ", searchedLst)


            ## Gets all pair id of the requested students
            requestedPair = []
            for i in searchedLst:
                for j in Pair.objects.filter(idstudent__exact=i):
                    requestedPair.append(j)

            print("list of pair id's: ", requestedPair)

            for i in Session.objects.all():
                if i.idpair in requestedPair:
                    sessionLst.append(i)
            return render(request, 'adminview.html', {'sessions': sessionLst, 'tutors': tutorLst, 'students': studentLst})

        ## Tutor name
        if searchType == '1':
            searchedLst = []
            for i in tutorLst:
                if search in i.firstname or search in i.lastname:
                    searchedLst.append(i.idtutor)
            print("list of student id's: ", searchedLst)

            ## Gets all pair id of the requested tutors
            requestedPair = []
            for i in searchedLst:
                for j in Pair.objects.filter(idtutor__exact=i):
                    requestedPair.append(j)

            print("list of pair id's: ", requestedPair)
            for i in Session.objects.all():
                if i.idpair in requestedPair:
                    sessionLst.append(i)
            return render(request, 'adminview.html', {'sessions': sessionLst, 'tutors': tutorLst, 'students': studentLst})

        ## Date
        if searchType == '2':
            search = int(search.lstrip('0'))
            for i in Session.objects.all():
                if search == i.date:
                    sessionLst.append(i)
            return render(request, 'adminview.html', {'sessions': sessionLst, 'tutors': tutorLst, 'students': studentLst})

        ## Content
        if searchType == '3':
            searchedLst = rptSearch(search)

            for i in Session.objects.all():
                for j in searchedLst[1]:
                    if i.pk == j[0] and i.idpair = j[1]:
                        sessionLst.append(i)

            return render(request, 'adminview.html', {'sessions': sessionLst, 'tutors': tutorLst, 'students': studentLst})


        else:
            for i in Session.objects.all():
                sessionLst.append(i)
            list.reverse(sessionLst)
        return render(request, 'adminview.html', {'sessions': sessionLst, 'tutors':tutorLst, 'students':studentLst})
    else:
        for i in Session.objects.all():
            sessionLst.append(i)
        list.reverse(sessionLst)
    return render(request, 'adminview.html', {'sessions': sessionLst, 'tutors':tutorLst, 'students':studentLst})

# i change some thing here to run success your code with student view
def studentview(request):
    ## TEST VALUE
    email = request.session.get('email')
    tutor = Tutor.objects.filter(email__icontains = 'lchiang20@ssis.edu.vn').first()
    print tutor.idtutor
    pairs = Pair.objects.filter(idtutor = tutor.idtutor)
    print pairs
    studentLst = []
    
    #check of user is admin
    if tutor.admin == 1:
        admin = True
    else:
        admin = False
    for pair in pairs:
        result = {}
        student = pair.idstudent
        tutor = pair.idtutor
        result['firstname'] = student.firstname
        result['lastname'] = student.lastname
        result['idstudent'] = student.idstudent

        # if u want to use info of tutor => u open comment
        # tutor = pair.idtutor
        # result['tutor_idtutor'] = tutor.idtutor
        # result['tutor_firstname'] = tutor.firstname

        studentLst.append(result)
    print studentLst

    if request.method == 'POST':
        if request.POST.get('profScore') and request.POST.get('idStudent')\
                and request.POST.get('coopScore') and request.POST.get('report'):
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
            if admin == True:
                return render(request, 'studentrpt.html', {'students': studentLst, 'admin': True})
            else:
                return render(request, 'studentrpt.html', {'students': studentLst, 'admin': False})
        else:
            if admin == True:
                return render(request, 'studentrpt.html', {'students': studentLst, 'admin': True})
            else:
                return render(request, 'studentrpt.html', {'students': studentLst, 'admin': False})
    else:
        if admin == True:
            return render(request, 'studentrpt.html', {'students' : studentLst, 'admin' :True})
        else:
            return render(request, 'studentrpt.html', {'students' : studentLst, 'admin' :False})

def renderRpt(studentLst, admin):
    if admin == True:
        return render(request, 'studentrpt.html', {'students': studentLst, 'admin': True})
    else:
        return render(request, 'studentrpt.html', {'students': studentLst, 'admin': False})

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

def rptSearch(keyword):
    '''

    :param keyword: string
    :return: two lists, one with the outstanding sentence, the other with primary key in form (idpair + date)
    '''
    rptLst = Session.objects.all()
    reports = []
    key = []
    for i in rptLst:
        rpt = i.progressreport
        ## Split sentence
        sentences = splitSentence(rpt)
        ## Extracts words
        extract = wordinSentence(sentences, keyword)
        reports.append(extract)
        key.append(rptLst[i], rptLst[i].idpair)
    return reports, key



def splitSentence(rpt):
    '''
    Takes any given string and returns a list where each element is a sentence from the original string
    '''
    endPunct = ['.', '!', '?']
    indices = [0]
    ## find indices of end punctuations
    for i in endPunct:
        ends = [j for j,  k in enumerate(rpt) if k == i]
        indices.extend(ends)
    indices.sort()

    ## splits the string by index locations
    sentences = []
    for i in range(len(indices) - 1):
        firstIndex = indices[i]
        secondIndex = indices[i+1]
        sentences.append(rpt[firstIndex:secondIndex+1])
    return sentences

def wordinSentence(sentences, word):
    '''
    :param sentence: list of sentences
    :return: list of sentence with the keywords in it
    '''
    result = []
    for i in sentences:
        if word in i:
            result.append(i)
    return result




