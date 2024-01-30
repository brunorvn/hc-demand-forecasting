# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
import os
from dotenv import find_dotenv, load_dotenv

import pandas as pd


def clean_and_convert_to_time_series(
    df: pd.DataFrame, id_variable: str = "Procedimentos realizados"
) -> pd.DataFrame:
    df = df.drop(columns=["Total"])

    df = df[df[f"{id_variable}"] != "Total"]

    long_df = pd.melt(df, id_vars=[f"{id_variable}"], var_name="ds", value_name="y")

    def parse_custom_date(date_str):
        month_mapping = {
            "Janeiro": "January",
            "Fevereiro": "February",
            "Março": "March",
            "Abril": "April",
            "Maio": "May",
            "Junho": "June",
            "Julho": "July",
            "Agosto": "August",
            "Setembro": "September",
            "Outubro": "October",
            "Novembro": "November",
            "Dezembro": "December",
        }
        month_str, year_str = date_str.split("/")
        month_str = month_mapping.get(month_str, month_str)
        return pd.to_datetime(f"{month_str}/{year_str}", format="mixed")

    long_df["ds"] = long_df["ds"].apply(parse_custom_date)

    long_df.rename(columns={"Procedimentos realizados": "unique_id"}, inplace=True)
    long_df.sort_values(by=["unique_id", "ds"], inplace=True)
    return long_df


@click.command()
@click.argument("input_filepath", type=click.Path(exists=True))
def main(input_filepath: str):
    """Runs data processing scripts to turn raw data from (../raw) into
    cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info("making final data set from raw data")

    raw_df = pd.read_csv(input_filepath, delimiter=",", encoding="latin-1")
    df = clean_and_convert_to_time_series(raw_df)
    df.to_csv(f"results_{input_filepath}.csv", index=False)


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
