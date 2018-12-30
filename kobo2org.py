#!/usr/bin/env python3
import logging
from pathlib import Path

from my.books.kobo import by_annotation, Highlight

from kython.state import JsonState
from kython.logging import setup_logzero
from kython.org import as_org_entry, append_org_entry


def get_logger():
    return logging.getLogger('kobo2org')

def description(d: Highlight):
    return f"{d.dt}: {d.summary} {d.text} {d.annotation}"

# TODO ugh. krill is the same tool, really. just different rules for handling?
class Kobo2Org:
    def __init__(self):
        self.state = JsonState(
            '/L/Dropbox/misc/states/kobo2org.state',
        )
        self.logger = get_logger()
        self.org_file = Path('/L/Dropbox/mobile/notes/kobo2org.org')

    def handled(self, d: Highlight) -> bool:
        return d.eid in self.state.get()

    def add_to_org(self, d: Highlight):
        print("Adding new item: " + description(d))
        append_org_entry(
            self.org_file,
            heading=d.annotation,
            body=f'{d.text}\nfrom {d.book}',
            created=d.dt,
            tags=['kobo2org'],
        )

    def mark_done(self, d: Highlight):
        st = self.state.get()
        st[d.eid] = description(d)
        self.state.update(st)

    def run(self):
        def with_todo(ann) -> bool:
            if ann is None:
                ann = ''
            return 'todo' in ann.lower().split()
            
        for d in by_annotation(with_todo):
            if self.handled(d):
                self.logger.debug('already handled: %s', d)
            else:
                self.logger.info('adding: %s', d)
                self.add_to_org(d)
                self.mark_done(d)

def main():
    setup_logzero(get_logger(), level=logging.DEBUG)
    kobo2org = Kobo2Org()
    kobo2org.run()

if __name__ == '__main__':
    main()

