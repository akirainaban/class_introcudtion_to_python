#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 15:17:00 2019

@author: akirainaba
"""

"""
Task 1: Read data from a comma-separated (csv) file 
which contains the customers’ information (i.e., the two given input files) 
and check whether there are any problems with the data 
(i.e. perform validation).

"""


import pandas as pd
import copy 
balances = pd.read_csv('balances_day_beginning.csv')
transactions = pd.read_csv("daily_transactions.csv")

"""
Check the type of each column
If there are any non-suitable type, the function will send an error message
memo:dataframe.dtypese[column-No.] shows type of the column
"""

def check_data(balance_data, transaction_data):
    if balance_data.dtypes[0] != "int":
        print("Error: 'Account number' in the file should be integer")
    elif balance_data.dtypes[1] != "float":
        print("Error: 'Balance(£)' in the file should be float")
    elif transaction_data.dtypes[0] != "int":
        print("Error: 'Timestamp' in the file should be integer")
    elif transaction_data.dtypes[1] != "int":
        print("Error: 'Outgoing Account' in the file should be integer")
    elif transaction_data.dtypes[2] != "int":
        print("Error: 'Ingoing Account' in the gile should be integer")
    elif transaction_data.dtypes[3] != "float":
        print("Error: 'Amount(£)' in the file should be float")
    else:
        print("The data in the files have correct types !")


check_data(balances, transactions)










"""
Task 2: Calculate the new (temporary) balance of each customer according to 
the transactions given as input. 
    
Balances can be negative at this stage. 

The output is a new csv file containing account numbers and new balances
where the account numbers are ordered increasingly by code. 
"""


"""
Detect the account numbers of both outgoing and ingoing accounts
minus or plus to the original balance 
memo:dataframe.loc("column-name" == specific name) detects the row or cell which
    has the specific data
memo:copy.deepcopy avoid changing the original data
"""



def cal_temp_balance (balance_data, transaction_data):
    balance_data_cp = copy.deepcopy(balance_data)
    transaction_data_cp = copy.deepcopy(transaction_data)
    for i in range(len(transaction_data_cp)):
        out_ac = transaction_data_cp.iloc[i][1].astype(int)
        in_ac = transaction_data_cp.iloc[i][2].astype(int)
        balance_data_cp.loc[balance_data_cp["Account Number"] == out_ac,' Balance (£)'] \
        = balance_data_cp.loc[balance_data["Account Number"] == out_ac,' Balance (£)'] - transaction_data_cp.iloc[i][3]
        balance_data_cp.loc[balance_data_cp["Account Number"] == in_ac,' Balance (£)'] \
        = balance_data_cp.loc[balance_data["Account Number"] == in_ac,' Balance (£)'] + transaction_data_cp.iloc[i][3]
    return(balance_data_cp.sort_values(by = "Account Number"))
    

print("The balance of each accounts at the end of the day are \n",cal_temp_balance(balances, transactions))
cal_temp_balance(balances, transactions).to_csv("balance_task2.csv")








"""
Task 3: Detect any accounts with a negative balance and remove transactions 
        from the system in order for the condition that all balances 
        be non-negative to be satisfied. 
        The algorithm consists of the following three steps:
            
Step 1: Find the account with the most negative balance. 
        If none exists, the algorithm halts. 
        Otherwise, go to step 2.
Step 2: Remove the latest outgoing transactions (according to their timestamp)
        from this account until its balance becomes non-negative.
Step 3: Update the balance of all the accounts. Go to step 1.

"""


"""
The function roles according to the above steps
memo:dataframe.iat[row-No.,column-No.] finds the cell which maches the those No.
memo:in dataframe each row has the name, which called index
memo:dataframe.index returns the dataframe of the index
memo:dataframe.index["index name"] returns the row whose index is same as "condeition"

"""

def delete_transaction_task3(balance_data, transaction_data):
    temp_balance_cp = copy.deepcopy(cal_temp_balance(balance_data, transaction_data).sort_values(by = " Balance (£)"))
    temp_transaction_cp = copy.deepcopy(transaction_data.sort_values(by = "Time", ascending = False))
    while temp_balance_cp.iat[0,1] < 0:
        latest_out_ac = temp_balance_cp.iat[0,0].astype(int)
        index = 0
        while temp_transaction_cp[" Outgoing Account"][temp_transaction_cp.index[index]] != latest_out_ac:
            index += 1
        temp_transaction_cp = temp_transaction_cp.drop(temp_transaction_cp.index[index])
        temp_balance_cp = cal_temp_balance(balance_data, temp_transaction_cp).sort_values(by = " Balance (£)")
        
    return(temp_balance_cp.sort_values(by = "Account Number"), temp_transaction_cp.sort_values(by = "Time"))
    
balance_3 = delete_transaction_task3(balances, transactions)[0]
transaction_3 = delete_transaction_task3(balances, transactions)[1]
print("The result of Balances in Task3 are\n",balance_3,"\n The result of remained transactions in Task3 are\n", transaction_3)
balance_3.to_csv("balance_task3.csv")
transaction_3.to_csv("transaction_task3.csv")






"""

Task 4: Similar to Task 3, but with a new algorithm which does the following:
With the data taken from Task 1 and 2, block the smallest number possible of
transactions in order for the condition that all balances be non-negative to be satisfied.

"""

"""
Minus and has only one transfer as an outgoing account call MOO_ac 
(Minus bocause of the Only One)
These kinda transactions should be extracted
->MOO_ac_check()
"""
    
"""
Step1: Delete MOO_ac
Step2: If none account has negative value, the algorithm will stop and show 
    the result(the balance at the end of the day with the transactions)
    Otherwise, go to Step3
Step3: Find the biggest transactin from the negative-account
Step4: Check the ingoing account and if its balance is smaller than the amount of transaction,
    go Step5
    Otherwise, go to Step6
Step5: Chose the next biggest amount transaction
    If such transaction does not exist, go to Step6
    Otherwise, go back to Step4
Step6: Subtract current transaction from the original the list of taransactions, 
    and go back to Step2
"""
"""
memo: dataframe.loc does not accept the PLURAL conditions(e.g. list or dataframe),
    in that case, .isin should be used to detect the row or cell which contains 
    the specific name or value
memo: In the if or while statements, the dataframe should not be used,
    cos the return (bool value) would be stored in the dataframe and not used appropriately
"""
            
    
def MOO_ac_check(balance_data, transaction_data):
    balance_cp = copy.deepcopy(cal_temp_balance(balance_data, transaction_data))
    transaction_cp = copy.deepcopy(transaction_data)
    MOO_ac = -1
    for i in range(len(balance_cp["Account Number"])):
        temp = balance_cp["Account Number"][i]
        if balance_cp[" Balance (£)"][i] < 0 \
        and len(transaction_cp["Time"].loc[transaction_cp[" Outgoing Account"] == temp]) == 1:
            MOO_ac = balance_cp["Account Number"].iat[i]
    return(MOO_ac)


    
def delete_transaction_task4(balance_d, transaction_d):
    balance_data = copy.deepcopy(balance_d)
    temp_transaction = copy.deepcopy(transaction_d)
    while MOO_ac_check(balance_data, temp_transaction) != -1:
        temp = MOO_ac_check(balance_data, temp_transaction)
        temp_transaction = temp_transaction.loc[temp_transaction[" Outgoing Account"] != temp]
    temp_balance = cal_temp_balance(balance_data, temp_transaction).sort_values(by = " Balance (£)")
    while temp_balance.iat[0,1] < 0:
        negative_ac = temp_balance["Account Number"].loc[temp_balance[" Balance (£)"] < 0 ]
        transaction_negative = temp_transaction[temp_transaction[" Outgoing Account"].isin(negative_ac)].sort_values(by = " Amount ()", ascending = False)
        i = 0
        while transaction_negative.iat[i,3] > temp_balance[temp_balance["Account Number"] == transaction_negative.iat[i, 2]].iat[0,1]:
            if i == len(transaction_negative) - 1:
                i = 0
                break
            else:
                i += 1
        subtract_index = transaction_negative.index[i]
        temp_transaction = temp_transaction.drop(subtract_index)
        temp_balance = cal_temp_balance(balance_data, temp_transaction).sort_values(by = " Balance (£)")
    return(temp_balance.sort_values(by = "Account Number"), temp_transaction)


balance_4 = delete_transaction_task4(balances, transactions)[0]
transaction_4 = delete_transaction_task4(balances, transactions)[1]
print("The result of Balances in Task4 are\n",balance_4,"\n The result of remained transactions in Task4 are\n", transaction_4)
balance_4.to_csv("balance_task4.csv")
transaction_4.to_csv("transaction_task4.csv")


