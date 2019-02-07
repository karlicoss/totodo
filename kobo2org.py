#!/usr/bin/env python3
from kython.org_tools import as_org_entry
from my.books.kobo import get_todos

from add2org import add2org
from config import STATES, NOTES

def main():
    todos = get_todos()


    items = [
        (
            t.eid,
            as_org_entry(
                heading=t.annotation,
                tags=['kobo2org'],
                body=f'{t.text}\nfrom {t.book}',
                created=t.dt,
                todo=True,
            )
        ) for t in todos
    ]

    add2org(
        items=items,
        output=NOTES.joinpath('kobo2org.org'),
        state=STATES.joinpath('kobo2org.state'),
        logger='kobo2org',
    )


if __name__ == '__main__':
    main()
# # TODO ugh. krill is the same tool, really. just different rules for handling?
