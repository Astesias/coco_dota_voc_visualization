import cv2
import os
import numpy as np
from math import atan,pi

def bgr2rgb(t):
     t=list(t)
     t[0],t[2]=t[2],t[0]
     return tuple(t)
     
def path2filename(path):
    if type(path)!=type('str'):
        raise TypeError('path is a str,not {}'.format(type(path)))
    if path.rfind('\\')>path.rfind('/'):
        return path[path.rfind('\\')+1:]
    else:
        return path[path.rfind('/')+1:]
    
def cv2_imread(filePath): 
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    return cv_img

def inteval(st):
    try:
        return eval(st)
    except :
        return st

def rotate_bound(image, angle):
          (h, w) = image.shape[:2]
          (cX, cY) = (w // 2, h // 2)
          M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
          cos = np.abs(M[0, 0])
          sin = np.abs(M[0, 1])
          nW = int((h * sin) + (w * cos))
          nH = int((h * cos) + (w * sin))
          M[0, 2] += (nW / 2) - cX
          M[1, 2] += (nH / 2) - cY
          return cv2.warpAffine(image, M, (nW, nH)) 

def get_box(txt_paths):  
    box=[[] for i in range(len(txt_paths))]
    for N,txt_path in enumerate(txt_paths[:]):
        
        with open(txt_path) as fp:
            txt=fp.read()
            txt_list=txt.split('\n')

            for n,line in enumerate(txt_list[:]):
                if line and ':' not in line:
                    line=line.split(' ')
                    # pdb.set_trace()
                    obj=list(map(inteval,line[:8])) + [line[8]]
                    box[N].append( obj )


    return box      
                    
def drawRect(img, pt1, pt2, pt3, pt4, color, lineWidth):
    cv2.line(img, pt1, pt2, color, lineWidth)
    cv2.line(img, pt2, pt3, color, lineWidth)
    cv2.line(img, pt3, pt4, color, lineWidth)
    cv2.line(img, pt1, pt4, color, lineWidth)



def dota_viewer(anno_path,jpeg_path,ro=0,rate=1,st=0,Nonepass=1):
    
    txt_names=os.listdir(anno_path)
    txt_paths=[anno_path+_ for _ in txt_names]
    jpg_paths=[jpeg_path+_.strip('txt')+'jpg' for _ in txt_names]
    boxes=get_box(txt_paths)
    for i in range(st,len(txt_paths)):
        path=jpg_paths[i]
        img=cv2_imread(path)
        if rate!=1 and rate:
            img=cv2.resize(img,(int(img.shape[0]*rate),int(img.shape[1]*rate)) )
            boxs=boxes[i]
            
            if Nonepass and len(boxs)!=0:
                Nonepas=1
            else:
                Nonepas=0 
                    
            for m,box in enumerate(boxs[:]):
                if not ro:
                    a,b,c,d,e,f,g,h=box[0],box[1],box[2],box[3],box[4],box[5],box[6],box[7]

                    if rate!=1 and rate:
                        a,b,c,d,e,f,g,h=tuple(map(lambda x:int(x*rate),(a,b,c,d,e,f,g,h)))
                    po1=(a,b)
                    po2=(c,d)
                    po3=(e,f)
                    po4=(g,h)
                    
                    
                    drawRect(img, po1,po2,po3,po4,(0,255,0),2)
                    cv2.putText(img,box[8],(po1[0]-5,po1[1]-5),cv2.FONT_HERSHEY_TRIPLEX,0.8,bgr2rgb((255,0,0))    ,2)
                    print('{} {} {} {} {} {}'.format(path,po1,po2,po3,po4,box[8]))
                    
                else:
                    a,b,c,d,e,f,g,h=box[0],box[1],box[2],box[3],box[4],box[5],box[6],box[7]
                    if rate!=1 and rate:
                        a,b,c,d,e,f,g,h=tuple(map(lambda x:int(x*rate),(a,b,c,d,e,f,g,h)))
                    po1=(a,b)
                    po2=(c,d)
                    po3=(e,f)
                    po4=(g,h)
                        
                    try:
                        angle=180-180*atan((f-d)/(e-c))/pi
                    except:
                        angle=0
                 
                    if angle>180:
                        angle-=180
                    if angle>90:
                        angle=-(180-angle)
                    
                    img=cv2_imread(path)
                    img=cv2.resize(img,(int(img.shape[0]*rate),int(img.shape[1]*rate)) )
                    drawRect(img, po1,po2,po3,po4,(0,255,0),2)
                    cv2.putText(img,box[8],(po1[0]-5,po1[1]-5),cv2.FONT_HERSHEY_TRIPLEX,0.8,bgr2rgb((255,0,0)))  
                    img=rotate_bound(img,angle)
                     
                    print('{} {} {} {} {} {}'.format(path,po1,po2,po3,po4,box[8]))
                
                     
                    cv2.imshow(path2filename(path),img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                
        if not ro:
            if Nonepass and Nonepas:
                cv2.imshow(path2filename(path),img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                print()
            elif not Nonepass:
                cv2.imshow(path2filename(path),img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                print()


if __name__ == '__main__':
    
    example=1
    
    anno_path='ann/'
    jpeg_path='img/'
    
#exsample 1:
    if 1:
        index=0
        dota_viewer(anno_path,jpeg_path,rate=0.6,ro=False,st=index,Nonepass=True)
#exsample 2:
    else:
        index=4
        dota_viewer(anno_path,jpeg_path,rate=0.6,ro=True,st=index,Nonepass=True)   
        #if  ro=True 1 img only contain 1 target 
    
        #          ann_dir|img_path|scale_rate|rotate|start_index|pass empty 

    # dota:    xxxxx: xxxxx
    #          gsd: xxxxx
    #          x1 y1 x2 y2 x3 y3 x4 y4 class diff
    
    