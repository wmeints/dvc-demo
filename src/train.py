import pandas as pd
import click
import json
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import joblib


@click.command()
@click.argument("input_path", type=str)
@click.argument("output_path", type=str)
def main(input_path, output_path):
    feature_names = [
        'TYPE_WACHTTIJD',
        'SPECIALISME',
        'ROAZ_REGIO',
        'TYPE_ZORGINSTELLING'
    ]

    encoders = [(feature_name, OneHotEncoder())
                for feature_name in feature_names]

    model_pipeline = Pipeline([
        ("combine_features", FeatureUnion(encoders)),
        ("estimator", DecisionTreeRegressor())
    ])

    df = pd.read_csv(input_path)
    df_train, df_test = train_test_split(df, test_size=0.2)

    df_train_features = df_train[feature_names]
    df_test_features = df_test[feature_names]

    df_train_output = df_train['WACHTTIJD']
    df_test_output = df_test['WACHTTIJD']

    model_pipeline.fit(
        df_train_features.to_numpy(),
        df_train_output.to_numpy()
    )

    score = model_pipeline.score(
        df_test_features.to_numpy(), df_test_output.to_numpy())

    with open('metrics.json', 'w') as metrics_file:
        metrics_file.write(json.dumps({
            'r2': score
        }))

    joblib.dump(model_pipeline, output_path)

if __name__ == "__main__":
    main()
