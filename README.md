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

### RF-DETR — Test Set

| Metric        | Bbox   | Mask   |
|---------------|--------|--------|
| mAP@50        | 88.52% | —      |
| mAP@50:95     | 44.92% | —      |
| Precision     | 84.59% | —      |
| Recall        | 81.07% | —      |
| F1-Score      | 82.79% | —      |

> EMA model (best checkpoint): mAP@50 = **89.37%** (bbox), **88.27%** (mask)

### YOLOv26 — Validation Set (epoch 10)

| Metric            | Box    | Mask   |
|-------------------|--------|--------|
| mAP@50            | 64.49% | 66.58% |
| mAP@50-95         | 31.04% | 29.47% |
| Precision         | 75.60% | 76.88% |
| Recall            | 54.81% | 56.04% |

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
