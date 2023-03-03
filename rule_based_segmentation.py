import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv(r'persona.csv')

df.info()


def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)


check_df(df)

cat_cols = [col for col in df.columns if df[col].dtypes in ["object", "category", "bool"]]

num_cols = [col for col in df.columns if col not in cat_cols]

num_but_cat = [col for col in df.columns if df[col].nunique() < 10 and df[col].dtypes in ["int64", "float64"]]

cat_but_car = [col for col in df.columns if df[col].nunique() > 20 and df[col].dtypes in ["object", "category"]]

cat_cols = cat_cols + num_but_cat

df[cat_cols].nunique()


def cat_summary(dataframe, col_name, plot=False):
    print(pd.DataFrame({col_name: dataframe[col_name].value_counts(),
                        "Ratio": 100 * (dataframe[col_name].value_counts()) / len(dataframe)}))
    print("##################################")


for i in cat_cols:
    cat_summary(df, i)


def cat_summary_with_plt(dataframe, col_name, plot=False):
    print(pd.DataFrame({col_name: dataframe[col_name].value_counts(),
                        "Ratio": 100 * (dataframe[col_name].value_counts()) / len(dataframe)}))
    print("##################################")
    if plot:
        sns.countplot(x=dataframe[col_name], data=dataframe)
        plt.show(block=True)


for i in cat_cols:
    if df[i].dtypes == "bool":
        df[i] = df[i].astype(int)
        cat_summary_with_plt(df, i, plot=True)
    else:
        cat_summary_with_plt(df, i, plot=True)


def target_summary_with_cat(dataframe, target, categorical_col):
    print(df.groupby([categorical_col]).agg({target: ["mean", "sum", "count"]}))


for col in cat_cols:
    print(target_summary_with_cat(df, "PRICE", col))

df.groupby(["COUNTRY", "SOURCE"]).agg({"PRICE": "mean"})

agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE", ascending=False)

agg_df.reset_index(inplace=True)

agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], bins=[0, 18, 23, 30, 40, 70], labels=["0_18", "19_23", "24_30", "31_40", "41_70"])

agg_df["customers_level_based"] = ['_'.join(i).upper() for i in agg_df.drop(["AGE", "PRICE"], axis=1).values]

agg_df2 = agg_df[['customers_level_based', 'PRICE']]

agg_df2["customers_level_based"].value_counts()

agg_df2 = agg_df2.groupby("customers_level_based").agg({"PRICE": "mean"})

agg_df2.reset_index(inplace=True)

agg_df2["customers_level_based"].value_counts()

agg_df2["SEGMENT"] = pd.qcut(agg_df2["PRICE"], 4, labels=["D", "C", "B", "A"])

agg_df2.head()

def check_segment(user):
    segment = agg_df2[(agg_df2["customers_level_based"] == user)].reset_index(drop=True)
    print(segment["SEGMENT"][0])


# COUNTRIES: BRA, CAN, DEU, FRA, TUR, USA
# PHONE: ANDROID, IOS
# SEX: FEMALE, MALE
# LABELS: 0_18, 19_23, 24_30, 31_40, 41_70


check_segment("BRA_ANDROID_FEMALE_0_18")
check_segment("TUR_IOS_MALE_24_30")


