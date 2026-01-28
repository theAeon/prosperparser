"""CLI for calling into parse"""

from dataclasses import dataclass
from typing import Annotated, TextIO

import cappa

from . import constants, parse


def valid_thresh(value: float):
    if 0 <= value <= 1:
        return value
    msg = "threshold must be a decimal probability"
    raise ValueError(msg)


def gt_zero(value: int):
    if value <= 0:
        msg = "top must be more than zero"
        raise ValueError(msg)
    return value


def valid_protease(value: list[str]):
    validated: list[str] = []
    for i in range(len(value)):
        if value[i] in constants.ids:
            validated.append(value[i])
        elif value[i] in constants.names:
            validated.append(constants.dict_map[value[i]])
        else:
            msg = f"invalid protease at {i}"
            raise ValueError(msg)
    return validated


@dataclass
class ProsperParser:
    """ProsperParser
    A program for parsing ProsperousPlus outputs"""

    input: Annotated[TextIO, cappa.Arg.required, cappa.FileMode(mode = "r", encoding = "utf-8")]
    """results.csv from ProsperousPlus"""

    output: Annotated[None | TextIO, cappa.Arg(default = None), cappa.FileMode(mode = "w", encoding = "utf-8")]
    """file to write output"""

    protease: Annotated[
        None | list[str],
        cappa.Arg(parse=[cappa.default_parse, valid_protease], action = cappa.ArgAction.append, short="-p", long=True),
    ]
    """full protein name or merops id from table S1"""

    sequence: Annotated[None | str, cappa.Arg(short="-s", long=True)]
    """sequence name for filtering output"""

    top: Annotated[
        None | int,
        cappa.Arg(parse=[cappa.default_parse, gt_zero], short="-n", long=True),
    ]
    """print top n results per sequence"""

    threshold: Annotated[
        None | float,
        cappa.Arg(
            parse=[cappa.default_parse, valid_thresh],
            short="-t",
            long=True,
        ),
    ] = None
    """Probability score cutoff"""


def run():
    args = cappa.parse(ProsperParser)
    parse.parse_csv(args)
