

def add_data(list_values):
	with open('iris.csv','a') as f:
		
		f.write(','.join(list_values)+'\n')


def delete_data(list_values):
	import pandas as pd
	iris=pd.read_csv('iris.csv',header=None)
	data=iris.loc[(iris[0]==list_values[0]) & (iris[1]==list_values[1]) & (iris[2]==list_values[2]) & (iris[3]==list_values[3]) & (iris[4]==list_values[4])]
	if data.empty:
		return "Data is not in the dataset"
	df = pd.merge(iris, data, on=[0,1,2,3,4], how='outer', indicator=True).query("_merge != 'both'").drop('_merge', axis=1).reset_index(drop=True)
	#print len(df)
	df.to_csv('iris.csv',index=False)
	return "Deleta data successfully"

