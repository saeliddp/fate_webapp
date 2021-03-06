from django.shortcuts import render
from django.http import HttpResponse
from version2.extraction import *
from django.shortcuts import redirect
from version2.models import *
import random

num_search_results = 5
# algorithms to be initially displayed on the left and right, respectively
left_alg = "0g"
right_alg = "01gfp"
# algorithms to be displayed on left and right after 10 turns
round_one_l = "0g"
round_one_r = "01gfp"
round_two_l = "05gfp"
round_two_r = "09gfp"

# maps algorithm names to lists of snippets
alg_to_snippets = {
    left_alg: extractFromFile(round_one_l + ".txt", num_search_results),
    right_alg: extractFromFile(round_one_r + ".txt", num_search_results),
    round_two_l: extractFromFile(round_two_l + ".txt", num_search_results),
    round_two_r: extractFromFile(round_two_r + ".txt", num_search_results)
}

# whether or not to swap the left and right algorithms on a given turn
swap = [False, True, True, False, True, True, True, False, False, False, False, False, True, True, False, False, True, False, True, True]
unseen_qids = []
num_qids_seen = 0
curr_qid = 0
respondent = None

for qid in alg_to_snippets[left_alg]:
    unseen_qids.append(qid)
def reset():
    global unseen_qids
    global num_qids_seen
    global curr_qid
    global left_alg
    global right_alg
    unseen_qids = []
    for qid in alg_to_snippets[left_alg]:
        unseen_qids.append(qid)
    curr_qid = 0
    num_qids_seen = 0

def getRandomQid():
    new_qid = unseen_qids[random.randint(0, len(unseen_qids) - 1)]
    unseen_qids.remove(new_qid)
    return new_qid
    
def getNextQid():
    new_qid = unseen_qids[0]
    unseen_qids.remove(new_qid)
    return new_qid

def consent(request):
    reset()
    return render(request, 'version2/consent.html')
    
def demographics(request):
    if 'age' in request.GET:
        global respondent
        """ Uncomment for database action
        respondent = Respondent(
            age=request.GET['age'],
            gender=request.GET['gender'],
            education=request.GET['education'])
        respondent.save()
        """
        return redirect('version2-instructions')
    else:
        return render(request, 'version2/demographics.html')
    
def instructions(request):
    return render(request, 'version2/instructions.html')

def home(request):
    global curr_qid
    curr_qid = getNextQid()
    print("Left: " + left_alg)
    print("Right: " + right_alg)
    context = {
        'left_snippets': alg_to_snippets[left_alg][curr_qid],
        'right_snippets': alg_to_snippets[right_alg][curr_qid],
        'query_name': alg_to_snippets[right_alg][curr_qid][0][0]
    }
    return render(request, 'version2/home.html', context);

def update(request):
    global num_qids_seen
    global curr_qid
    global left_alg
    global right_alg
    global num_responses
    
    num_qids_seen += 1
    if (num_qids_seen <= 20):
        # send data to server
        # we will have to have a 'None' algorithm in our database to represent 
        # if the user didn't choose at all
        choice = 'None'
        not_choice = 'None'
        if 'radio' in request.GET:
            if request.GET['radio'] == 'left':
                choice = left_alg
                not_choice = right_alg
            else:
                choice = right_alg
                not_choice = left_alg

        print("User chose: " + choice)
        # Uncomment for database action
        response = Response(respondent=respondent,
                            query=Query.objects.filter(query_id=curr_qid)[0],
                            chosen_alg=Algorithm.objects.filter(name=choice)[0],
                            unchosen_alg=Algorithm.objects.filter(name=not_choice)[0],
                            time_elapsed=int(request.GET['time_elapsed']))
        response.save()
        
        if num_qids_seen == 10:
            print("Switching to second and third")
            left_alg = round_two_l
            right_alg = round_two_r
            
        if swap[num_qids_seen - 1]:
            print("Swapping")
            temp = left_alg
            left_alg = right_alg
            right_alg = temp
            
        # redirect to home
        if num_qids_seen < 20:
            return redirect('version2-home')
        else:
            return redirect('version2-thanks')
    else:
        return redirect('version2-thanks')

def thanks(request):
    return render(request, 'version2/thanks.html')
    
