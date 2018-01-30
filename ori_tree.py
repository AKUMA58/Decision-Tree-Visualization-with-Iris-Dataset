import csv 
import os
import shutil
from PIL import Image

def attribute(i):
	if int(i) ==0:
		return "sepal length in cm"
	if int(i) ==1:
		return "sepal width in cm"
	if int(i)==2:
		return "petal length in cm"
	if int(i) ==3:
		return "petal width in cm"

def draw_ori_tree():
	csvfile=open("dec_tree.csv","r")
	reader=csv.reader(csvfile)
	gv_file=open('ori_tree.gv','w')
	gv_file.write("digraph Tree{node[shape=box];")
	shutil.rmtree('pic')
	os.mkdir('pic')
	dectree=[]
	orderDectree=[]
	parent=dict()
	root=-1
	for row in reader:
		if reader.line_num==1:
			continue
		dectree.append(row)
	csvfile.close()

	for i in range (len(dectree)):
		j=dectree[i][0]
		if dectree[i][1]!='':
			parent[(dectree[i][1])]=j
		if dectree[i][2]!='':
			parent[(dectree[i][2])]=j
	for j in range (len(dectree)):
		if str(j) not in parent:
			root=j
	#sort nodes
	for i in range (len(dectree)):
		for j in range (len(dectree)):
			if int(dectree[j][0])==i:
				orderDectree.append(dectree[j])
	for i in range (len(orderDectree)):
		gv_file.write(str(orderDectree[i][0]))
		if orderDectree[i][5]=='leaf':
			gv_file.write('[label='+'"'+orderDectree[i][3])
		if orderDectree[i][5]=='decision':
			gv_file.write('[label='+'"'+attribute(orderDectree[i][3])+'\n<'+orderDectree[i][4]+'      >='+orderDectree[i][4])
		gv_file.write('\n'+orderDectree[i][6]+'"'+'];')
		if i!=root:
			gv_file.write(str(parent['%i'%i])+'->'+str(i)+'[labeldistance=2.5,')
			if int(orderDectree[int(parent['%i'%i])][1])==i:
				gv_file.write('labellangle='+str(45)+'];')
			if int(orderDectree[int(parent['%i'%i])][2])==i:
				gv_file.write('labellangle='+str(-45)+'];')			
		gv_file.write('}')
		gv_file.close()
		os.system('dot ori_tree.gv -Tpng -o pic/ori_tree_'+str(i)+'.png')
		gv_file=open('ori_tree.gv','a+')
		gv_file.seek(-1,os.SEEK_END)
		gv_file.truncate()
	gv_file.write('}')	
	gv_file.close()
	os.system('dot ori_tree.gv -Tpng -o ori_tree.png')
	im=Image.open('ori_tree.png')
	nim=im.resize((800,550))
	nim.save('ori_tree.png',quality=300)

draw_ori_tree()


	
