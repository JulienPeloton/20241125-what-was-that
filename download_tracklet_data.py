#!/usr/bin/env python
# Copyright 2024 Julien Peloton
# Author: Julien Peloton
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Download and save tracklet data from Fink"""

import io
import requests
import pandas as pd

import logging

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


def get_tracklet_candidates(date):
    """Get alert data associated with tracklets for a given date

    Parameters
    ----------
    date: str
        date. Format: YYYY-MM-DD hh:mm:dd.
        You can use shorter versions such as
        YYYY-MM, YYYY-MM-DD, or YYYY-MM-DD hh.

    Returns
    -------
    out: pd.DataFrame
        Pandas DataFrame with Tracklet data.
    """
    logging.info("Downloading...")
    r = requests.post(
        "https://fink-portal.org/api/v1/tracklet",
        json={"date": date, "output-format": "json"},
    )

    # Format output in a DataFrame
    pdf = pd.read_json(io.BytesIO(r.content))
    return pdf


date = "2024-11-25"
pdf_alerts = get_tracklet_candidates(date)

pdf_objects = pdf_alerts.groupby("d:tracklet").size()

logging.info(
    "{:,} candidates ({:,} unique tracklets) found in {}".format(
        len(pdf_alerts), len(pdf_objects), date
    )
)

# Save it into parquet
pdf_alerts.to_parquet("fink_tracklet_20241125.parquet")
