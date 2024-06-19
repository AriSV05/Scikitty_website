from ..scikitty import scikitty_funtions as sk
from ..scikitty.models.DecisionTree import DecisionTreeClassifier
from ..scikitty.metrics.metrics import accuracy_score, recall_score, precision_score, f1_score
import numpy as np
import os
from sklearn.metrics import mean_squared_error


def building_tree(filename, target):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    ruta = os.path.join(project_root, 'csv', filename)
    models = os.path.join(project_root, 'created_models', f'{filename}.pkl')

    data = sk.read_csv_with_column_names(ruta)

    target_column = data.pop(target)
    data[target] = target_column;
    
    X = data.drop(columns=[target]).values
    Y = data[target].values.reshape(-1,1)

    X_train, X_test, Y_train, Y_test = sk.train_test_split(X, Y)

    targets = np.array(Y).flatten()
    uniques_targets = np.unique(targets)

    if os.path.isfile(models):
        print("**Loading existing model**\n\n")
        classifier = sk.import_model(models)

    else:
        altura = 6

        classifier = DecisionTreeClassifier(min_samples_split= 2, max_depth=altura)
        classifier.fit(X_train,Y_train)

        model_name = filename

        sk.save_model(classifier, model_name, f'{project_root}/created_models')
    
    classifier.print_tree(data=data)

    return uniques_targets, X_test, Y_test, classifier

def metrics(y_test, x_test, classifier, targets, positive_pos):
     y_pred = classifier.predict(x_test)
 
     positive = targets[positive_pos]

     accuracy = accuracy_score(y_test, y_pred)
     precision = precision_score(y_test, y_pred, positive)
     recall = recall_score(y_test, y_pred, positive)
     f1 = f1_score(precision, recall)

     results = {
        "Accuracy":accuracy,
        "Precision":precision,
        "recall":recall,
        "f1":f1
    }
     
     print(results)

def console_input(targets):
    while True:
        entrada = input(f'Ingese 0 para seleccionar como positivo *{targets[0]}* o 1 para seleccionar *{targets[1]}*: ')
        if entrada == "1" or entrada == "0":
            break
        else:
            print("¡Error! Debes ingresar solo 1 o 0.")
    return int(entrada)

def tree_boosting(filename, target):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    ruta = os.path.join(project_root, 'csv', filename)
    data = sk.read_csv_with_column_names(ruta)

    X = data.drop(columns=[target]).values
    Y = data[target].values.reshape(-1,1)

    _, X_test, _, Y_test = sk.train_test_split(X, Y)

    h = sk.tree_gradient_boosting(X_test, Y_test, T=20, alpha=0.1, alpha_min=0.01, data_columns=data)
   
    mse = mean_squared_error(Y_test, h)
    print(f"\nMSE: {mse}\n")
