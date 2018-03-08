import pandas as pd
import numpy as np
import implicit
from scipy.sparse import csr_matrix

store_details=pd.read_csv('storeDetails.csv')

transaction=pd.read_csv('TransactionDetails_Dummy_Final_with_cat.csv')

users=pd.read_csv('User_Details_Dummy_Final.csv')


users.columns=['User_id', u'currentpoints', u'lifetimepoints', u'lifetimepurchases',
       u'dateofjoining', u'slabname', u'Lastupdatedstorename', u'Gender',
       u'agegroup', u'birthday', u'anniversary', u'pincode', u'kidsgender',
       u'kidsagegroup', u'Contact_number']

transaction_user=transaction.merge(users,on='User_id',how='left')

transaction['Category']=transaction['Category'].fillna('nill')

transaction=transaction[transaction['Category']!='nill']

cols=[ u'User_id', u'Category', u'Gender', u'agegroup',u'birthday',u'anniversary', u'pincode',u'kidsgender', u'kidsagegroup',u'Contact_number']

transaction_user['kidsagegroup']=transaction_user['kidsagegroup'].fillna('nill')

transaction_user[transaction_user['kidsagegroup']!='nill']['Category'].value_counts()

trans=transaction[['User_id','Category','BRD_DESC']]

trans['y']=1

train_dummies=pd.get_dummies(trans[['User_id','Category']],columns=['User_id','Category'])

transaction['colon']='_'

trans['Category']=transaction['BRD_DESC']+transaction['colon']+transaction['Category']

contacts=transaction_user[['User_id','Contact_number']]

contacts['Contact_number']=contacts['Contact_number'].apply(lambda x:x.split('-')[1])

#generating user-item  and item-user matrix 

X_train_sparse=csr_matrix(train_dummies.values)

item_users=pd.get_dummies(trans[['User_id','Category']],columns=['User_id'])

item_users_grouped=item_users.groupby('Category').agg('sum')

item_users_sparse=csr_matrix(item_users_grouped.values)

user_items=pd.get_dummies(trans[['User_id','Category']],columns=['Category'])

user_items_grouped=user_items.groupby('User_id').agg('sum')

user_items_sparse=csr_matrix(user_items_grouped.values)

user_items_gp=user_items_grouped.reset_index()

# initialize a model
model = implicit.als.AlternatingLeastSquares(factors=50)

# train the model on a sparse matrix of item/user/confidence weights
model.fit(item_users_sparse)

from sklearn.externals import joblib
joblib.dump(model, 'reco_model_pickle')

del model

model=joblib.load('reco_model_pickle')


#for predicting new recommendations
#creating mapper
items=list(item_users_grouped.index)

item_dict={}
k=0
for i in items:
    item_dict[float(k)]=i
    k=k+1
    

#creating prediction dataframe
final_recs=user_items_gp[['User_id','Category_Arrow Jeans_Jeans']]

del final_recs['Category_Arrow Jeans_Jeans']


rec_arr=[]
for user in range(len(final_recs)):
    rec_list=list(model.recommend(user,user_items_sparse))
    t=pd.DataFrame(np.array(rec_list))[0][0:5].apply(lambda x:item_dict[x])
    ta=np.reshape(t, (1,len(t)))
   
    if rec_arr==[]:
        rec_arr=ta
    else:
        rec_arr=np.append(rec_arr,ta,axis=0)
        

recs=pd.DataFrame(rec_arr,columns=['Reco1','Reco2','Reco3','Reco4','Reco5'])

final_recs=pd.concat([final_recs,recs],axis=1)

final_recs=final_recs.merge(contacts,on='User_id',how='left')

final_recs=final_recs[[u'Contact_number',u'Reco1', u'Reco2', u'Reco3', u'Reco4', u'Reco5']]

final_recs=final_recs.reset_index()

final_recs['index']=final_recs['index']+1


final_recs.columns=[u'RecoID', u'Contact_number', u'Reco1', u'Reco2', u'Reco3', u'Reco4','Reco5']

final_recs.to_csv('Final_Recommendation.csv')
