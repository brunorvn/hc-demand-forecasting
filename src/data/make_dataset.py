# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
import os
from dotenv import find_dotenv, load_dotenv

import pandas as pd


@click.command()
@click.argument("input_filepath", type=click.Path(exists=True))
@click.argument("output_filepath", type=click.Path())
def main(input_filepath, output_filepath):
    """Runs data processing scripts to turn raw data from (../raw) into
    cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info("making final data set from raw data")


def clean_raw_data(df, vars_str):
    df = df.drop(columns=["Total"])

    df = df[df[f"{vars_str}"] != "Total"]
    return df


def clean_and_convert_to_time_series(df, vars_str):
    cleaned_df = clean_raw_data(df, vars_str)

    id_vars = [f"{vars_str}"]

    ts_df = pd.melt(cleaned_df, id_vars=id_vars, var_name="ds", value_name="y")

    def parse_custom_date(date_str):
        month_mapping = {
            "Jan": "January",
            "Fev": "February",
            "Mar": "March",
            "Abr": "April",
            "Mai": "May",
            "Jun": "June",
            "Jul": "July",
            "Ago": "August",
            "Set": "September",
            "Out": "October",
            "Nov": "November",
            "Dez": "December",
        }

        if date_str != "Total":
            month_str, year_str = date_str.split("/")
            month_str = month_mapping.get(month_str, month_str)
            return pd.to_datetime(f"{month_str}/{year_str}", format="%B/%Y")

        return date_str

    ts_df["ds"] = ts_df["ds"].apply(parse_custom_date)

    ts_df.rename(columns={vars_str: "unique_id"})

    return ts_df


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
