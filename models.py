import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix


class Model:

    def __init__(self):
        self.name = ''
        path = 'dataset/records.csv'
        df = pd.read_csv(path)
        df = df[['Experience', 'Certifications', 'PG', 'Graduation', 'Linkedin', 'Github', 'Metro', 'LinkCount', 'CPP',
                 'SQL', 'GIT', 'WEB', 'class']]

        # Handling Missing Data
        df['Experience'] = df['Experience'].fillna(df['Experience'].mode()[0])
        df['Certifications'] = df['Certifications'].fillna(df['Certifications'].mode()[0])
        df['PG'] = df['PG'].fillna(df['PG'].mode()[0])
        df['Graduation'] = df['Graduation'].fillna(df['Graduation'].mode()[0])
        df['Linkedin'] = df['Linkedin'].fillna(df['Linkedin'].mode()[0])
        df['Github'] = df['Github'].fillna(df['Github'].mode()[0])
        df['Metro'] = df['Metro'].fillna(df['Metro'].mode()[0])
        df['LinkCount'] = df['LinkCount'].fillna(df['LinkCount'].mode()[0])
        df['CPP'] = df['CPP'].fillna(df['CPP'].mode()[0])
        df['SQL'] = df['SQL'].fillna(df['SQL'].mode()[0])
        df['GIT'] = df['GIT'].fillna(df['GIT'].mode()[0])
        df['WEB'] = df['WEB'].fillna(df['WEB'].mode()[0])
        df['class'] = df['class'].fillna(df['class'].mode()[0])

        labelencoder = LabelEncoder()
        df['PG'] = labelencoder.fit_transform(df['PG'])
        df['Graduation'] = labelencoder.fit_transform(df['Graduation'])
        df['Linkedin'] = labelencoder.fit_transform(df['Linkedin'])
        df['Github'] = labelencoder.fit_transform(df['Github'])
        df['Metro'] = labelencoder.fit_transform(df['Metro'])
        df['CPP'] = labelencoder.fit_transform(df['CPP'])
        df['SQL'] = labelencoder.fit_transform(df['SQL'])
        df['GIT'] = labelencoder.fit_transform(df['GIT'])
        df['WEB'] = labelencoder.fit_transform(df['WEB'])
        self.split_data(df)

    def split_data(self, df):
        x = df.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]].values
        y = df.iloc[:, 12].values
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=24)
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test

    def svm_classifier(self):
        self.name = 'Svm Classifier'
        classifier = SVC()
        return classifier.fit(self.x_train, self.y_train)

    def decisionTree_classifier(self):
        self.name = 'Decision tree Classifier'
        classifier = DecisionTreeClassifier()
        return classifier.fit(self.x_train, self.y_train)

    def randomforest_classifier(self):
        self.name = 'Random Forest Classifier'
        classifier = RandomForestClassifier()
        return classifier.fit(self.x_train, self.y_train)

    def naiveBayes_classifier(self):
        self.name = 'Naive Bayes Classifier'
        classifier = GaussianNB()
        return classifier.fit(self.x_train, self.y_train)

    def knn_classifier(self):
        self.name = 'Knn Classifier'
        classifier = KNeighborsClassifier()
        return classifier.fit(self.x_train, self.y_train)

    def accuracy(self, model):
        predictions = model.predict(self.x_test)
        cm = confusion_matrix(self.y_test, predictions)
        accuracy = (cm[0][0] + cm[1][1]) / (cm[0][0] + cm[0][1] + cm[1][0] + cm[1][1])
        print(f"{self.name} has accuracy of {accuracy * 100} % ")


if __name__ == '__main__':
    model = Model()
    model.accuracy(model.svm_classifier())
    model.accuracy(model.decisionTree_classifier())
    model.accuracy(model.randomforest_classifier())
    model.accuracy(model.naiveBayes_classifier())
    model.accuracy(model.knn_classifier())
