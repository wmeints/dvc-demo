# Training models with DVC and Github actions

In [my previous post][PREV_POST] I showed how to use DVC to manage data for your
machine-learning project. Today it's time to take things to the next level.
Let's build a pipeline to train a machine-learning model with DVC and Github
actions.

## Quick reminder: What was DVC again?

DVC is a tool that helps version data used in a machine-learning project.
It removes the need to create separate folders for your models. Instead you
version the data using a storage account and your local GIT repository. You can
use a wide variety of remote storage accounts to keep your data safe.

## About the sample in this article

In this article I'm using a toy project that I've used over the past few months
to test various MLOps tools. It's a model that predicts waiting times for dutch
healthcare based on a [public dataset][DATASET].

The model uses the following features to predict the waiting time:

- TYPE_WACHTTIJD: The type of visit ('Behandeling', 'Diagnostiek', 'Polikliniekbezoek')
- SPECIALISME: The specialization we're predicting the waiting time for
- ROAZ_REGIO: The region in the Netherlands ('Brabant', 'Euregio', 'Limburg', 'Midden-NL', 'Noord-NL', 'Noordwest', 'Oost', 'SpzNet AMC', 'West', 'Zuidwest-NL', 'Zwolle')
- TYPE_ZORGINSTELLING: The type of healthcare provider we're predicting for (Kliniek, Ziekenhuis)

You can find the code for the sample on [Github][DEMO_CODE].

We use two scripts to train the model:

* `src/prepare.py` - Extracts the features from the raw dataset and cleans the data.
* `src/train.py` - Trains the model based on the extracted features and stores the trained model on disk.

It's not a very complicated project, but enough to get a feel for how DVC works.

## Building a pipeline to train a model

In the previous post we've used the basic commands available in DVC to manage
the data for a machine-learning project. That's nice, but most of us will have
a couple of steps that need to be performed before we have a working
machine-learning model.

This is where data pipelines come into play. DVC allows the use of stages to
combine several steps into a data pipeline. 

Each step is implemented as a shell command. For each step you can define
dependencies and outputs. When one step depends on the output of another step,
DVC will order the steps based on the dependencies of each step. When the
dependencies of a step haven't changed, the step is skipped.

Here's how to set up a pipeline.

### Building a data preparation step

First, we need to create a stage for the preparation step. You can create a new
step using the following command:

```
dvc stage add prepare -d data/raw/wachttijden.csv -d src/prepare.py -m metrics.json -o data/intermediate/wachttijden.csv python src/prepare.py data/raw/wachttijden.csv data/intermediate/wachttijden.csv
```

The `dvc stage add` command needs a set of dependencies specified with `-d`. 
We've provided the input dataset as a dependency, and the prepare script. When
one of these files changes, we want the stage to be invalidated.

The final argument for the stage command is the command-line we use to run the
preparation script including the requirement arguments for the script.

### Building a training step

## Running the experiment on your computer


[PREV_POST]: https://fizzylogic.nl/2022/10/14/managing-machine-learning-datasets-with-dvc
[DATASET]: https://puc.overheid.nl/PUC/Handlers/DownloadDocument.ashx?identifier=PUC_656543_22&versienummer=1
[DEMO_CODE]: https://github.com/wmeints/dvc-demo