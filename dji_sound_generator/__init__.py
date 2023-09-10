import typing as T
import numpy as np
import pandas as pd
from pathlib import Path

from . import (
    loader,
    processor,
    generator
)

def generate(
    file: T.Union[str, Path],
    sound: str
):
    df = loader.load(file)
    processor.process(df)

    pass
