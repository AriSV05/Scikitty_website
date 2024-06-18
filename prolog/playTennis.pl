:- [utils].

path('../csv/playTennis.csv').

% Tree rules

dt_outlook(Ex, yes) :- 
    _{outlook:overcast} :< Ex, 
    writeln('Outlook is overcast, predicting yes').

dt_outlook(Ex, UA) :- 
    _{outlook:not_overcast} :< Ex, 
    writeln('Outlook is not overcast, passing to dt_humidity'),
    dt_humidity(Ex, UA).

dt_humidity(Ex, no) :- 
    _{humidity:high} :< Ex, 
    writeln('  Humidity is high, predicting no').

dt_humidity(Ex, UA) :- 
    _{humidity:normal} :< Ex, 
    writeln('  Humidity is normal, passing to dt_wind'),
    dt_wind(Ex, UA).

dt_wind(Ex, no) :- 
    _{wind:strong} :< Ex, 
    writeln('    Wind is strong, predicting no').

dt_wind(Ex, yes) :- 
    _{thread:weak} :< Ex, 
    writeln('    Wind is weak, predicting yes').

dt_pred(Ex, UA) :- 
    dt_outlook(Ex, UA),
    writeln(''),
    format('Final prediction: ~w~n', [UA]).

test_predict(UserAction) :-
    Ex = _{outlook:not_overcast, humidity:normal, wind:strong},
    writeln('Testing prediction for example:'),
    writeln("{outlook:not_overcast, humidity:normal, wind:strong}"),
    writeln(''),
    dt_pred(Ex, UserAction).

:- initialization(test_predict(_)).