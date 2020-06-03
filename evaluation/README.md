This directory contains scripts used to evaluate user provided feedback stored
in the ```./data/evaluation-reports``` directory. 

# How it is done?

## Scores
For every evaluation we collect ordering of the methods. User provides
the ordering by other using drag and drop or by changing the order
in the text box.

For example user may rate methods *A*, *B*, *C*, *D*, *E* with values
```1, 2, 2, 3, 4``` respectively. One of the method, user does not know
which one, is used as a baseline, let us assume that *D* is the baseline method.

Now we want to change the result into interval ```<-1, 1>```. Baseline method
map to value 0. Methods performing better (with smaller user rating) will be
mapped to positive integers. 

Next we compute several values:
 * *baseline* the score assigned to baseline method
 * *min_value* the minimal assigned score minus *baseline*
 * *max_value* the maximum assigned score minus *baseline*
 * *scale* ```max(abs(min_value), abs(max_value))```

In our case the values are:
 * *baseline* = 3
 * *min_value* = -2
 * *max_value* = 1
 * *scale* = 2

Now we can transform each score using following formula:
 ```score = - (value - baseline) / scale```
The idea is to center the results using baseline, next we scale them to
```<-1, 1>``` there the maximum or minimum is equal to either -1 or 1.
In the last step we take the negative values, as higher score actually 
corresponds to poorer performance.

If we apply this to our number we got:
 * *A* ```-(1 - 3) / 2 =  1.0``` 
 * *B* ```-(2 - 3) / 2 =  0.5```
 * *C* ```-(2 - 3) / 2 =  0.5```
 * *D* ```-(3 - 3) / 2 =  0.0```
 * *E* ```-(4 - 3) / 2 = -0.5```

## Duration
For each session we store times of user actions like: loading the form,
changing the order and submit. 

We compute duration as *submit time* - *first action time*.
 