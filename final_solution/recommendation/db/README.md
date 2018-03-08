All the DB related files that bring up and would also help in tearing down the MySQL schema. There are two tables being used:
<br/>
1. LoyaltyCheck - Stores the customer phone no entered at the kiosk for retrieving the loyalty points accumulated
2. Reco - Stores the pre-calculated top 5 recommendations for a particular customer

reco_model_pickle - Contains trained recommendation model
<br/>
reco_training_scoring - For training the model and generating top 5 recommendation
<br/>
Final_Recommendations - Static file of Top 5 recommendations generated for each customer.
