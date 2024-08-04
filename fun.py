from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier
import pandas as pd
from sklearn.model_selection import train_test_split

def modeling(path_file,
             models = [LogisticRegression(solver = "liblinear")],
             features = [],
             aim = "regression",
             ):
    wyniki = []
    data = pd.read_csv(path_file)
    X = data[features[0]]
    Y = data[features[1]]
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state = 2)    

    if aim == "regression":
        for model in models:
            model.fit(x_train, y_train)
            accuracy = model.score(x_test, y_test)            
            print(f"{str(model.__class__.__name__)}: {accuracy}")
            wyniki.append(accuracy)
    if aim == "classification":
        for model in models:
            model.fit(x_train, y_train)
            accuracy = model.score(x_test, y_test)            
            print(f"{str(model.__class__.__name__)}: {accuracy}")
            wyniki.append(accuracy)
    
    return wyniki

