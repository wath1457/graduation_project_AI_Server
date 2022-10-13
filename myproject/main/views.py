from django.shortcuts import render, HttpResponse, redirect

import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from eunjeon import Mecab
from collections import Counter
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from keras.models import load_model

 
# Create your views here.
def index(request):
    return render(request, "main/index.html")
def depression(request):
    
    return redirect('/')
