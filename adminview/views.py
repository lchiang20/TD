from django.shortcuts import render
from TutoringDragons.tutorview.models import *

# Create your views here.
def adminview(request):


def rptSearch(keyword):
    rptLst = Session.objects.all()
    ##Two dimensional array that stores sentence with keyword and the primary key of the Session (idpair + date)
    result = []
    for i in rptLst:
        rpt = i.progressreport
        ## Split sentence
        sentences = splitSentence(rpt)
        ## Extracts words
        extract = wordinSentence(sentences, keyword)
        result.append([extract, rptLst[i], rptLst[i].idpair])



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




