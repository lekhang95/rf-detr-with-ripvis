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

### Validation Set (best EMA checkpoint)

| Metric        | Bbox   | Mask   |
|---------------|--------|--------|
| mAP@50        | 89.37% | 88.27% |
| mAP@50:95     | 45.41% | 35.62% |
| Precision     | 83.99% | 82.55% |
| Recall        | 82.20% | 80.80% |
| F1-Score      | 83.09% | 81.67% |

### Test Set (final evaluation)

| Metric        | Bbox   | Mask   |
|---------------|--------|--------|
| mAP@50        | 88.52% | —      |
| mAP@50:95     | 44.92% | —      |
| Precision     | 84.59% | —      |
| Recall        | 81.07% | —      |
| F1-Score      | 82.79% | —      |

---

## Requirements

```bash
pip install huggingface_hub rfdetr torch torchvision
```

- Python 3.10+
- PyTorch 2.x with CUDA
- GPU ≥ 16 GB VRAM recommended
