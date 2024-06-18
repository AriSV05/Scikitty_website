:- use_module(library(csv)).

% Read the CSV file and convert it to a list of dicts
read_csv_file(File, Rows) :-
    csv_read_file(File, Data, [functor(row)]),
    maplist(row_to_dict, Data, Rows).

% Convert a row to a dict
row_to_dict(Row, Dict) :-
    Row =.. [row|Values],
    path(File),
    csv_read_file(File, [HeaderRow|_], [functor(row)]),
    HeaderRow =.. [row|Headers],
    pairs_keys_values(Pairs, Headers, Values),
    dict_create(Dict, row, Pairs).

% Count instances of a class and calculate percentages
count_class([], _, _, 0).
count_class([H|T], ClassAttr, Class, Count) :-
    (get_dict(ClassAttr, H, Class) -> Count1 is 1; Count1 is 0),
    count_class(T, ClassAttr, Class, CountTail),
    Count is Count1 + CountTail.

calculate_percentage(ClassCount, Total, Percent) :-
    Percent is (ClassCount / Total) * 100.