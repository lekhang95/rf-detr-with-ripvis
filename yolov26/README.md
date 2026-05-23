# YOLOv26 — Rip Current Instance Segmentation

Fine-tuning **YOLOv26s-seg** on the [RipVIS dataset](https://huggingface.co/datasets/Irikos/RipVIS) for rip current detection and segmentation using the Ultralytics framework.

---

## Directory Structure

```
yolov26/
├── src_yolov26_ripvis/
│   ├── data_processing.ipynb   # Download, convert, and prepare dataset
│   ├── train.ipynb             # Training notebook
│   └── README.md               # Quick-start notes
├── train7/                     # Best training run (10 epochs, continued)
│   ├── args.yaml               # Full training config
│   ├── results.csv             # Per-epoch metrics
│   ├── BoxF1_curve.png
│   ├── BoxPR_curve.png
│   ├── MaskF1_curve.png
│   ├── MaskPR_curve.png
│   ├── confusion_matrix.png
│   ├── confusion_matrix_normalized.png
│   ├── labels.jpg
│   ├── results.png
│   ├── train_batch*.jpg
│   └── val_batch*_pred.jpg
├── data.py                     # (utility script)
└── data_processing.ipynb       # Alternate data prep notebook
```

---

## Model

| Setting          | Value                  |
|------------------|------------------------|
| Base model       | `yolo26s-seg.pt`       |
| Framework        | Ultralytics 8.4.19     |
| Input resolution | 640×640                |
| Batch size       | 18 (train7)            |
| Epochs           | 10 (continued run)     |
| Optimizer        | Auto (cosine LR)       |
| lr0              | 0.01                   |
| Patience         | 10                     |
| GPU              | NVIDIA RTX A5000       |

---

## Data Preparation

Run `src_yolov26_ripvis/data_processing.ipynb` to:

1. **Download** RipVIS from Hugging Face (YOLO format annotations):
   - `train/sampled_images.zip`
   - `train/yolo_annotations.zip`
   - `val/sampled_images.zip`
   - `val/yolo_annotations.zip`

2. **Extract and flatten** images and labels into:
   ```
   ripVIS_yolo/
   ├── images/train/   (18,389 images)
   ├── images/val/     (4,349 images)
   ├── labels/train/   (12,089 positive + 6,300 negative)
   └── labels/val/     (2,861 positive + 1,488 negative)
   ```

3. **Validate** all label files (format, coordinate range, numeric check)

4. **Create negative labels** — empty `.txt` files for frames with no rip current (NR videos), so the model learns to suppress false positives

5. **Generate `ripvis.yaml`** dataset config

Dataset stats after processing:

| Split | Images | Positive labels | Negative labels |
|-------|--------|-----------------|-----------------|
| Train | 18,389 | 12,089          | 6,300           |
| Val   | 4,349  | 2,861           | 1,488           |

---

## Training

```bash
# Option 1: CLI
yolo segment train \
  model=yolo26s-seg.pt \
  data=<path_to>/ripvis.yaml \
  imgsz=640 epochs=25 batch=32 \
  device=0 patience=8 lr0=0.005 cos_lr=True

# Option 2: Notebook
jupyter notebook src_yolov26_ripvis/train.ipynb
```

> **Note:** Update all absolute paths in `data_processing.ipynb` and the training command to match your local environment.

---

## Results (train7 — epoch 10)

| Metric            | Box    | Mask   |
|-------------------|--------|--------|
| mAP@50            | 64.49% | 66.58% |
| mAP@50-95         | 31.04% | 29.47% |
| Precision         | 75.60% | 76.88% |
| Recall            | 54.81% | 56.04% |

Training curves and confusion matrices are saved in `train7/`.

---

## Requirements

```bash
pip install -U ultralytics huggingface_hub
```

- Python 3.10+
- PyTorch 2.x with CUDA (`torch==2.10.0+cu128` tested)
- GPU ≥ 8 GB VRAM (16 GB+ recommended for batch=32)
