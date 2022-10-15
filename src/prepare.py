from pathlib import Path
import pandas as pd
import click


def select_features(df):
    columns = [
        'WACHTTIJD',
        'TYPE_WACHTTIJD',
        'SPECIALISME',
        'ROAZ_REGIO',
        'TYPE_ZORGINSTELLING'
    ]

    return df[columns]


def fix_missing_values(df):
    df = df.dropna(subset=['WACHTTIJD'])
    df['TYPE_ZORGINSTELLING'] = df['TYPE_ZORGINSTELLING'].fillna('Kliniek')

    return df


@click.command()
@click.argument('input_path', type=str)
@click.argument('output_path', type=str)
def main(input_path, output_path):
    df = pd.read_csv(input_path, sep=';')

    df = select_features(df)
    df = fix_missing_values(df)

    Path(output_path).parent.mkdir(exist_ok=True)
    df.to_csv(output_path, index=None)


if __name__ == "__main__":
    main()
