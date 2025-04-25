import pandas as pd
from matplotlib import matplotlib.pyplot as plt
import streamlit as st 

def barchart(borough,years):
	columns_to_plot = pivot_table.columns[:-1]
	pivot_table_without_total = pivot_table[columns_to_plot]
	fig, ax = plt.subplots()
	ax.set_ylabel('Number of Empty Houses in 2018')
	if borough=="All boroughs":
		if years=="All timeframes":
			pivot_table_without_total.iloc[:-1].plot(kind='bar', figsize=(10, 6),ax=ax)
		else:
			pivot_table[years].iloc[:-1].plot(kind='bar', figsize=(10, 6),ax=ax)
		ax.set_title('Number of Empty Houses by Borough')
		ax.set_xlabel('Boroughs of London')
	else:
		row_to_plot=pivot_table_without_total.loc[borough]
		row_to_plot.plot(kind='bar', figsize=(10, 6),ax=ax)
		ax.set_title('Number of Empty Houses in '+ borough)
		ax.set_xlabel('Timeframe')
	plt.xticks(rotation=45,ha="right")
	#plt.legend(title='Empty Status')
	plt.tight_layout()
	st.pyplot(fig)

def boxplot():

#------prepare the dataset--------
	columns_to_boxplot = pivot_table.columns[:-2]  # Exclude the last two columns ('Grand Total' and 'Unknown')
	boxplot_to_filter = pivot_table[columns_to_boxplot].iloc[:-1]#<---no last row
	filtered_boxplot = boxplot_to_filter[boxplot_to_filter <=outlier]
	labels=pivot_table.columns[:-2].tolist()

#-----prepare the boxplot chart
	boxprops = dict(linestyle='-', linewidth=2.5, color='darkgoldenrod') # Define box properties (color)
	medianprops = dict(linestyle='-', linewidth=2.5, color='firebrick') # Define median line properties (color)
	fig, ax=plt.subplots(figsize=(6, 9))
	ax.set_title('Distribution of Empty Houses for each borough by time period')
	ax.set_xlabel('Years unoccupied')
	ax.set_ylabel('Number of Empty Houses in 2018')
	plt.xticks(ha='right')
	plt.tight_layout()

	ax.boxplot(
		[filtered_boxplot[col].dropna().values for col in pivot_table.columns[:-2]],
		labels= labels,
		patch_artist=True,  # Enable filled boxes for color
		boxprops=boxprops, # Apply box properties
		medianprops=medianprops # Apply median properties
	   )
	st.pyplot(fig)

def pie_chart(borough):
	
#--------prepare the pie chart---------
	if borough=="All boroughs":borough="All London"
	filtered_pivot_table = pivot_table.loc[pivot_table.index == borough].iloc[:, :-1]
	sizes=filtered_pivot_table.values.tolist()[0]
	labels =filtered_pivot_table.columns.tolist()

# Create the pie chart
	fig, ax = plt.subplots( figsize=(6, 6))
	ax.pie(
		sizes,
		labels=labels,
		autopct='%1.1f%%',  # Show percentages
		startangle=90,  # Start at the top
	)
	ax.set_title('Empty houses by years in '+borough)
	st.pyplot(fig)

#---------main program----------------

df = pd.read_csv("EmptyHouses.csv")

pivot_table = df.pivot_table(
    index='Borough',
    columns='Empty',
    values='GLAID',
    aggfunc='count',
    margins='True',
    margins_name='All London'
    )
pivot_table = pivot_table.rename(columns={'All London': 'All years'})
pivot_table.fillna(0, inplace=True)
st.set_page_config(layout="wide")
st.header("Statistics on Empty Houses in London in 2018")
col1, col2, col3 = st.columns([1,3,1])
#-----This remove the last column from pivot_table ------
#-----.iloc[:-1] takes away the last row too!
columns_to_plot = pivot_table.columns[:-1]
pivot_table_without_total = pivot_table[columns_to_plot].iloc[:-1]  # Exclude the last row ('Grand Total')

boroughs_list=['All boroughs']
for items in pivot_table.index.tolist():
	boroughs_list.append(items)
empty_bins=['All timeframes']
for items in pivot_table.columns.tolist():
	empty_bins.append(items)

with col1:
	outlier = st.slider("Outlier control: No value over?", 0, 1300, step=100,value=1200)
	years=st.selectbox("Filter by years", empty_bins,index=1)
	boxplot()

with col2:
	borough=st.selectbox("Filter by borough", boroughs_list,index=0)
	barchart(borough,years)
with col3:
	pie_chart(borough)
	st.write(pivot_table.loc[pivot_table.index == borough].T)
