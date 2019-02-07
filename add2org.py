import logging
from pathlib import Path
from typing import TypeVar, Generic, Dict, Sequence, Union, List, Tuple

from kython.klogging import setup_logzero
from kython.ktyping import PathIsh
from kython.kos import atomic_append
from kython.state import JsonState
from kython.org_tools import append_org_entry

Key = str
# I = TypeVar('I')
FormattedOrg = str # TODO perhaps we'll do something smarter later...
I = FormattedOrg
LoggerIsh = Union[str, logging.Logger]

def add2org(
        items: Union[List[Tuple[Key, I]], Dict[Key, I]],
        output: PathIsh,
        state: PathIsh,
        logger: LoggerIsh,
        org_formatter=None,
):
    if isinstance(items, dict):
        items = list(items.items())
    assert len(set(i[0] for i in items)) == len(items), 'Duplicate keys!!'

    output = Path(output)
    json_state = JsonState(Path(state))

    if isinstance(logger, str):
        logger = logging.getLogger(logger)
        setup_logzero(logger, level=logging.DEBUG)

    for k, i in items:
        if k in json_state:
            logger.debug('already handled: %s %s', k, i)
        else:
            logger.info('adding: %s %s', k, i)
            print(f'adding new item {k} {i}') # print since it's easier to track changes via kron emailing. maybe It's not the best way, dunno..
            atomic_append(
                output,
                i,
            )
            json_state[k] = repr(i)
