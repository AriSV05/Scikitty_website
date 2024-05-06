import numpy as np

class Node():
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, info_gain=None, samples=None, value=None, rest_samples=None):
        ''' constructor ''' 
        
        # for decision node
        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.info_gain = info_gain
        self.samples = samples
        self.rest_samples = rest_samples
        
        # for leaf node
        self.value = value
        
class DecisionTreeClassifier():
    def __init__(self, min_samples_split=2, max_depth=2):
        ''' constructor '''
        
        # initialize the root of the tree 
        self.root = None
        
        # stopping conditions
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        
    def build_tree(self, dataset, curr_depth=1):
        ''' recursive function to build the tree ''' 
        
        X, Y = dataset[:,:-1], dataset[:,-1]
        num_samples, num_features = np.shape(X)
        
        #print(np.shape(X))
        
        # split until stopping conditions are met
        if num_samples>=self.min_samples_split and curr_depth<=self.max_depth:  #aqui se podria quitar min
            # find the best split
            best_split = self.get_best_split(dataset, num_samples, num_features)
            # check if information gain is positive
            if best_split["info_gain"]>0:
                # recur left
                left_subtree = self.build_tree(best_split["dataset_left"], curr_depth+1)
                # recur right
                right_subtree = self.build_tree(best_split["dataset_right"], curr_depth+1)
                # return decision node
                return Node(best_split["feature_index"], best_split["threshold"], 
                            left_subtree, right_subtree, best_split["info_gain"], num_samples)
        
        # compute leaf node
        leaf_value = self.calculate_leaf_value(Y)
        # return leaf node
        return Node(value=leaf_value, rest_samples=num_samples)
    
    def get_best_split(self, dataset, num_samples, num_features):
        ''' function to find the best split '''
        
        # dictionary to store the best split
        best_split = {}
        max_info_gain = -float("inf")
        
        # loop over all the features
        for feature_index in range(num_features):
            
            feature_values = dataset[:, feature_index]
            #print(feature_values)
            
            possible_thresholds = np.unique(feature_values)
            #print(possible_thresholds)
            
            # loop over all the feature values present in the data
            for threshold in possible_thresholds:
                # get current split
                dataset_left, dataset_right = self.split(dataset, feature_index, threshold)
                # check if childs are not null
                if len(dataset_left)>0 and len(dataset_right)>0:
                    y, left_y, right_y = dataset[:, -1], dataset_left[:, -1], dataset_right[:, -1]
                    # compute information gain
                    curr_info_gain = self.information_gain(y, left_y, right_y)
                    # update the best split if needed
                    if curr_info_gain>max_info_gain:
                        best_split["feature_index"] = feature_index
                        best_split["threshold"] = threshold
                        best_split["dataset_left"] = dataset_left
                        best_split["dataset_right"] = dataset_right
                        best_split["info_gain"] = curr_info_gain
                        max_info_gain = curr_info_gain

                        
        return best_split
    
    def split(self, dataset, feature_index, threshold):
        ''' function to split the data '''
        dataset_left = []
        dataset_right = []
        
        '''dataset_left = np.array([row for row in dataset if row[feature_index]<=threshold])
        dataset_right = np.array([row for row in dataset if row[feature_index]>threshold])'''
        #print(feature_index,threshold)
        
        if (isinstance(threshold, int) or isinstance(threshold, float)):
            dataset_left = np.array([row for row in dataset if row[feature_index]<=threshold])
            dataset_right = np.array([row for row in dataset if row[feature_index]>threshold])
            #print("NUMEROO..", feature_index,threshold)
        else:
            dataset_left = np.array([row for row in dataset if row[feature_index]==threshold])
            dataset_right = np.array([row for row in dataset if row[feature_index]!=threshold])
            #print("CARACTER..", feature_index,threshold)
            
        #print("DATAset L Y R..", dataset_left,dataset_right)
        return dataset_left, dataset_right
    
    def information_gain(self, parent, l_child, r_child):
        ''' function to compute information gain '''
        
        weight_l = len(l_child) / len(parent)
        weight_r = len(r_child) / len(parent)

        #print("l_child", l_child, "r_child", r_child)
        #Obtener con G(parent) - sum(wi * G(child(i)) ) el que sea mayor va a ser el mejor
        gain = self.gini_index(parent) - (weight_l*self.gini_index(l_child) + weight_r*self.gini_index(r_child))
        #print("GAIN", gain)
        return gain
    
    def gini_index(self, y):
        ''' function to compute gini index '''
        
        class_labels = np.unique(y)
        #print("class_labels", class_labels, "Y", y)
        gini = 0
        for cls in class_labels:
            p_cls = len(y[y == cls]) / len(y)
            gini += p_cls**2
            
        #print("GINI", 1 - gini)
        return 1 - gini
        
    def calculate_leaf_value(self, Y):
        ''' function to compute leaf node '''
        
        Y = list(Y)
        return max(Y, key=Y.count)
    
    def print_tree(self, tree=None, indent=" ",data= None):
        ''' function to print the tree '''
        
        if not tree:
            tree = self.root

        if tree.value is not None:
            print(tree.value, tree.rest_samples)

        else:
            if (isinstance(tree.threshold, int) or isinstance(tree.threshold, float)):#Numerico
                print(data.columns[tree.feature_index], "<=", tree.threshold, "?", tree.info_gain)
                print("%sleft:" % (indent), end="")
                self.print_tree(tree.left, indent + indent, data)
                print("%sright:" % (indent), end="")
                self.print_tree(tree.right, indent + indent, data)
            else:
                print(data.columns[tree.feature_index], "==", tree.threshold, "?", "{Gain:",tree.info_gain, " Samples:", tree.samples,"}")
                print("%sleft:" % (indent), end="")
                self.print_tree(tree.left, indent + indent, data)
                print("%sright:" % (indent), end="")
                self.print_tree(tree.right, indent + indent, data)
    
    def fit(self, X, Y):
        ''' function to train the tree '''
        
        dataset = np.concatenate((X, Y), axis=1)
        self.root = self.build_tree(dataset)
    
    def predict(self, X):
        ''' function to predict new dataset '''
        
        preditions = [self.make_prediction(x, self.root) for x in X]
        return preditions
    
    def make_prediction(self, x, tree): #ve num y cat
        ''' function to predict a single data point '''
        
        if tree.value!=None: return tree.value
        feature_val = x[tree.feature_index]
        if (isinstance(feature_val, int) or isinstance(feature_val, float)):#Numerico
            if feature_val<=tree.threshold:
                return self.make_prediction(x, tree.left)
            else:
                return self.make_prediction(x, tree.right)
        else: #Categorico
            if feature_val==tree.threshold:
                return self.make_prediction(x, tree.left)
            else:
                return self.make_prediction(x, tree.right)

class Metrics():
    def __init__(self):
        pass
    
    def accuracy_score(y_true, y_pred):
        ''' Function to calculate accuracy score '''
        
        correct = 0
        for true, pred in zip(y_true, y_pred):
            if true == pred:
                correct += 1
        accuracy = correct / len(y_true)
        return accuracy

    def recall_score(y_true, y_pred, positive_class):
        ''' Function to calculate recall score '''
        
        true_positives = 0
        actual_positives = 0
        
        for true, pred in zip(y_true, y_pred):
            if true == positive_class:
                actual_positives += 1
                if pred == positive_class:
                    true_positives += 1
                    
        if actual_positives == 0:
            return 0  # Si no hay muestras positivas en los datos reales, el recall es 0
        
        recall = true_positives / actual_positives
        return recall

    def precision_score(y_true, y_pred, positive_class):
    
        true_positives = 0
        false_positives = 0

        for true, pred in zip(y_true, y_pred):
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
