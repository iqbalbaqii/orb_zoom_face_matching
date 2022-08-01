from src.bll import Face
import os
import cv2

parrent_dir = '/home/bucky/Documents/Py/final/orb_zoom_face_matching/assets/datasource'

user = 'Zaneva_Rahmanda_Ikhsan'
os.mkdir(parrent_dir+'/'+user+'/result')
for i,filename in enumerate(os.listdir(parrent_dir+'/'+user+'/raw')):
    img = cv2.imread(parrent_dir+'/'+user+'/raw/'+filename)
    
    segmented = Face.segment_face(img)
    cv2.imwrite(parrent_dir+'/'+user+'/result/label_'+str(i)+'.png', segmented)

