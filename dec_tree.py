import pandas as pd 
from math import log
from sklearn.utils import shuffle
import csv
import pickle as pkl
import sys
import os
global iris
iris=pd.read_csv('iris.csv',header=None)
show=[]
count=0
class Tree(object):
	def __init__(self):
		self.left = None
		self.right = None
		self.name=None
		self.attr= None
		self.boundary=None
		self.type=None
		self.split=[]
	
	 

def find_diff(l):
	prev=l[0][1]
	tuples=[]
	boundaries=[]
	for i in range(1,len(l)):
		if l[i][1] == l[i-1][1]:
			prev=l[i][1]
		elif l[i][0] != l[i-1][0] :
			
				tuples.append((l[i][1],l[i-1][1]))
				boundaries.append((l[i][0]+l[i-1][0])/2)
		

			
	return tuples,boundaries


def find_opt_boundary(IG,attr,l):
	[tuples,boundaries]=find_diff(l)

	G=[]
	if tuples == []:
		return None
	for t in boundaries:
		G.append((IG-find_attr_entropy(attr,t,iris),t))
	
		
	return tuples[boundaries.index(max(G,key=lambda item:item[0])[1])],max(G,key=lambda item:item[0])[1],max(G,key=lambda item:item[0])[0]
		
def find_split_attr(attr_list,data):
	
	IG=find_entropy(data)
	potential_splits=[]
	for attr in attr_list:

		attr_l=data[[attr,4]].values
		attr_l=attr_l.tolist()
		attr_l.sort(key=lambda x: x[0])
		
			
		# if attr==2	:
		# 	print attr_l
		#import pdb;pdb.set_trace()
		opt=find_opt_boundary(IG,attr,attr_l)
		if opt != None:
			potential_splits.append((attr,opt[1],opt[2]))

	
	return max(potential_splits,key=lambda item:item[2])




def find_entropy(data):
	entropy=0
	for i in data[4].unique().tolist():
		pi=len(data.loc[data[4]==i])*1.0/len(data)
		entropy=entropy-pi*log(pi,2)
	return entropy


def find_attr_entropy(attr, boundary, data):
	a_entropy=0
	
	less=data.loc[data[attr]<boundary]
	more=data.loc[data[attr]>=boundary]

	a_entropy=(len(less)*1.0/len(data))*find_entropy(less)+(len(more)*1.0/len(data))*find_entropy(more)
	
	return a_entropy

def is_pure(data,threshold=0.08):
	if len(data[4].unique().tolist())==1:
		return True
	elif threshold!=0:
		if 1-(data[4].value_counts().max()*1.0/len(data))<=threshold:
			return True


	return False

def find_data_split(data):
	counts=data[4].value_counts()
	result=[0 for x in range (3)]
	try:
		result[0]=counts['Iris-setosa']
	except:
		result[0]=0
	try:
		result[1]=counts['Iris-versicolor']
	except:
		result[1]=0
	try:
		result[2]=counts['Iris-virginica']
	except:
		result[2]=0
	return result

def train_tree(prev,data,train=True):
	if train:
		root=Tree()
		global count
		
		if not data.empty:
			if is_pure(data):
				root.attr=data[4].value_counts().idxmax()
				#print data[4].unique().tolist()[0]
				root.split=data[4].value_counts().tolist()
				root.type='leaf'
				root.name=count
				root.split=find_data_split(data)
				count+=1
				show.append((root.name,root.left,root.right,root.attr,root.boundary,root.type,root.split))
				return root
			else:	
				attr_list=list(data.columns)[:-1]
				if( prev in attr_list):
					attr_list.remove(prev)


				(attr,boundary,e)=find_split_attr(attr_list,data)
				#print attr,boundary
				root.split=data[4].value_counts().tolist()
				root.type='decision'
				root.attr=attr
				root.boundary=boundary
				root.split=find_data_split(data)
				root.name=count
				count+=1
				root.left=train_tree(attr,data.loc[data[attr]<boundary])
				root.right=train_tree(attr,data.loc[data[attr]>=boundary])
				show.append((root.name,root.left.name,root.right.name,root.attr,root.boundary,root.type,root.split))
				
				return root
	else:
		root=pkl.load(open('tree.pkl','r'))
		return root

def test(data, tree):
	acc=0
	root=tree
	for index, row in data.iterrows():
		
		
		while tree.type!='leaf':
			if row[tree.attr]<=tree.boundary:
				
				tree=tree.left
			else:
				
				tree=tree.right
		if tree.attr != row[4]:
			acc=acc+1
		tree=root
	
	return acc
def classify_file(data, tree):
	
	results=[]
	root=tree
	for index, row in data.iterrows():
		
		
		while tree.type!='leaf':
			if row[tree.attr]<=tree.boundary:
				
				tree=tree.left
			else:
				
				tree=tree.right
		results.append(tree.attr)
		tree=root
	
	return results

def is_valid(tup, flag=False):
	inval=[]
	ranges=[]
	output=''
	
	if flag:
		for t in range(0,4):
			try:
				tup[t]=float(tup[t])
			except ValueError:
				return 'First four attributes must be numbers!'
	else:
		for t in range(0,4):
			try:
				tup[t]=float(tup[t])
			except ValueError:
				return 'All attributes must be numbers!'
	for i in range(0,4):
		ranges.append([iris[i].min(),iris[i].max()])
	for t in range(0,4):
		if tup[t] >= ranges[t][0] and tup[t] <= ranges[t][1]:
			pass
		else:
			inval.append(t)
	if flag:
		if tup[4] in iris[4].unique().tolist():
			pass
		else:
			output=output+'Class is invalid. Should be one of '+' '.join(iris[4].unique().tolist())+'\n'
		if inval != []:
			for i in inval:	
				output=output+'Attribute '+str(i)+' is invalid. Should be in range ['+str(ranges[i][0])+','+str(ranges[i][1])+']'+'\n'
	else:
		if inval != []:
			for i in inval:	
				output=output+'Attribute '+str(i)+' is invalid.\n Should be in range ['+str(ranges[i][0])+','+str(ranges[i][1])+']'+'\n'
	return output

def test_file(path,tree):
	if not os.path.isfile(path):
		return 'Invalid Path!'
	else:
		data=pd.read_csv(path,header=None)
		results=classify_file(data,tree)
		
		result='Results are:\n'
		for r in results:
			result=result+r+'\n'
		return result
		
def classify_one(data, tree):
	root=tree
	while root.type!='leaf':
		if data[root.attr]<=root.boundary:
				
			root=root.left
		else:				
			root=root.right
	return root.attr


if __name__ == "__main__":
	
	if len(sys.argv)>1:
		if sys.argv[1]=='True':
			train=True
		else:
			train=False
	else:
		train=False
	
	
	iris=shuffle(iris)
	root=train_tree(-1,iris[0:120],train)
	pkl.dump(root,open('tree.pkl','w'))
	print 'Accuracy: ' ,(1-test(iris[120:150],root)*1.0/30)*100,"%"
	if train:
		csvfile=file('dec_tree.csv','wb')
		writer=csv.writer(csvfile)
		writer.writerow(['Name','left_child','right_child','Attribute','boundary','type'])
		writer.writerows(show)
		csvfile.close()
	#import pdb;pdb.set_trace()
	#print test_file('./test2.csv',root)
	#print is_valid(['1','2','4','4','dfsdf'],True)

	#print classify_one({0:2,1:1,2:3,3:4},root)


