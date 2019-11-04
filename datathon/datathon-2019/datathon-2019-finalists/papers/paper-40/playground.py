from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from tqdm import tqdm
tqdm.pandas()


# load all the data
train = pd.read_csv("data/ts_train_catid.csv")
val = pd.read_csv("data/ts_val_catid.csv")

features = list(train.columns)
features.remove('userID')
features.remove('inAudience')

sns.heatmap(train[features].corr(), vmin=.7)

target = 'inAudience'
y_true = val[target]

rf = RandomForestClassifier(random_state=42,
                            n_jobs=-1,
                            class_weight={0:.75, 1: 100},
                            n_estimators=250)

rf = rf.fit(train[features], train[target])

feats = pd.DataFrame(data={'feature': features, 'importance': rf.feature_importances_})
feats = feats.sort_values('importance', ascending=False)


important_features = list(feats['feature'][:8])

dtc = DecisionTreeClassifier(random_state=42,
                             criterion='entropy', max_depth=5,
                             class_weight={0:1, 1: 7})
dtc = dtc.fit(train[important_features], train[target])
y_pred = dtc.predict(val[important_features])
print(accuracy_score(y_true, y_pred))
conf_mat = confusion_matrix(y_true, y_pred)
print(conf_mat/np.sum(conf_mat, axis=0))

plot_tree(dtc, max_depth=4, feature_names=important_features, proportion=True)

featdct = pd.DataFrame(data={'feature': important_features, 'importance':dtc.feature_importances_})
featdct = featdct.sort_values('importance', ascending=False)


chart = sns.barplot(x=feats['feature'],
                    y=feats['importance'], palette="Blues_r")
chart.set_xticklabels(chart.get_xticklabels(), fontsize=7,
                      rotation=90, horizontalalignment='center')

chart = sns.barplot(x=featdct['feature'],
                    y=featdct['importance'], palette=sns.color_palette("Blues_r"))
chart.set_xticklabels(chart.get_xticklabels(), fontsize=7,
                      rotation=90, horizontalalignment='center')


sns.distplot( train[train.inAudience == True]['Online Communities_lti'] , color="skyblue")
sns.distplot( train[train.inAudience == False]['Online Communities_lti'] , color="red")

important_features