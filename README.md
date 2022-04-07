# TablesExtractorWebDemo
Web demo of tables extraction functionality

# Installation
1. Prepare tensorflow models:
```bash
cd tables_extractor/tables_extractor/models
bash download_model.sh matroshenko TablesDetector v3.0.0 tables_detector_v3
bash download_model.sh matroshenko TableAnalyzer v2.0.0 splerge_model_v1
unzip tables_detector_v3.zip -d tables_detector_v3
unzip splerge_model_v1.zip -d splerge_model_v1
```
2. Install packages `pip install -r requirements.txt`.

# Usage
1. Run server `python demo.py runserver`.
2. Open link in browser `127.0.0.1:5000`.