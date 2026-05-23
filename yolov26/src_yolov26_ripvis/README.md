step 1:
 - run data_processing.ipynb file : 
	+ Dowload data
	+ Convert to Yolo format
	+ Check label
	+ Create negative label
	+ Creat yaml
step 2: run command to train yolo:  
yolo segment train model=yolo26s-seg.pt data="C:\khanglv1\ripvis\yolo26\ripVIS_yolo\ripvis.yaml" imgsz=640 epochs=25 batch=32 device=0 patience=8 lr0=0.005 cos_lr=True 

*NOTE: chú ý các đường dẫn trong file data_processing và command train