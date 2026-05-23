# RF-DETR — Rip Current Instance Segmentation

Fine-tuning **RF-DETR** (Roboflow Detection Transformer) with a segmentation head on the [RipVIS dataset](https://huggingface.co/datasets/Irikos/RipVIS) for rip current detection.

---

## Directory Structure

```
rf-detr/
├── src/
│   ├── data_and_training_rfdetr.ipynb   # Main notebook: data prep + training
│   └── rf-detr-seg-medium.pt            # Pretrained RF-DETR-Seg-Medium weights
├── data_rfdetr_final/                   # Processed dataset (COCO format)
│   ├── train/
│   │   ├── _annotations.coco.json
│   │   └── *.jpg  (18,389 images)
│   ├── valid/
│   │   ├── _annotations.coco.json
│   │   └── *.jpg  (2,184 images)
│   └── test/
│       ├── _annotations.coco.json
│       └── *.jpg  (2,165 images)
├── output/                              # Training output (5 epochs)
│   ├── log.txt
│   ├── results.json
│   ├── results_mask.json
│   └── metrics_plot.png
└── output_continue_ema/                 # Continued training with EMA
    ├── log.txt
    ├── results.json
    └── ...
```

---

## Model

| Setting            | Value                          |
|--------------------|--------------------------------|
| Base model         | `rf-detr-seg-medium`           |
| Parameters         | 35.4M                          |
| Backbone           | DINOv2 Windowed Small (12 layers) |
| Input resolution   | 432 px (multi-scale up to 552) |
| Decoder layers     | 5                              |
| Queries            | 200                            |
| Batch size         | 8 (grad accum ×4 → effective 32) |
| Learning rate      | 1e-4 (encoder: 1.5e-4)        |
| Epochs             | 5                              |
| EMA decay          | 0.993                          |
| GPU                | NVIDIA RTX A5000 (25.7 GB)     |

---

## Data Preparation

The notebook `data_and_training_rfdetr.ipynb` performs these steps:

1. **Download** RipVIS from Hugging Face (`Irikos/RipVIS`)
2. **Extract** `sampled_images.zip` for train and val splits
3. **Merge** additional training data into the main images folder
4. **Restructure** into RF-DETR's expected COCO layout:
   - `train/_annotations.coco.json` + images
   - `valid/_annotations.coco.json` + images
5. **Carve out test set** from validation using balanced video-level selection:
   - ~50% of RIP frames (19 videos, 1,430 frames)
   - ~50% of NR frames (2 videos, 735 frames)
   - Final test: **2,165 frames** | Remaining valid: **2,184 frames**

---

## Training

```python
from rfdetr import RFDETRMedium

model = RFDETRMedium(pretrain_weights="rf-detr-seg-medium.pt")
model.train(
    dataset_dir="data_rfdetr_final",
    epochs=5,
    batch_size=8,
    lr=1e-4,
    output_dir="output",
    use_ema=True,
)
```

Or run the full notebook:

```bash
jupyter notebook src/data_and_training_rfdetr.ipynb
```

---

## Results

### Best Segmentation Results (Validation Set)

| Setting              | Best Epoch | mAP@50 (Mask) | mAP@50–95 (Mask) | F1-Score |
|----------------------|-----------|---------------|------------------|----------|
| Regular              | 5         | 86.15%        | 36.88%           | 80.94%   |
| EMA                  | 8         | 89.74%        | 36.46%           | 85.06%   |
| EMA (highest mAP@50) | 10        | **90.19%**    | **34.79%**       | **86.13%** |

### Detailed Training Results (10 Epochs)

| Epoch | Train Loss | mAP@50 | mAP@50–95 | EMA mAP@50–95 |
|-------|-----------|--------|-----------|---------------|
| 1     | 46.80     | 78.25% | 29.78%    | 35.62%        |
| 2     | 41.43     | 82.86% | 29.17%    | 34.01%        |
| 3     | 38.83     | 86.83% | 34.16%    | 35.11%        |
| 4     | 38.36     | 85.30% | 33.85%    | 36.22%        |
| 5     | 36.22     | 86.15% | 36.88%    | 36.36%        |
| 6     | 37.21     | 84.19% | 32.15%    | 35.61%        |
| 7     | 37.28     | 85.21% | 33.59%    | 35.10%        |
| 8     | 36.93     | 85.07% | 33.00%    | **36.46%**    |
| 9     | 35.96     | 83.61% | 33.23%    | 35.19%        |
| 10    | 35.13     | 85.23% | 32.86%    | 34.79%        |

---

## Requirements

```bash
pip install huggingface_hub rfdetr torch torchvision
```

- Python 3.10+
- PyTorch 2.x with CUDA
- GPU ≥ 16 GB VRAM recommended
