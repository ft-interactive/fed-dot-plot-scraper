"""Utility functions."""
from __future__ import annotations

import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd
import requests


def parse_date(url) -> datetime:
    """Parse the date from a source URL."""
    s = re.split(r"fomcprojtabl", url)[1]
    s = s.replace(".htm", "")
    return pd.to_datetime(s[-8:])


def get_url(url) -> str:
    """Get the provided URL."""
    r = requests.get(url)
    assert r.ok
    return r.text


def safestr(ele) -> str | None:
    """Return a stripped string or None."""
    return ele.strip() or None


def format_wide_to_long(df: pd.DataFrame) -> pd.DataFrame:
    """Re-format data into a long format (to prep for use in some of our charts)

    Args:
        df (pd.DataFrame): The original wide-formatted dataframe.

    Returns:
        pd.DataFrame: A DataFrame in a long format, where date/rate/year combinations each occupy a row with a value of the number of participants who supported that value
    """

    # add a prefix to columns with years (and "longer run") to prep for wide_to_long
    timeframe_prefix = "num_participants"
    long_df = df.add_prefix(timeframe_prefix)
    long_df.columns = ["meeting_date", "midpoint"] + [x for x in long_df.columns][2:]

    # expand wide_to_long to put the year in a column and number of votes as the value
    long_df = pd.wide_to_long(
        long_df,
        [timeframe_prefix],
        i=["meeting_date", "midpoint"],
        j="year",
        suffix=r"\w+",
    )

    # drop any empty rows (meeting date/interest rate val/year combos with no participant votes)
    long_df.dropna(inplace=True)

    # sort by meeting date, projected year, midpoint value
    long_df.sort_values(by=["meeting_date", "year", "midpoint"], inplace=True)

    return long_df


def expand_df(df: pd.DataFrame) -> pd.DataFrame:
    """Expand long data to a format where each individual FOMC member's projections for a given year on a given meeting date are one row

    Args:
        df (pd.DataFrame): The long-formatted dataframe.

    Returns:
        pd.DataFrame: A DataFrame that can be used in our beeswarm template, where each individual FOMC member's projection has been expanded to a single row
    """

    expanded_df = df.copy()

    # We'll create a dummy column with an array of length n...
    # where n = the number of fed officials who supported a particular value for a particular year at a particular meeting
    expanded_df["dummy_col"] = expanded_df.apply(
        lambda row: [0 for _ in range(int(row["num_participants"]))], axis=1
    )
    # We can then explode the dataframe on the length of this dummy column, so we end up with one row per participant vote
    expanded_df = expanded_df.explode("dummy_col")

    # And then remove the dummy column and the count of participants (since this would now be duplicated across rows without meaning)
    expanded_df = expanded_df.drop(["dummy_col", "num_participants"], axis=1)

    return expanded_df


def format_for_beeswarm(
    df: pd.DataFrame, filter_last_year: bool = True
) -> pd.DataFrame:
    """Formats expanded data to match the format we need for our particular beeswarm template that we use for the dotplot

    Args:
        df (pd.DataFrame): The expanded dataframe.
        filter_last_year (bool): determines whether to limit the data to only FOMC meetings in the past year

    Returns:
        pd.DataFrame: A DataFrame that can be used in our beeswarm template, where each individual FOMC member's projection has been expanded to a single row and the columns/dates are correctly formatted
    """
    formatted_df = df.copy().reset_index()

    # For some formatting reasons, we want the rows with years to be sorted in descending order...
    # ...and the "longer run" rows to be sorted in ascending order (of meeting date), so we'll split here
    dated_projections = formatted_df.loc[formatted_df["year"] != "longer_run"]
    long_run_projections = formatted_df.loc[formatted_df["year"] == "longer_run"]

    # Then sort each of them how we want to
    dated_projections.sort_values(
        by=["meeting_date", "year", "midpoint"],
        inplace=True,
        ascending=[False, True, True],
    )
    long_run_projections.sort_values(
        by=["meeting_date", "year", "midpoint"], inplace=True
    )

    # Then re-concatenate them together
    formatted_df = pd.concat([dated_projections, long_run_projections], axis=0)

    # Filter to only the past year of meetings if filter_last_year is set to True
    if filter_last_year == True:
        formatted_df = formatted_df[
            formatted_df["meeting_date"]
            >= formatted_df["meeting_date"].max() - relativedelta(months=11)
        ]

    # Now we'll format the meeting dates into "MMM YYYY" format, which is what we want on the dropdowns
    formatted_df["meeting_date"] = formatted_df.apply(
        lambda row: datetime.strftime(row["meeting_date"], "%b %Y"), axis=1
    )

    # Rename "longer_run" to "Longer run"
    formatted_df.loc[formatted_df["year"] == "longer_run", "year"] = "Longer run"

    return formatted_df
