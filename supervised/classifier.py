from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from decision_tree import decisionTree
from random_forest import randomForest
from ada_boost import adaBoost
from naiveBayesCategorico import naiveBayesCategorical

#Calcolo delle feature importance
def printFeatureRanking(clf, X, path):
    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    print("\nFeature ranking:")
    for f in range(0, 5):
        print("%d. %s (%f)" % (f+1, X.columns[indices[f]], importances[indices[f]]))

    # creazione del grafico
    plt.clf()
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(X.shape[1]), importances[indices], color="orange", align="center")
    plt.xticks(range(X.shape[1]), [categorical_features[i] if i<len(categorical_features) else numeric_features[i-len(categorical_features)] for i in indices], rotation=90, fontsize=8)
    plt.xlim([-1, X.shape[1]])
    plt.subplots_adjust(bottom=0.4)

    plt.savefig(path)

# Caricamento del dataset
data = pd.read_csv("data/working_dataset/dataset_operativo.csv")
#map={'rain':1, 'snow':2}

# Selezionare le feature e la variabile target
categorical_features = ["Summary", "Daily Summary","wind_chill","Precip Type"]
numeric_features = ["Temperature (C)", "Apparent Temperature (C)", "Humidity","Wind Speed (km/h)","Wind Bearing (degrees)","Visibility (km)","Pressure (millibars)"]
target = "season"
#data["Precip Type"]=data["Precip Type"].replace(map)
X = data[categorical_features + numeric_features]
data=data.dropna()
X=X.dropna()
print("\n---DECISION TREE---")
clf = decisionTree(data, categorical_features, numeric_features, target)
printFeatureRanking(clf, X, "images/features/dt_feature.png" )

print("\n---RANDOM FOREST---")
clf = randomForest(data, categorical_features, numeric_features, target)
printFeatureRanking(clf, X, "images/features/rf_feature.png" )

print("\n---NAIVE BAYES CATEGORICAL---")
clf = naiveBayesCategorical(data, categorical_features, target)

print("\n---ADA BOOST---")
clf = adaBoost(data, categorical_features, numeric_features, target)
printFeatureRanking(clf, X, "images/features/ab_feature.png" )

