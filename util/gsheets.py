""" Work with Google Sheets

  * Read data from publicly available Google sheet
  * The gsheets API requires setting up a GCP account with billing, which is too complex.
    For example gspread package depends on having the account.

"""
import logging
from urllib.parse import quote

import pandas as pd


def download_gsheets(sheet_id, sheet_name):
    """Download data from one Google Sheets

    :param sheet_id: sheet ID, is in the URL of the sheet, for example:
      https://docs.google.com/spreadsheets/d/<sheet ID is here>
    :param sheet_name: name of the sheet that has data, which is shown at the bottom tabs.
    :return: Pandas DF
    """
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    # tenhle odkaz uz nam nefunguje, zacal nam generovat rozbite CSV
    # url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={quote(sheet_name)}"
    logging.info(f"downloading from {url}")
    return pd.read_csv(url, keep_default_na=False).to_dict("records")

