import pandas as pd
import plotly.express as px

get_file = pd.read_csv('comptagevelo2012.csv', sep=",")
df = pd.DataFrame(get_file)

print("\n>>>> Head table:")
print(df.head())
print("\n>>>> Info table:")
print(df.info())
print("\n>>>> Describe table:")
print(df.describe())

# визначте загальну кількість велосипедистів за вибраний рік для всіх велодоріжок;
total_cyclists = 0
cyclists_by_ways = df.iloc[:, 2:].sum()
for count in cyclists_by_ways:
  total_cyclists += count
print(f"The total number of cyclists in 2012 year was {int(total_cyclists)}")

# визначте найбільш популярний місяць за кількістю велосипедистів для трьох обраних велодоріжок;
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
df["date_parse"] = pd.to_datetime(df.iloc[:, 0], errors="coerce", dayfirst=True)
df["months"] = pd.Categorical(df["date_parse"].dt.month_name(), categories=months, ordered=True)
group_by_month = df.groupby("months")[['Rachel / Papineau','Brébeuf','PierDup']].sum()
group_by_month["total"] = group_by_month.sum(axis=1).astype('Int64')
print(f"\n>>  Selected bike tracks:\n{group_by_month}")

months = group_by_month.nlargest(3, "total")
print(f"\nMost popular monthes:\n{months}")

# виконайте групування даних за місяцями та визначте динаміку використання однієї з велодоріжок.
bike_way = 'Rachel / Papineau'
way_rachel = group_by_month[bike_way]
way_rachel_popular = way_rachel.nlargest(1).values[0]
print(f"\nMost popular month >> {way_rachel.nlargest(1).index[0]} << on way - {bike_way}: - {way_rachel_popular} cyclists")

print(way_rachel)

# Побудуйте графік, який відображає зміну кількості велосипедистів на обраній велодоріжці за обраний рік за місяцями.s
fig = px.bar(
  way_rachel.reset_index(), 
  x="months", 
  y="Rachel / Papineau", 
  title=f"Most popular month >> {way_rachel.nlargest(1).index[0]}",
  color_discrete_sequence=["#2ca02c"])
fig.show()