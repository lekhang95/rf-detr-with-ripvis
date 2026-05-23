# YOLOv26 — Quick Start

## Step 1 — Data Preparation

Run `data_processing.ipynb`:

- Download dataset
- Convert to YOLO format
- Validate labels
- Create negative labels (empty files for no-rip frames)
- Generate `ripvis.yaml`

## Step 2 — Training

```bash
yolo segment train \
  model=yolo26s-seg.pt \
  data="<path_to>/ripvis.yaml" \
  imgsz=640 epochs=25 batch=32 \
  device=0 patience=8 lr0=0.005 cos_lr=True
```

> **Note:** Update all absolute paths in `data_processing.ipynb` and the training command to match your local environment.