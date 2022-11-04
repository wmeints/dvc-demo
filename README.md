# Sample ML project using DVC

This repo contains a demo project that shows how to use DVC to build machine-learning projects.
Please follow the instructions below to get started.

## System requirements 

- Latest version of DVC
- Python 3.10

## Getting started

### Checking in the source data for the project  

This project relies on an open dataset from the dutch government. You can download it [here][DATASET].
Save the downloaded file to `data/raw/wachttijden.csv` and run the following command to store the data in DVC:

```shell
dvc add data/raw
git commit -am "Add source data"
```

### Running the experiment

You can run the experiment using the following command:

```shell
dvc repro
```

This command will run the following scripts in order:

- `src/prepare.py`
- `src/train.py`

After the pipeline is completed, you can find the model in `.mlem/model`. You can use this model in an inference program.

### Using the Github actions workflow

This project includes a Github actions workflow that you can use for CI/CD purposes. You can find it in 
`.github/workflows/train_model.yml`. The workflow perfoms the following steps:

- Lint the source code
- Run unit-tests against the source code
- Train the model
