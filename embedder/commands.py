import os

import click
from rich import print
from rich.pretty import Pretty
import lancedb
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector

from embedder.config import appConfig
from embedder.database import EmbedderDb

import logging
logger = logging.getLogger(__name__)



@click.command()
@click.option(
    "--db",
    default=appConfig.get("DATABASE_PATH"),
    help="File path of the sqlite database to use.",
)
@click.option(
    "--schema",
    default=appConfig.get("SCHEMA_FILE"),
    help="The schema file used to create the database.",
)
def init_db(db, schema):
    """
    Will generate the sqlite database using the schema file.
    """
    EmbedderDb.init_db(db, schema)
    logger.info("Database initialized successfully.")


@click.group()
def cli():
    pass


cli.add_command(init_db)
