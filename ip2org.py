#!/usr/bin/env python3
from kython.org_tools import as_org_entry
from my.instapaper import get_todos

from add2org import add2org
from config import STATES, NOTES

# these three files are still 90% same! maybe I could generalise even more...
def main():
    todos = get_todos()

    # TODO meh. maybe, use abstract OrgNote instead?
    items = [
        (
            t.uid,
            as_org_entry(
                heading=t.note,
                tags=['ip2org'],
                body=f'{t.text}\nfrom {t.title} {t.url}',
                created=t.dt,
                todo=True,
            ),
        ) for t in todos
    ]

    add2org(
        items=items,
        output=NOTES.joinpath('ip2org.org'),
        state=STATES.joinpath('ip2org.json'),
        logger='ip2org',
    )


if __name__ == '__main__':
    main()
