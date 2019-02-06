#!/usr/bin/env python3
from kython.org_tools import as_org_entry
from my.hypothesis import get_todos

from add2org import add2org
from config import STATES, NOTES

def main():
    todos = get_todos()

    # TODO meh. maybe, use abstract OrgNote instead?
    items = [
        (
            t.eid,
            as_org_entry(
                heading=t.annotation,
                tags=['hyp2org', *t.tags],
                body=t.context,
                created=t.dt,
                todo=True,
            ),
        ) for t in todos
    ]

    add2org(
        items=items,
        output=NOTES.join('hyp2org.org'),
        state=STATES.join('hyp2org.json'),
        logger='hyp2org',
    )


if __name__ == '__main__':
    main()
