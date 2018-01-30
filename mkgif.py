import matplotlib.pyplot as plt
import imageio,os
from PIL import Image
images = []
filenames=[]
count=0
for fn in os.listdir('pic/'):
	count+=1
for i in range (count):
	filenames.append('ori_tree_'+str(i)+'.png')
for filename in filenames:
	im=Image.open('pic/'+filename)
	nim=im.resize((950,550))
	nim.save('pic/'+filename,quality=300)
	images.append(imageio.imread('pic/'+filename))
imageio.mimsave('ori_tree.gif', images,duration=2)