#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pandas')
get_ipython().system('pip install mysql-connector-python')


# In[1]:


import mysql.connector
import pandas as pd
import csv
import datetime
import numpy as np


# In[2]:


db = mysql.connector.connect(
  host="localhost",
  port = 3306,  
  user="root",
  password="",
  database="intellithon",
  use_unicode=True
)


# In[3]:


mycursor = db.cursor(buffered=True)
mycursor.execute("Show databases;")


# In[4]:


mycursor.fetchall()


# In[63]:


mycursor.execute("select DISTINCT(a.id),a.name,a.idea_submit,b.teamname from int_users a inner join int_team b on a.id=b.leaderid WHERE a.id >'{}'ORDER BY a.id ASC".format(37))
df = pd.DataFrame(mycursor,columns = ['id', 'name', 'idea submiited', 'team name'])
df.to_csv('check.csv')
new_col = ['email','Phone','gender','state','city','org','utype','profile pic','status','password','hashcode','dob','address','v1','v2','v3','v4','added_on']
df[new_col]=np.nan
df.head(2)


# In[64]:


id = df['id']
ideasub = df['idea submiited']
ideasub
# id


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[65]:


counter = 0
def check(x):
    global counter
    if x == 1:
        mycursor.execute("SELECT * FROM int_users WHERE id = {} ".format(id[counter]))
        #print(list(mycursor.fetchall()[0][2:-1]))
        df.loc[counter,new_col]= (mycursor.fetchall()[0][2:-1])
        #print(df.iloc[counter])
    counter+=1
    

ideasub.apply(check)


# In[66]:


df.head(10)


# In[67]:


counter=0
df['Team Mentor']=np.nan
def check1(x):
    global counter
    if x == 1:
        mycursor.execute("SELECT tmname,uytpe,id FROM `int_team` WHERE `leaderid` LIKE {} ORDER BY `leaderid` DESC ".format(id[counter]))
        for i,(j,k,l)  in enumerate(mycursor.fetchall() ,start=1 ):
            if k == 'Team Member':
                col_name = [k +' '+ str(i),k +' '+ str(i)+' id']
                df.loc[counter , col_name] = [j,l]
                
            else:
                df.loc[counter , k] = j
        
            
        
    counter+=1
ideasub.apply(check1)


# In[69]:


df.to_csv('newdb.csv')


# In[37]:


df2 = pd.DataFrame(l)


# In[85]:


df.iloc[9]


# In[22]:


df2.to_csv('checking.csv')


# In[135]:


counter=0
col_name = ['psid','idea_title','idea_approach','idea_desc','idea_doc1','youtube_link','added_on']
def check2(x):
    global counter
    if x == 1:
        mycursor.execute("SELECT psid,idea_title,idea_approach,idea_desc,idea_doc1,youtube_link,added_on FROM `int_idea` WHERE `userid` = {} ORDER BY id ASC".format(id[counter]))
        a = (mycursor.fetchall())
        #print(a)
        if (a != []) :
               df.loc[counter , col_name] = a
        else:

                for i in range(1,6):
                    if not(np.isnan(df['Team Member '+str(i)+' id'].iloc[counter])) :
                        a = mycursor.execute("SELECT psid,idea_title,idea_approach,idea_desc,idea_doc1,youtube_link,added_on FROM `int_idea` WHERE `userid` = {} ORDER BY id ASC".format(df['Team Member '+str(i)+' id'].iloc[counter]))
                        if (a != []):
                            df.loc[counter , col_name] = a
                            break
        
                    
   
                
        
            
        
    counter+=1
ideasub.apply(check2)


# In[111]:


mycursor.execute("SELECT psid,idea_title,idea_approach,idea_desc,idea_doc1,youtube_link,added_on FROM `int_idea` WHERE `userid` = {} ORDER BY id ASC".format(9))
print((mycursor.fetchall()))
if len(mycursor.fetchall()) != 0 :
    print('hey')


# In[141]:


df.drop(['password','v1','v2','v3','v4'], axis=1 , inplace=True)


# In[142]:


df.iloc[9]


# In[ ]:




