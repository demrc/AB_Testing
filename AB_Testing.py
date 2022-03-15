import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

#Part 1

df_t_ = pd.read_excel("ab_testing.xlsx" , sheet_name = "Test Group") #Step1
df_k_ = pd.read_excel("ab_testing.xlsx" , sheet_name = "Control Group")

df_t = df_t_
df_k = df_k_

df_t.groupby(["Click","Purchase"]).agg({"Earning":"mean"}).head() #Step2

df_t["Purchase"].mean()

df_k.groupby(["Click","Purchase"]).agg({"Earning":"mean"}).head()

df_k["Purchase"].mean()

#When we examined the test and control groups, although Click numbers were higher in the control group than in the test group.
#Purchase and Earning values are higher in the test group in the first 5 observations. We can see the certainty of this after the EU test.

df_k["Group"]="K" #Step 3
df_t["Group"]="T"
df = pd.concat([df_k, df_t], ignore_index=True)

#Part2

#Step 1
#Hipotez
#H0:M1=M2(Kontrol grubu ve test grubu satın alma ortalamaları arasında fark yoktur.)
#H1:M1!=M2M1=M2(Kontrol grubu ve test grubu satın alma ortalamaları arasında fark vardır.)

df.groupby("Group").agg({"Purchase":"mean"})

#Normalization Hypothesis
test_stat, pvalue = shapiro(df.loc[df["Group"]=="K","Purchase"])
print("Test Stat = %.4f, p-value = %.4f" %(test_stat,pvalue))

test_stat, pvalue = shapiro(df.loc[df["Group"]=="T","Purchase"])
print("Test Stat = %.4f, p-value = %.4f" %(test_stat,pvalue))

#Normallik varsayımı testi uyguladığımızda ortaya çıkan p değerlerine göre normallik varsayımı sağlanmaktadır.
#Yani H0 reddedilemez.

#Variance Hypothesis
test_stat, pvalue = levene(df.loc[df["Group"]=="T","Purchase"],df.loc[df["Group"]=="K","Purchase"])
print("Test Stat = %.4f, p-value = %.4f" %(test_stat,pvalue))

# Varyans hipotezi testi uyguladığımızda ortaya çıkan p değerlerine göre varyans hipotezi sağlanmaktadır.
#Yani H0 reddedilemez.

#Step 2

test_stat, pvalue = ttest_ind(df.loc[df["Group"]=="K","Purchase"],df.loc[df["Group"]=="T","Purchase"],equal_var=True)
print("Test Stat = %.4f, p-value = %.4f" %(test_stat,pvalue))

#Elde edilen p-value değerine göre kontrol ve test grubu ortalamaları arasında istatistiki olarak kayda değer bir fark
#yoktur. p<0.05 değerini sağlamadığı için H0 reddedilememektedir. Hipotez doğrudur.

#Part 3

#Step 1
#Her iki hipotez veriler için sağlanmaktadır. Tüm varsayımların sağlandığı durumlarda kullanacağımız test türü parametrik
# test için kullanılan "ttest_ind" olacaktır.

#Step 2
#Mevcut olarak kullanılan yöntemi değiştirmek kayda değer bir satın alma farkı gözükmemektedir. Yeni yönteme ayrılacak 
#bütçenin müşteriler için kampanyalara veya reklamlara aktarılabilir.
