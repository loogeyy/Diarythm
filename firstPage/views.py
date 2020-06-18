import numpy
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import joblib
import pickle

# Create your views here.

# pickle_in = open("./models/model.pickle", "rb")
# reloadModel = pickle.load(pickle_in)
reloadModel = joblib.load('./models/model.pickle')  # references model

'''
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html) #returns current time
    '''


# index page - HttpRequest object is created and returns an HttpResponse content (i.e. webpage, redirect, error)
def index(request):
    context = {'a': 'Hello World!'}
    # return HttpResponse(context) returns template and displays index.html page -> context is unique value that can
    # be passed onto the website using {{}} in index.html  i.e. {{a}} -> Hello World
    return render(request, 'index.html', context)


# what is displayed on the screen indicated by context will be different for diff instantiations, but index will
# still run
def predictGrade(request):
    print(request)  # POST '/predictGrade'
    if request.method == 'POST':
        # print('Hello World') #Hello World is printed, indicating that it is a POST method
        # print(re,quest.POST.dict())  #shows the token, and input variable values from index.html form
        temp = {'studytime': request.POST.get('studyVal'), 'failures': request.POST.get('failVal'),
                'freetime': request.POST.get('freetimeVal'), 'absences': request.POST.get('absentVal'),
                'G1': request.POST.get('firstVal'), 'G2': request.POST.get('secondVal')}  # creates dictionary
        userInput = list(temp.values()) # converts dictionary to list
        new = numpy.array(userInput) # converts to numpy array
        new = new.reshape(1, -1) # reshapes so it can be fit into model
        new = pd.np.asarray(new, dtype='float64') # converts each element into a float
        print(new)
        new[0][4] /= 5 # scales G1
        new[0][5] /= 5 # scales G2
        scoreVal = reloadModel.predict(new)*5  # uses imported model to predict value and scales it
        scoreVal = scoreVal.astype(int)
        context = {'scoreval': scoreVal, 'temp': temp}
    return render(request, 'index.html', context)
