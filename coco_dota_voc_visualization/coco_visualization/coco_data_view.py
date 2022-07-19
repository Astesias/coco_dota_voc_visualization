import json
import cv2
import os
import numpy as np

def bgr2rgb(t):
    t=list(t)
    t[0],t[2]=t[2],t[0]
    return tuple(t)
    
def cv2_imread(filePath):
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    return cv_img

def label_img(nparry,bbox,category_id):
    colors={'cyan':(0,255,255),'blue':(0,0,255),'white':(255,255,255),
        'red':(255,0,0),'yellow':(255,255,0),'green':(0,255,0),'black':(0,0,0)}
    img=nparry
    x=int(bbox[0])
    y=int(bbox[1])
    w=int(bbox[2])
    h=int(bbox[3])
    left_top=(x,y)
    right_bottom=(x+w,y+h)
    
    if category_id%7==1:
        color=colors['cyan']
    if category_id%7==2:
        color=colors['blue']
    if category_id%7==3:
        color=colors['white']
    if category_id%7==4:
        color=colors['red']
    if category_id%7==5:
        color=colors['yellow']
    if category_id%7==6:
        color=colors['green']
    if category_id%7==0:
        color=colors['black']
    color=bgr2rgb(color) 
    cv2.rectangle(img, left_top, right_bottom,color, 2)
    cv2.putText(img, names[category_id-1], left_top,cv2.FONT_HERSHEY_TRIPLEX,0.4,bgr2rgb(colors['green']),1)
    
    return img

def coco_viewer(json_dir,img_dir,rate,index):
    
    if img_dir[-1]!= '/' or img_dir[-1]!='\\':
        img_dir+='/'
    
    with open(json_dir,'r') as fp:    
        a=json.load(fp) 
    
    images=a['images']
    annotations=a['annotations']
    categories=a['categories']
    # pdb.set_trace()
    global names
    names=[None for i in range(len(categories))]
    for cate in categories:
        if cate['name'] not in names:
            names[int(cate['id'])-1]=cate['name']
            
    new_pic_flag=1
    _=1
    for annoer in annotations[index:]:
        
        box=annoer['bbox']
        img_id=annoer['image_id']
        clas=annoer['category_id']
        box=list(map(lambda x:x*rate,box))
        img_name=images[img_id]['file_name']

        
        if _:
            fr_img_name=img_name
            _=0
            
        if img_name!=fr_img_name:
            new_pic_flag=1
            cv2.imshow(fr_img_name,img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()  
            print()
            
        if new_pic_flag:
            img=cv2_imread(img_dir+img_name)
            new_pic_flag=0
            if rate and rate!=1 :
                img=cv2.resize(img,(int(rate*img.shape[1]),int(rate*img.shape[0])),interpolation=cv2.INTER_LINEAR)
                
        print('filename:{} box:{} class: {}'.format(img_name,box,names[clas-1]))
        img=label_img(img,box,clas)
        fr_img_name=img_name
 

if __name__ == '__main__':
    
    # example1:
    if 1:
        ann_dir='ann1/train.json'
        img_dir='img1/'
        rate=2
        index=4
        
    # example2:
    else:
        ann_dir='ann2/train.json'
        img_dir='img2/'
        rate=2
        index=1
        
    
    coco_viewer(ann_dir,img_dir,rate=rate,index=index) 
    #   json_dir|img_dir|scale_rate|start_index 
    
    # press any key to view next
     
