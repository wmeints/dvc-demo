import pandas as pd
import click
import json
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
import joblib


FEATURE_NAMES = [
    'TYPE_WACHTTIJD',
    'SPECIALISME',
    'ROAZ_REGIO',
    'TYPE_ZORGINSTELLING'
]


def get_model():
    encoders = [(feature_name, OneHotEncoder(sparse=False))
                for feature_name in FEATURE_NAMES]

    model_pipeline = Pipeline([
        ("combine_features", FeatureUnion(encoders)),
        ("estimator", GradientBoostingRegressor())
    ])

    return model_pipeline


def get_data(input_path):
    df = pd.read_csv(input_path)
    df_train, df_test = train_test_split(df, test_size=0.2)

    df_train_features = df_train[FEATURE_NAMES]
    df_test_features = df_test[FEATURE_NAMES]

    df_train_output = df_train['WACHTTIJD']
    df_test_output = df_test['WACHTTIJD']

    return df_train_features, df_test_features, df_train_output, df_test_output


@click.command()
@click.argument("input_path", type=str, default='data/intermediate/wachttijden.csv')
@click.argument("output_path", type=str, default='models/classifier.bin')
def main(input_path, output_path):
    model_pipeline = get_model()
    
    train_features, test_features, train_output, test_output = \
        get_data(input_path)

    model_pipeline.fit(
        train_features,
        train_output
    )

    score = model_pipeline.score(
        test_features.to_numpy(), test_output.to_numpy())

    with open('metrics.json', 'w') as metrics_file:
        metrics_file.write(json.dumps({
            'r2': score
        }))

    joblib.dump(model_pipeline, output_path)


if __name__ == "__main__":
    main()
