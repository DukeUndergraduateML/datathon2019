import ast
import pandas as pd
from tqdm import tqdm
from tqdm.auto import tqdm
tqdm.pandas()


# def load(file):
#     import pandas as pd
#     import ast
#     df = pd.read_csv(file)

#     # convert the column values from literal string to dictionary
#     df['ltiFeatures'] = df['ltiFeatures'].progress_apply(ast.literal_eval)
#     df['stiFeatures'] = df['stiFeatures'].progress_apply(ast.literal_eval)

#     return df


# # load all the data
# training = load("data/training.csv")
# validation = load("data/validation.csv")
interest_topics = pd.read_csv("interest_topics.csv")

# # inspect the data
# interest_topics.head()
# training.head()
# validation.head()

interest_topics['category_name'] = interest_topics.topic_name.progress_apply(lambda t: t[1:].split('/')[0])
categories = list(set(interest_topics['category_name'].values))
category_ids = {k: (v+1)for v, k in enumerate(categories)}
interest_topics['category_id'] = interest_topics['category_name'].progress_apply(lambda cn: category_ids[cn])

interest_topics.to_csv('categorized_topics.csv', index=False)

interest2topic = {k:v for k,v in interest_topics[['topic_id', 'category_id']].values}
catid2name = {v:k for k,v in category_ids.items()}


def pivot(df):
    df_lti_pivot = df.pivot(index='userID',columns='category_name', values='ltiFeatures')
    df_lti_pivot = df_lti_pivot.fillna(0)
    df_sti_pivot = df.pivot(index='userID',columns='category_name', values='stiFeatures')
    df_sti_pivot = df_sti_pivot.fillna(0)
    df_pivot = pd.merge(df_lti_pivot, df_sti_pivot, on='userID', suffixes =('_lti', '_sti'))
    df_pivot = df_pivot.reset_index()
    return df_pivot


def preprocess_tall_skinny(interest2topic=interest2topic, catid2name=catid2name):
    ts_train = pd.read_csv("data/training_tallskinny.csv")
    ts_validation = pd.read_csv("data/validation_tallskinny.csv")

    ts_train['category_id'] = ts_train['topic_id'].progress_apply(lambda ti: interest2topic.get(ti, 0))
    ts_validation['category_id'] = ts_validation['topic_id'].progress_apply(lambda ti: interest2topic.get(ti, 0))

    del ts_train['topic_id']
    del ts_validation['topic_id']

    ts_train = ts_train.groupby(['userID', 'category_id', 'inAudience']).sum().reset_index()
    ts_validation = ts_validation.groupby(['userID', 'category_id', 'inAudience']).sum().reset_index()


    ts_train['category_name'] = ts_train['category_id'].progress_apply(lambda ci: catid2name.get(ci, 'UNKNOWN'))
    ts_validation['category_name'] = ts_validation['category_id'].progress_apply(lambda ci: catid2name.get(ci, 'UNKNOWN'))

    target_train = ts_train.groupby('userID').mean().reset_index()[['userID', 'inAudience']]
    target_val = ts_validation.groupby('userID').mean().reset_index()[['userID', 'inAudience']]
    
    ts_train = pivot(ts_train)
    ts_validation = pivot(ts_validation)
    ts_train = pd.merge(ts_train, target_train, on=['userID'])
    ts_validation = pd.merge(ts_validation, target_val, on=['userID'])

    ts_train.to_csv('data/ts_train_catid.csv', index=False)
    ts_validation.to_csv('data/ts_val_catid.csv', index=False)


preprocess_tall_skinny()