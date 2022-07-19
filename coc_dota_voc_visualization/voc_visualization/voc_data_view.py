import xml.etree.ElementTree as ET
import cv2
import os
import numpy as np


colors={'cyan':(0,255,255),'blue':(0,0,255),'white':(255,255,255),
        'red':(255,0,0),'yellow':(255,255,0),'green':(0,255,0),'black':(0,0,0)}

def bgr2rgb(t):
    t=list(t)
    t[0],t[2]=t[2],t[0]
    return tuple(t)
    
def cv2_imread(filePath):
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    return cv_img

def get_box(path):
    

    xml_dirs=os.listdir(path)
    
    box=[]
    n=0
    for xml_file in xml_dirs: 
        
        tree=ET.parse(path+'\\'+xml_file)  
        
        root=tree.getroot()

        fileName=root.find('filename')
        objects=root.findall('object')
        for obj in objects:    
            name=obj.find('name')
            
            bndbox=obj.findall('bndbox')
            for bbox in bndbox:
            
                xmin=bbox.find('xmin')
                ymin=bbox.find('ymin')
                xmax=bbox.find('xmax')
                ymax=bbox.find('ymax')
                
                xmin=int(eval(xmin.text))
                ymin=int(eval(ymin.text))
                xmax=int(eval(xmax.text))
                ymax=int(eval(ymax.text))
                
                abox=[ n, fileName.text , name.text , xmin,ymin,xmax,ymax]
                box.append(abox)
                n+=1
                
                yield abox
    
def label_pic(nparry,bbox,c='cyan'):

    pic=nparry

    left_top=(bbox[-4],bbox[-3])
    right_bottom=(bbox[-2],bbox[-1])
    cv2.rectangle(pic, left_top, right_bottom,bgr2rgb(colors[c]), 2)
    
    return pic   
    
def main(Anno_path,JPEG_path,rate=1):

    pic_path=[JPEG_path+'\\'+i for i in os.listdir(JPEG_path)]
    boxiter=iter(get_box(Anno_path))

    new_pic_flag=1
    num=0
    _=1
    pic=cv2_imread(pic_path[num])
    for box in boxiter:
        if rate and rate!=1:
            box[-4:]=map(lambda x:int(x*rate),box[-4:])
            
        pic_id=box[1]
        if _:
            fr_picid=box[1]
            _=0
        
        if pic_id!=fr_picid:
            new_pic_flag=1
            cv2.imshow(pic_path[num][pic_path[num].rfind('\\')+1:],pic)
            cv2.waitKey(0)
            cv2.destroyAllWindows()  
        
        if new_pic_flag:
            pic=cv2_imread(pic_path[num])
            num+=1
            new_pic_flag=0
    
            if rate and rate!=1 :
                pic=cv2.resize(pic,(int(rate*pic.shape[0]),int(rate*pic.shape[1])),interpolation=cv2.INTER_LINEAR)
    
        print(box)
        cv2.putText(pic,box[2],(box[-4],box[-3]-4),cv2.FONT_HERSHEY_TRIPLEX,0.6,bgr2rgb(colors['red']),1)   
        pic=label_pic(pic,box)
        fr_picid=pic_id
        
        
if __name__ == '__main__':
     
#example:
    Anno_path='ann'  
    JPEG_path='img'
    main(Anno_path,JPEG_path,rate=0.5) 
    #    ann_dir | img_dir| scale_rate