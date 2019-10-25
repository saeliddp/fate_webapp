from django.shortcuts import render
from django.http import HttpResponse
from version2.extraction import *
from django.shortcuts import redirect
import random
# Create your views here.
first_algorithm = "t"
second_algorithm = "rp"
num_search_results = 5
# gets relevant data from snippet.pickle file
first_snippets = extractFromFile(first_algorithm + ".txt", num_search_results)
second_snippets = extractFromFile(second_algorithm + ".txt", num_search_results)
unseen_qids = []
num_qids_seen = 0

for qid in first_snippets:
    unseen_qids.append(qid)

def getRandomQid():
    new_qid = unseen_qids[random.randint(0, len(unseen_qids) - 1)]
    unseen_qids.remove(new_qid)
    return new_qid
    
def getNextQid():
    new_qid = unseen_qids[0]
    unseen_qids.remove(new_qid)
    return new_qid

def consent(request):
    return render(request, 'version2/consent.html')
    
def demographics(request):
    return render(request, 'version2/demographics.html')
    
def instructions(request):
    return render(request, 'version2/instructions.html')

def home(request):
    curr_qid = getRandomQid()
    context = {
        'first_snippets': first_snippets[curr_qid],
        'second_snippets': second_snippets[curr_qid],
        'query_name': first_snippets[curr_qid][0][0]
    }
    return render(request, 'version2/home.html', context);

def update(request):
    global num_qids_seen
    num_qids_seen += 1
    if (num_qids_seen < 20):
        # send data to server
        
        # redirect to home
        return redirect('version2-home')
    else:
        # should I reset unseen_qids and num_qids_seen here?
        return redirect('version2-thanks')
    
def thanks(request):
    return render(request, 'version2/thanks.html')
    
