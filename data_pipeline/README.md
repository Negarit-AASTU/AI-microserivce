# Negarit AI Microservice

This part of the project focuses on preparing the dataset used by the AI system.

## What was done

* Combined multiple datasets:

  * Resume Classification Dataset (raw text)
    https://www.kaggle.com/datasets/hassnainzaidi/resume-classification-dataset-for-nlp

  * Structured Resume Dataset
    https://www.kaggle.com/datasets/rayyankauchali0/resume-dataset

  * Job Description Dataset
    https://www.kaggle.com/datasets/dilshaansandhu/international-jobs-dataset

  Note:
    Due to size limitations, the full datasets are not included in this repository. 
* Reconstructed missing fields (name, experience, education, etc.)
* Localized the data to fit the Ethiopian context (names, companies, universities, locations)
* Added realistic contact information (email, phone, LinkedIn, Telegram)
* Enriched records with skills and multi-domain roles
* Normalized everything into a consistent format
* Cleaned the dataset (removed duplicates and invalid records)

## How to run

```bash
python main.py
```

## Output

The pipeline generates:

* `negarit_dataset.json` → final cleaned dataset

The full dataset is not included due to size.
A sample dataset `sample_negarit_dataset.json`is provided for testing and development.

## Notes

* The dataset is designed for further use in:

  * resume parsing
  * job matching
  * recommendation systems
