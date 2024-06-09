import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def accuracy_score(y_test, y_pred):
    correct = 0
    for true, pred in zip(y_test, y_pred):
        if true == pred:
            correct += 1
    accuracy = correct / len(y_test)
    return accuracy

def recall_score(y_test, y_pred, positive_class): 
    true_positives = 0
    actual_positives = 0
        
    for true, pred in zip(y_test, y_pred):
        if true == positive_class:
            actual_positives += 1
            if pred == positive_class:
                true_positives += 1
                    
    if actual_positives == 0:
        return 0  # Si no hay muestras positivas en los datos reales, el recall es 0
        
    recall = true_positives / actual_positives
    return recall

def precision_score(y_test, y_pred, positive_class):
    true_positives = 0
    false_positives = 0

    for true, pred in zip(y_test, y_pred):
        if pred == positive_class:
            if true == positive_class:
                true_positives += 1
            else:
                false_positives += 1  

    if (true_positives + false_positives) == 0:
        return 0
    else:
        return true_positives / (true_positives + false_positives)
    
def f1_score(precision, recall):
    if precision + recall == 0:
        return 0
    return 2 * (precision * recall) / (precision + recall)

def confusion_matrix(y_test, y_pred):
    # Convertir a arrays NumPy unidimensionales
    y_test_uni = np.array(y_test).flatten()
        
    # Encontrar las clases únicas presentes en las etiquetas verdaderas y las predicciones
    classes = np.unique(np.concatenate((y_test_uni, y_pred)))

    # Inicializar la matriz de confusión como una matriz numpy
    matrix = np.zeros((len(classes), len(classes)), dtype=int)
        
    # Llenar la matriz de confusión
    for true, pred in zip(y_test, y_pred):
        true_idx = np.where(classes == true)[0][0]
        pred_idx = np.where(classes == pred)[0][0]
        matrix[true_idx, pred_idx] += 1
        
    # Crear un DataFrame de Pandas para la matriz de confusión
    conf_df = pd.DataFrame(matrix, index=classes, columns=classes)
        
    label_1 = classes[1] if 1 in classes else classes[0]
    label_2 = classes[0] if label_1 == classes[1] else classes[1]
        
    # Agregar etiquetas a la matriz
    conf_df.rename({label_1: label_1, label_2: label_2}, axis=0, inplace=True)
    conf_df.rename({label_1: label_1, label_2: label_2}, axis=1, inplace=True)
        
    return conf_df
    
def img_confusion_matrix(y_test, y_pred, route):
    matrix = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    tick_marks = range(len(matrix))
    plt.xticks(tick_marks, matrix.columns, rotation=45)
    plt.yticks(tick_marks, matrix.index)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig(route)  
