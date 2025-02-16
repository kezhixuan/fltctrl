import pandas as pd
import re


data = {
    "Me1": ["Row1", "1", "2", "3"],
    "Me2": [1, 4, 5, None],
    "Me3": ["Row3", "7", "7", "8"],
}

df = pd.DataFrame(data)

df = df.assign(Me5=["Row4", "3", "3", "#3"])
print(df)

df.rename(columns={"Me3": "Me2"}, inplace=True)

BAD_CHARS = [".", "&", "(", ")", ";", "-"]
pat = "|".join(["({})".format(re.escape(c)) for c in BAD_CHARS])


df = df.drop(df.filter(regex=("[^.\s]+\.[^.\s]")), axis=1)
# df = df.drop(list(df.filter(regex=('[^.\s]+\.[^.\s]'))),axix=1)


convert_dict = {"Me2": str}


df = df.astype(convert_dict)
df = df.T.reset_index()
df = df.groupby(df.columns, axis=1).apply(
    lambda x: x.apply(lambda y: ",".join([l for l in y if l is not None]), axis=1)
)

print(df)


datedata = {
    "Index": [1, 2, 3],
    "RefreshDate": ["2023/10/31", "2023/09/09", "2023/08/08"],
}

dateDF = pd.DataFrame(datedata)
dateDF["RefreshDate"] = pd.to_datetime(
    dateDF["RefreshDate"].astype(str), format="%Y/%m/%d"
)
# dataDf.add({4,"2023/01/01"})
print(dateDF.dtypes)
print(dateDF)
