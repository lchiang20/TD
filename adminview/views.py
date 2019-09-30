from django.shortcuts import render
from TutoringDragons.tutorview.models import *

# Create your views here.
def rptSearch(keyword, pair):
    rptLst = Session.objects.all()

    ##Two dimensional array that stores sentence with keyword and the primary key of the Session (idpair + date)
    for i in rptLst:
        rpt = i.progressreport
        if keyword in rpt:
            for letter in rpt:

def splitSentence(rpt):
    '''
    Takes any given string and returns a list where each element is a sentence from the original string
    '''
    endPunct = ['.', '!', '?']
    sentences = []
    indices = []
    ## find indices of end punctuations
    for i in endPunct:
        ends = [j for j,  k in enumerate(rpt) if k == i]
        indices.extend(ends)

    ## loops through paragraph and



