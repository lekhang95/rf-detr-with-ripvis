# Rip Current Detection with RF-DETR and YOLOv26

Instance segmentation of rip currents using two state-of-the-art models — **RF-DETR** (transformer-based) and **YOLOv26** (CNN-based) — trained and evaluated on the [RipVIS dataset](https://huggingface.co/datasets/Irikos/RipVIS).

---

## Repository Structure

```
df_detr_with_rip_vis/
├── rf-detr/                        # RF-DETR experiment
│   ├── src/
│   │   ├── data_and_training_rfdetr.ipynb   # Data prep + training notebook
│   │   └── rf-detr-seg-medium.pt            # Pretrained weights
│   ├── data_rfdetr_final/          # Processed dataset (COCO format)
│   │   ├── train/
│   │   ├── valid/
│   │   └── test/
│   └── output/                     # Training results
│       ├── log.txt
│       ├── results.json
│       └── metrics_plot.png
│
├── yolov26/                        # YOLOv26 experiment
│   ├── src_yolov26_ripvis/
│   │   ├── data_processing.ipynb   # Data prep notebook
│   │   ├── train.ipynb             # Training notebook
│   │   └── README.md
│   └── train7/                     # Training run results
│       ├── results.csv
│       ├── args.yaml
│       └── *.png                   # Curves & visualizations
│
└── README.md
```

---

## Dataset

**RipVIS** — a video dataset of rip current footage from beach surveillance cameras.

- Source: [Irikos/RipVIS on Hugging Face](https://huggingface.co/datasets/Irikos/RipVIS)
- Classes: `rip_currents` (1 class), with negative (no-rip) frames included
- Splits used:

| Split | Images |
|-------|--------|
| Train | 18,389 |
| Valid | 2,184  |
| Test  | 2,165  |

The test set was carved out from the original validation split using a balanced video-level selection (50% RIP / 50% NR frames by video).

---

## Models

### RF-DETR (Transformer)

- Base model: `rf-detr-seg-medium` (35.4M parameters)
- Backbone: DINOv2 Windowed Small
- Resolution: 432×432 (multi-scale with 552)
- Trained on: NVIDIA RTX A5000 (25.7 GB)
- Epochs: 5 (with EMA)

### YOLOv26 (CNN)

- Base model: `yolo26s-seg.pt`
- Framework: Ultralytics 8.4.19
- Resolution: 640×640
- Trained on: NVIDIA RTX A5000
- Epochs: 10 (cosine LR, patience=10)

---

## Results

### RF-DETR — Best Segmentation Results (Validation Set)

| Setting              | Best Epoch | mAP@50 (Mask) | mAP@50–95 (Mask) | F1-Score |
|----------------------|-----------|---------------|------------------|----------|
| Regular              | 5         | 86.15%        | 36.88%           | 80.94%   |
| EMA                  | 8         | 89.74%        | 36.46%           | 85.06%   |
| EMA (highest mAP@50) | 10        | **90.19%**    | **34.79%**       | **86.13%** |

### YOLOv26 — Best Segmentation Results by Variant (Validation Set)

| Model         | Best Epoch | mAP@50 (Mask) | mAP@50–95 (Mask) |
|---------------|-----------|---------------|------------------|
| YOLOv26n-seg  | 25        | 62.63%        | 27.44%           |
| YOLOv26s-seg  | 17        | 64.88%        | 27.24%           |
| YOLOv26m-seg  | 19        | **66.66%**    | **29.51%**       |
| YOLOv26l-seg  | 10        | 64.17%        | 26.88%           |

---

## Quickstart

### RF-DETR

```bash
# 1. Install dependencies
pip install huggingface_hub rfdetr

# 2. Open and run the notebook
jupyter notebook rf-detr/src/data_and_training_rfdetr.ipynb
```

The notebook covers:
1. Downloading RipVIS from Hugging Face
2. Restructuring into COCO format (`train/valid/test`)
3. Splitting test set from validation by video
4. Training RF-DETR with segmentation head

### YOLOv26

```bash
# 1. Install dependencies
pip install -U ultralytics huggingface_hub

# 2. Run data processing
jupyter notebook yolov26/src_yolov26_ripvis/data_processing.ipynb

# 3. Train
yolo segment train \
  model=yolo26s-seg.pt \
  data=<path_to>/ripvis.yaml \
  imgsz=640 epochs=25 batch=32 \
  device=0 patience=8 lr0=0.005 cos_lr=True
```

The data processing notebook covers:
1. Downloading RipVIS (YOLO format annotations)
2. Extracting and flattening images/labels
3. Creating empty label files for negative (no-rip) frames
4. Generating `ripvis.yaml` config

---

## How to Use the Model

### RF-DETR — Inference

```python
from rfdetr import RFDETRMedium
from rfdetr.util.coco_utils import get_coco_api_from_dataset
import supervision as sv
from PIL import Image

# Load model with trained weights
model = RFDETRMedium(pretrain_weights="rf-detr/src/rf-detr-seg-medium.pt")

# Run inference on a single image
image = Image.open("path/to/image.jpg")
detections = model.predict(image, threshold=0.5)

# Visualise with supervision
annotator = sv.MaskAnnotator()
annotated = annotator.annotate(
    scene=image.copy(),
    detections=detections
)
annotated.show()
```

To run inference on a folder of images:

```python
import os
from PIL import Image

image_dir = "rf-detr/data_rfdetr_final/test"
for fname in os.listdir(image_dir):
    if fname.endswith(".jpg"):
        image = Image.open(os.path.join(image_dir, fname))
        detections = model.predict(image, threshold=0.5)
        print(f"{fname}: {len(detections)} detection(s)")
```

> **Checkpoint location:** trained weights are saved under `rf-detr/output/eval/latest.pth` (standard) or `rf-detr/output_continue_ema/eval/latest.pth` (EMA run). Pass the `.pth` path to `pretrain_weights` to load a specific checkpoint.

---

### YOLOv26 — Inference

```python
from ultralytics import YOLO

# Load trained model
model = YOLO("yolov26/train7/weights/best.pt")

# Predict on a single image
results = model.predict(
    source="path/to/image.jpg",
    imgsz=640,
    conf=0.25,
    iou=0.45,
    save=True          # saves annotated image to runs/segment/predict/
)

# Inspect detections
for r in results:
    print(r.boxes)     # bounding boxes
    print(r.masks)     # segmentation masks
```

Batch inference on a directory:

```python
results = model.predict(
    source="path/to/images/",
    imgsz=640,
    conf=0.25,
    save=True,
    save_txt=True      # also saves labels in YOLO format
)
```

Video inference:

```python
results = model.predict(
    source="path/to/video.mp4",
    imgsz=640,
    conf=0.25,
    save=True          # saves annotated video
)
```

> **Checkpoint location:** `yolov26/train7/weights/best.pt` (best mAP) or `last.pt` (final epoch).

---

## Requirements

| Package         | Version tested |
|-----------------|----------------|
| Python          | 3.10           |
| PyTorch         | 2.10.0+cu128   |
| Ultralytics     | 8.4.19         |
| huggingface_hub | ≥ 0.36         |
| rfdetr          | latest         |

GPU with ≥ 16 GB VRAM recommended (tested on NVIDIA RTX A5000, 24 GB).

---

## Citation

If you use this work, please cite the RipVIS dataset:

```bibtex
@dataset{ripvis,
  author    = {Irikos},
  title     = {RipVIS},
  year      = {2024},
  publisher = {Hugging Face},
  url       = {https://huggingface.co/datasets/Irikos/RipVIS}
}
```
