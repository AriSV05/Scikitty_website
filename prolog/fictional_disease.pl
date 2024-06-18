:- [utils].

path('../csv/fictional_disease.csv').

dt_smokerH(Ex, UA) :- 
    _{smokerHistory:non_smoker} :< Ex, 
    writeln('Smoker History is non_smoker, passing to dt_age'),
    dt_age(Ex, UA).

dt_smokerH(Ex, UA) :- 
    _{smokerHistory:smoker} :< Ex, 
    writeln('Smoker History is smoker, passing to dt_age'),
    dt_age(Ex, UA).


dt_age(Ex, UA) :-
    _{age:Age} :< Ex, 
    (
        Age>=65 -> writeln('  Age is bigger than 65, predicting not_disease'), UA = not_disease
        ;
        Age>=32, Age<65 -> writeln('  Age is bigger than 32 and smaller than 65, predicting disease'), UA = disease
        ;
        Age>=27, Age<32 -> writeln('  Age is bigger than 27 and smaller than 32, predicting not disease'), UA = not_disease
        ;
        Age>=24, Age<27 -> writeln('  Age is bigger than 24 and smaller than 27, predicting disease'), UA = disease
        ;
        Age>=22, Age<24 -> writeln('  Age is bigger than 22 and smaller than 24, passing to dt_gender'), dt_gender(Ex,UA)
        ;
        Age>=12, Age<22 -> writeln('  Age is bigger than 12 and smaller than 22, predicting disease'), UA = disease
        ;
        writeln('  Age is smaller than 12, predicting not_disease'), UA = not_disease
    ).

dt_gender(Ex, not_disease) :- 
    _{gender:female} :< Ex, 
    writeln('    Gender is female, predicting not_disease').

dt_gender(Ex, not_disease) :- 
    _{gender:male} :< Ex, 
    writeln('    Gender is male, predicting not_disease').

dt_pred(Ex, UA) :- 
    dt_smokerH(Ex, UA),
    writeln(''),
    format('Final prediction: ~w~n', [UA]).

test_predict(UserAction) :-
    Ex = _{smokerHistory:non_smoker, age:23, gender:female},
    writeln('Testing prediction for example:'),
    writeln("{smokerHistory:non_smoker, age:23, gender:female}"),
    writeln(''),
    dt_pred(Ex, UserAction).

:- initialization(test_predict(_)).