#!/usr/bin/env python
# coding: utf-8

# In[10]:


import pandas as pd
import math

df = pd.read_csv('mamiferos.csv')


# In[33]:


def calcular_entropia(feature):
    entropia_total = 0
    valores = df[feature].unique()
    total_dataframe = len(df)  
    for valor in valores:
        proporciones = df[df[feature] == valor]["mamifero"].value_counts(normalize=True)
        entropia_valor = sum([-p * math.log2(p) for p in proporciones])
        total_valor = len(df[df[feature] == valor])
        prob = total_valor / total_dataframe
        entropia_total += entropia_valor * prob
        
        #print("\n",feature,"[",valor,"]", "=", total_valor, "/", total_dataframe,"\nproporciones ", proporciones)
        
    return entropia_total


# In[34]:


mejor_feature = None
mejor_entropia = float('inf')
entropias = {}

for columna in df.columns[1:-1]:  # Excluimos la primera (animal) y la última (mamifero)
    actual_entropia = calcular_entropia(columna)
    entropias[columna] = actual_entropia
    if actual_entropia < mejor_entropia:
        mejor_entropia = actual_entropia
        mejor_feature = columna


# In[35]:


print("La entropia para cada feature:")
for feature, entropia in entropias.items():
    print(f"{feature}: {entropia}")
        
print("\nEl mejor atributo de split es", mejor_feature,"con una entropia de", mejor_entropia)


# In[41]:


def calcular_gini(feature):
    gini_total = 0
    valores = df[feature].unique()
    total_dataframe = len(df)  
    for valor in valores:
        proporciones = df[df[feature] == valor]["mamifero"].value_counts(normalize=True)
        gini = 1 - sum([p ** 2 for p in proporciones])
        total_valor = len(df[df[feature] == valor])
        prob = total_valor / total_dataframe
        gini_total += gini * prob
        
        #print("\n",feature,"[",valor,"]", "=", total_valor, "/", total_dataframe,"\nproporciones ", proporciones)
        
    return gini_total


# In[42]:


mejor_feature = None
mejor_gini = float('inf')
ginis = {}

for columna in df.columns[1:-1]:  # Excluimos la primera (animal) y la última (mamifero)
    actual_gini = calcular_gini(columna)
    ginis[columna] = actual_gini
    if actual_gini < mejor_gini:
        mejor_gini = actual_gini
        mejor_feature = columna

#ginis


# In[43]:


print("El indice gini para cada feature:")
for feature, gini in ginis.items():
    print(f"{feature}: {gini}")
        
print("\nEl mejor atributo de split es", mejor_feature,"con un indice gini de", mejor_gini)


# In[ ]:




