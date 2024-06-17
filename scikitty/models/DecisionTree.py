import numpy as np
from dsplot.tree import BinaryTree
import pandas as pd
import queue
from .Node import Node as Node
        
class DecisionTreeClassifier():
    def __init__(self, min_samples_split=2, max_depth=2):
        
        self.root = None
        
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        
    def build_tree(self, dataset, curr_depth=1):
        #Se construye el arbol recursivamente viendo quien es el mejor feature y se guarda en un nodo, 
        #cuando se sale la recursividad, solo guarda el valor de la hoja (Y)
        
        X, Y = dataset[:,:-1], dataset[:,-1]
        num_samples, num_features = np.shape(X) # num_samples(row) y num_features(columns)
        
        #print(np.shape(X))
        
        #Nodos
        if num_samples>=self.min_samples_split and curr_depth<=self.max_depth: 
            best_split = self.get_best_decision_point(dataset, num_samples, num_features)
            if best_split.get("gain",0)>0:
                # nodo izq
                left_subtree = self.build_tree(best_split["dataset_left"], curr_depth+1)
                # nodo der
                right_subtree = self.build_tree(best_split["dataset_right"], curr_depth+1)
                return Node(best_split["feature_index"], best_split["decision_point"], 
                            left_subtree, right_subtree, best_split["gain"], num_samples)
        
        #Hojas
        leaf_value = self.calculate_leaf_value(Y)
        return Node(value=leaf_value, rest_samples=num_samples)
    
    def get_best_decision_point(self, dataset, num_samples, num_features):
        # Buscar el mejor feature para el árbol 
        
        best_split = {} # diccionario 
        max_gain = -float("inf") #obtener el mejor
        
        # Ciclo de cada variable (feature column name)
        for feature_index in range(num_features):
            
            feature_values = dataset[:, feature_index]
            possible_decision_points = np.unique(feature_values)
            
            # Ciclo de cada feature unico (filas)
            for decision_point in possible_decision_points:
                dataset_left, dataset_right = self.split(dataset, feature_index, decision_point)
                
                if len(dataset_left)>0 and len(dataset_right)>0:
                    y, left_y, right_y = dataset[:, -1], dataset_left[:, -1], dataset_right[:, -1]
                    # Calculo la ganancia
                    curr_gain = self.calculate_gain(y, left_y, right_y)
                    
                    if curr_gain > max_gain: # Si es mejor al max_gain se actualiza por el actual
                        best_split["feature_index"] = feature_index
                        best_split["decision_point"] = decision_point
                        best_split["dataset_left"] = dataset_left
                        best_split["dataset_right"] = dataset_right
                        best_split["gain"] = curr_gain
                        max_gain = curr_gain

                        
        return best_split
    
    def split(self, dataset, feature_index, decision_point):
        #Divido el dataset en izq y der
        dataset_left = []
        dataset_right = []
        
        if (isinstance(decision_point, int) or isinstance(decision_point, float)): #Si es numerico el feature
            dataset_left = np.array([row for row in dataset if row[feature_index]<=decision_point])
            dataset_right = np.array([row for row in dataset if row[feature_index]>decision_point])
            #print("NUMERICO: ", feature_index,threshold)

        else: #Si es categorico el feature
            dataset_left = np.array([row for row in dataset if row[feature_index]==decision_point])
            dataset_right = np.array([row for row in dataset if row[feature_index]!=decision_point])
            #print("CATEGORICO: ", feature_index,threshold)
            
        #print("Dateset L y R : ", dataset_left,dataset_right)
        return dataset_left, dataset_right
    
    def calculate_gain(self, parent, l_child, r_child):
       #Calcular ganancia con gini
        
        weight_l = len(l_child) / len(parent)
        weight_r = len(r_child) / len(parent)

        #Obtener con G(parent) - sum(wi * G(child(i)) ) el que sea mayor va a ser el mejor
        gain = self.gini(parent) - (weight_l*self.gini(l_child) + weight_r*self.gini(r_child))
        #print("GAIN", gain)
        return gain
    
    def gini(self, y):
        #Calcular Gini
        
        class_labels = np.unique(y)
        #print("class_labels", class_labels, "Y", y)
        gini = 0
        for cls in class_labels:
            p_cls = len(y[y == cls]) / len(y)
            gini += p_cls**2
            
        #print("GINI", 1 - gini)
        return 1 - gini
        
    def calculate_leaf_value(self, Y):
        #Obtener valor de la hoja
        Y = list(Y)
        return max(Y, key=Y.count) #Calcula el max de veces de un elemento que aparece en Y
    
    def print_tree(self, tree=None, indent=" ",data= None):
        #Imprimir el arbol en consola
        if not tree:
            tree = self.root

        if tree.value is not None:  
            print(tree.value, tree.rest_samples)

        else:
            if (isinstance(tree.decision_point, int) or isinstance(tree.decision_point, float)):#Numerico
                print(data.columns[tree.feature_index], "<=", tree.decision_point, "?", "{Gain:",tree.gain, " Samples:", tree.samples,"}")
                print("%sleft:" % (indent), end="")
                self.print_tree(tree.left, indent + indent, data)
                print("%sright:" % (indent), end="")
                self.print_tree(tree.right, indent + indent, data)

            else: #Categorico
                print(data.columns[tree.feature_index], "==", tree.decision_point, "?", "{Gain:",tree.gain, " Samples:", tree.samples,"}")
                print("%sleft:" % (indent), end="")
                self.print_tree(tree.left, indent + indent, data)
                print("%sright:" % (indent), end="")
                self.print_tree(tree.right, indent + indent, data)

    
    def BFS_list(self,data= None):
        #Obtener una lista por breath first search del arbol construido 
        nodes=[]
        tree = self.root
        if tree is None:
            return
        
        cola = queue.Queue()
        cola.put(tree)
        while not cola.empty():
            tmp = cola.get()
            
            if(tmp.decision_point is not None):
                if (isinstance(tmp.decision_point, int) or isinstance(tmp.decision_point, float)):
                    question = " "+data.columns[tmp.feature_index] + " <= " + str(tmp.decision_point) + " ?"
                else:
                    question = " "+data.columns[tmp.feature_index] + " == " + tmp.decision_point + " ?"
                nodes.append(question)
            else:
                nodes.append(tmp.value)

            if tmp.left is not None:
                cola.put(tmp.left)
            if tmp.right is not None:
                cola.put(tmp.right)
                
        return nodes

    def image_tree_model(self, Y, data, route):
        #Crear imagen del Arbol con dsplot
        plotNodes = self.BFS_list(data)
        places = [i for i, n in enumerate(plotNodes) if n in np.unique(Y)]

        for i, v in enumerate(places):
            index_left_child = 2 * v + 1
            index_right_child = 2 * v + 2
            
            if index_left_child < len(plotNodes) and plotNodes[index_left_child] is not None:
                plotNodes.insert(index_left_child, None)
            else:
                #print("STOP: No hay hijo izquierdo en el nodo", v)
                break
            
            if index_right_child < len(plotNodes) and plotNodes[index_right_child] is not None:
                plotNodes.insert(index_right_child, None)
            else:
                #print("STOP: No hay hijo derecho en el nodo", v)
                break

        tree = BinaryTree(plotNodes)
        tree.plot(f'{route}.png', fill_color='#aec6cf')  

    def fit(self, X, Y):
        #Entrenar el modelo, o sea construir el arbol
        dataset = np.concatenate((X, Y), axis=1)
        self.root = self.build_tree(dataset)
    
    def predict(self, X):
        #Predecir con el modelo
        preditions = [self.make_prediction(x, self.root) for x in X]
        return preditions

    def make_prediction(self, x, tree):
        #predice un dato en el arbol

        if tree.value!=None: return tree.value
        feature_val = x[tree.feature_index]
        if (isinstance(feature_val, int) or isinstance(feature_val, float)):#Numerico
            if feature_val<=tree.decision_point:
                return self.make_prediction(x, tree.left)
            else:
                return self.make_prediction(x, tree.right)
        else: #Categorico
            if feature_val==tree.decision_point:
                return self.make_prediction(x, tree.left)
            else:
                return self.make_prediction(x, tree.right)