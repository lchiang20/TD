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
        request.session['email'] = email
        return render(request, 'index.html', {'logged' : True})
    else:
        email = request.POST.get('email')
        return render(request, 'index.html', {'logged':False})



def adminview(request):
    studentLst = Student.objects.all()
    tutorLst = Tutor.objects.all()
    sessionLst = []
    search = request.POST.get('search')

    if request.method == 'POST':
        searchType = request.POST.get('searchby')
        ## Student name
        if searchType == "0":
            searchedLst = []
            for i in studentLst:
                if search in i.firstname or search in i.lastname:
                    searchedLst.append(i.idstudent)

            ## Gets all pair id of the requested students
            requestedPair = []
            for i in searchedLst:
                for j in Pair.objects.filter(idstudent__exact=i):
                    requestedPair.append(j)

            for i in Session.objects.all():
                if i.idpair in requestedPair:
                    sessionLst.append(i)
            return render(request, 'adminview.html',
                          {'sessions': sessionLst})

        ## Tutor name
        if searchType == '1':
            searchedLst = []
            for i in tutorLst:
                if search in i.firstname or search in i.lastname:
                    searchedLst.append(i.idtutor)

            ## Gets all pair id of the requested tutors
            requestedPair = []
            for i in searchedLst:
                for j in Pair.objects.filter(idtutor__exact=i):
                    requestedPair.append(j)

            for i in Session.objects.all():
                if i.idpair in requestedPair:
                    sessionLst.append(i)

            return render(request, 'adminview.html',
                          {'sessions': sessionLst})

        ## Date
        if searchType == '2':
            if search.isnumeric():
                search = int(search.lstrip('0'))
                for i in Session.objects.all():
                    if search == i.date:
                        sessionLst.append(i)
                return render(request, 'adminview.html',
                              {'sessions': sessionLst})
            else:
                return render(request, 'adminview.html',
                              {'sessions': sessionLst})

        print("This is the search", search)

        ## Content
        if searchType == '3':
            print("it's running correctly")
            searchedLst = rptSearch(search)
            print("This is searched list", searchedLst)

            print("This is session: ", sessionLst)

            return render(request, 'adminview.html',
                          {'sessions': searchedLst[1]})


        else:
            for i in Session.objects.all():
                sessionLst.append(i)
            list.reverse(sessionLst)
        return render(request, 'adminview.html', {'sessions': sessionLst})
    else:
        for i in Session.objects.all():
            sessionLst.append(i)
        list.reverse(sessionLst)
    return render(request, 'adminview.html', {'sessions': sessionLst})

# i change some thing here to run success your code with student view

def studentview(request):
    ## TEST VALUE
    email = request.session.get('email')
    tutor = Tutor.objects.filter(email__icontains = email)[0].idtutor
    pairSelect = Pair.objects.filter(idtutor__exact = tutor)
    studentLst = []
    
    #check of user is admin
    if Tutor.objects.filter(pk=tutor)[0].admin == 1:
        admin = True
    else:
        admin = False

    for i in pairSelect:
        perStudent = Student.objects.filter(pk = i.idstudent.idstudent)
        studentLst.append(perStudent[0])

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
            coopChange = updateCS(int(coop), int(student))
            profChange = updatePS(int(prof), int(student))
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

    score1 = Student.objects.filter(idstudent__exact = student)[0].coopscore1
    score2 = Student.objects.filter(idstudent__exact = student)[0].coopscore2
    score3 = Student.objects.filter(idstudent__exact = student)[0].coopscore3

    newScore = newScore + 40

    oldAvg = (score1+score2+score3)/3
    ## updates average and cumulative change
    newAvg = (score2+score3+newScore)/3
    coopChange = newAvg - oldAvg
    ## making updates
    Student.objects.filter(pk=student).update(coopscore1 = newScore)
    Student.objects.filter(pk=student).update(coopscore2 = score1)
    Student.objects.filter(pk=student).update(coopscore3 = score2)

    return coopChange

def updatePS(newScore, idstudent):
    '''updates the current proficiency score based on passed value'''
    base = 95
    oldScore = int(Student.objects.get(pk=idstudent).profscore)
    ## creates base value
    if oldScore == 0:
        oldScore = 100
    result = 0.4*(base+int(newScore)) + 0.6*(oldScore)
    print(newScore)
    profChange = result - oldScore
    Student.objects.filter(pk=idstudent).update(profscore = result)
    return profChange


def rptSearch(keyword):
    '''

    :param keyword: string
    :return: two lists, one with the outstanding sentence, the other with the sessions
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
        if extract != []:
            reports.append(extract)
            key.append(i)

    return reports, key



def splitSentence(rpt):
    '''
    Takes any given string and returns a list where each element is a sentence from the original string
    '''
    endPunct = ['.', '!', '?']
    indices = [0]
    rpt = rpt + "."
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
    print('sentences: ', sentences)
    result = []
    for i in sentences:
        if word in i:
            result.append(i)
    return result



