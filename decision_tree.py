from sklearn import tree
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, plot_confusion_matrix#for visualizing tree


for i in categorical_column_list:
    print(i)
    values = pd.DataFrame(previous_application[i].value_counts()).reset_index()
    #print(values)
    k=0
    for j in values['index']:
        #print(j)
        print("Replace ",j," By ",k)
        previous_application[i] = previous_application[i].replace([j],k)
        k=k+1

feature_columns = []
for i in previous_application.columns:
    if i != 'TARGET':
        feature_columns.append(i)
        print(i)

X = previous_application[feature_columns]
Y = previous_application['TARGET']
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=1) # 70% training and 30% test

# Create Decision Tree classifer object
clf = DecisionTreeClassifier()
clf = clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)
print("Classification report - \n", classification_report(y_test,y_pred))
