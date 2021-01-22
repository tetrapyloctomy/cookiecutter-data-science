# -*- coding: utf-8 -*-
import typer
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from rich.logging import RichHandler

app = typer.Typer()

logging.basicConfig(
    level="NOTSET",
    format="%(name)s - %(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)


@app.command()
def make_dataset(
    input_filepath: Path,
    output_filepath: Path,
):
    """Runs data processing scripts to turn raw data from (../raw) into
    cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info("making final data set from raw data")


if __name__ == "__main__":
    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    app()
