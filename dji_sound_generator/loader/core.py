import typing as T
import numpy as np
import pandas as pd
from pathlib import Path
import srt
import re

def load(
    file_path: T.Union[str, Path],
) -> pd.DataFrame:
    return pd.DataFrame([
        extract_subtitle_data(subtitle)
        for subtitle in load_srt(file_path)
    ])


def extract_subtitle_data(
    subtitle: srt.Subtitle
):
    record = {}
    for match in re.finditer(r"\[(?P<key>.*?)\s?:\s?(?P<value>.*?)\]", subtitle.content):
        key, value = match.group("key"), match.group("value")
        if key in [
            'longitude',
            'latitude',
            'altitude'
        ]:
            value = float(value)
        record[key] = value
    record["starttime"] = subtitle.start

    return record

def load_srt(
    file_path: T.Union[str, Path]
) -> list[srt.Subtitle]:
    with open(file_path, 'r', encoding='utf-8') as file:
        srt_content = file.read()

    # Parse the SRT content
    subtitles = list(srt.parse(srt_content))

    return subtitles
    
