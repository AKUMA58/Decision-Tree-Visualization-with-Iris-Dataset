import csv 
import os
from PIL import Image

def next_point(dectree,node_from,a,b,c,d):
	if int(dectree[node_from][3])==0:
		e=a
	if int(dectree[node_from][3])==1:
		e=b
	if int(dectree[node_from][3])==2:
		e=c
	if int(dectree[node_from][3])==3:
		e=d
	if float(e)<float(dectree[node_from][4]):
		return int(dectree[node_from][1])
	else:
		return int(dectree[node_from][2])

def attribute(i):
	if int(i) ==0:
		return "sepal length in cm"
	if int(i) ==1:
		return "sepal width in cm"
	if int(i)==2:
		return "petal length in cm"
	if int(i) ==3:
		return "petal width in cm"

def draw_path_tree(a,b,c,d):
	csvfile=open("dec_tree.csv","r")
	reader=csv.reader(csvfile)
	gv_file=open('tree_path.gv','w')
	gv_file.write("digraph Tree{node[shape=box];")
	dectree=[]
	orderdectree=[]
	path=[]
	parent=dict()
	root=-1
	for row in reader:
		if reader.line_num==1:
			continue
		dectree.append(row)
	csvfile.close()
	#find parent
	for i in range (len(dectree)):
		j=dectree[i][0]
		if dectree[i][1]!='':
			parent[(dectree[i][1])]=j
		if dectree[i][2]!='':
			parent[(dectree[i][2])]=j
	#find root
	for j in range (len(dectree)):
		if str(j) not in parent:
			root=j
	for i in range (len(dectree)):
		for j in range (len(dectree)):
			if int(dectree[j][0])==i:
				orderdectree.append(dectree[j])
	#find path
	node_from=root
	while orderdectree[node_from][5]!='leaf':
		node_to=next_point(orderdectree,node_from,a,b,c,d)
		path.append((node_from,node_to))
		node_from=node_to
	#draw nodes
	for i in range (len(dectree)):
		gv_file.write(str(orderdectree[i][0]))
		if orderdectree[i][5]=='leaf':
			gv_file.write('[label='+'"'+orderdectree[i][3]+'"''];')
		if orderdectree[i][5]=='decision':
			gv_file.write('[label='+'"'+attribute(orderdectree[i][3])+'\n<'+orderdectree[i][4]+'      >='+orderdectree[i][4]+'"'+'];')
	# #draw lines
	for j in range (len(dectree)):
		if j!=root:
			gv_file.write(str(parent['%i'%j])+'->'+str(j)+'[labeldistance=2.5,')
			for k in range (len(path)):
				if int(path[k][0])==int(parent['%i'%j]) and int(path[k][1])==j:
					gv_file.write('color="red",')
			if int(orderdectree[int(parent['%i'%j])][1])==j:
				gv_file.write('labellangle='+str(45)+'];')
			if int(orderdectree[int(parent['%i'%j])][2])==j:
				gv_file.write('labellangle='+str(-45)+'];')
	gv_file.write('}')
	gv_file.close()
	os.system('dot tree_path.gv -Tpng -o tree_path.png')
	im=Image.open('tree_path.png')
	nim=im.resize((800,550))
	nim.save('tree_path.png',quality=300)
	return orderdectree[node_from][3]
# dc=draw_path_tree(6.9,3.1,5.4,2.1)
# print dc
	
