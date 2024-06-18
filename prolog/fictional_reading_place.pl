:- [utils].

path('../csv/fictional_reading_place.csv').

% Tree rules

dt_length(Ex, skips) :- 
    _{length:long} :< Ex, 
    writeln('Length is long, predicting skips').

dt_length(Ex, UA) :- 
    _{length:short} :< Ex, 
    writeln('Length is short, passing to dt_author'),
    dt_author(Ex, UA).

dt_author(Ex, reads) :- 
    _{author:known} :< Ex, 
    writeln('  Author is known, predicting reads').

dt_author(Ex, UA) :- 
    _{author:unknown} :< Ex, 
    writeln('  Author is unknown, passing to dt_thread'),
    dt_thread(Ex, UA).

dt_thread(Ex, reads) :- 
    _{thread:new} :< Ex, 
    writeln('    Thread is new, predicting reads').

dt_thread(Ex, skips) :- 
    _{thread:follow_up} :< Ex, 
    writeln('    Thread is follow_up, predicting skips').

dt_pred(Ex, UA) :- 
    dt_length(Ex, UA),
    writeln(''),
    format('Final prediction: ~w~n', [UA]).

test_predict(UserAction) :-
    Ex = _{length:short, author:unknown, thread:follow_up},
    writeln('Testing prediction for example:'),
    writeln("{length:short, author:known, thread:follow_up}"),
    writeln(''),
    dt_pred(Ex, UserAction).

:- initialization(test_predict(_)).