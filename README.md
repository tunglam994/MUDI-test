# 🧬 MUDI: A Multimodal Biomedical Dataset for Understanding Pharmacodynamic Drug–Drug Interactions

This repository provides the full dataset, molecular representations, textual metadata, and preprocessing scripts used in the MUDI project. The dataset is designed for developing and benchmarking multimodal models that predict clinically meaningful drug–drug interactions (DDIs) from a pharmacodynamic perspective.

---

## 📁 Directory Structure

```bash
.
├── dataset/
│   ├── train.csv
│   └── test.csv
│
├── molecules/
│   ├── images/
│   │   └── [drug_id].png
│   └── graphs/
│       └── [drug_id].graphml
│
├── preprocess/
│   ├── formula_handler.py
│   ├── graph_handler.py
│   ├── image_handler.py
│   └── text_handler.py
│
└── drug_info.json
```

---

## 📄 Dataset Overview

### `dataset/train.csv` and `dataset/test.csv`

These two CSV files contain the labeled DDI pairs used for training and evaluation.
Each file has the following columns:

* `Drug1`: Unique identifier for the first drug
* `Interaction`: One of the pharmacodynamic classes:

  * `Synergism`: Drug1 enhances the effect of Drug2
  * `Antagonism`: Drug1 reduces or neutralizes the effect of Drug2
  * `New Effect (New Adverse)`: The combination causes a novel effect not present when the drugs are used separately
* `Drug2`: Unique identifier for the second drug

All drug IDs correspond to keys in `drug_info.json`.

---

## 🧪 Molecular Representations

### `molecules/images/`

Contains 2D structure diagrams of each drug, rendered from its SMILES representation.

* File format: `.png`
* Naming convention: `[drug_id].png`
* Resolution: **1000×800** pixels
* Can be used with any standard image model (e.g., Vision Transformer)

### `molecules/graphs/`

Contains molecular graphs derived from SMILES, encoded in GraphML format.

* File format: `.graphml`
* Naming convention: `[drug_id].graphml`
* Standard: Follows the **GraphML** specification
* Recommended library: [NetworkX](https://networkx.org/)
* Structure:

  * **Nodes**: Atoms
  * **Edges**: Bonds between atoms (single, double, aromatic, etc.)

---

## 📚 Textual and Structural Metadata

### `drug_info.json`

Contains comprehensive textual and structural information for every drug used in the dataset.
Each entry has the following schema:

```json
{
  "drug_id": {
    "name": "DrugName",
    "description": {
      "summary": "...",
      "indication": "...",
      "metabolism": "...",
      "moa": "...",
      "pharmacodynamics": "..."
    },
    "formula": "C20H25N3O",
    "smiles": "CC(C)NCC(O)..."
  }
}
```

These fields are used to build input features for textual and formula-based encoders.

---

## ⚙️ Preprocessing Code

The `/preprocess` directory contains modular scripts for extracting features and building modality-specific inputs. Each script is self-contained and includes helper functions for reading raw drug metadata and converting it to a usable form.

* `text_handler.py`: Loads and concatenates textual fields (summary, indication, etc.) for BioMedBERT-based models.
* `formula_handler.py`: Translates chemical formulas into tokenized strings for language model inputs.
* `image_handler.py`: Uses RDKit to generate 2D structure diagrams from SMILES strings.
* `graph_handler.py`: Constructs molecular graphs from SMILES and exports them as GraphML files.

Dependencies include `RDKit`, `Pandas`, `NetworkX`, and `transformers`.

---

## 📜 License and Citation

* License: **Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0)**
* If you use this dataset in your research, please cite:

```bibtex
to be announced
```

---

## 🤝 Contact

For questions, feedback, or collaboration inquiries, please contact:
📧 \[[lhquynh@vnu.edu.vn](mailto:lhquynh@vnu.edu.vn)]
