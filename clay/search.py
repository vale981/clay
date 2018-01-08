"""
Components for search page.
"""
import urwid

from clay.gp import GP
from clay.songlist import SongListBox
from clay.notifications import NotificationArea
from clay.page import Page


class ArtistListBox(urwid.ListBox):
    """
    Widget that displays list of artists.
    """
    def __init__(self):
        self.walker = urwid.SimpleListWalker([])
        super(ArtistListBox, self).__init__(self.walker)


class SearchBox(urwid.Columns):
    """
    Widget that displays search input and results.
    """
    signals = ['search-requested']

    def __init__(self):
        self.query = urwid.Edit()
        super(SearchBox, self).__init__([
            ('pack', urwid.Text('Search: ')),
            self.query
        ])

    def keypress(self, size, key):
        """
        Handle keypress.
        """
        if key == 'enter':
            urwid.emit_signal(self, 'search-requested', self.query.edit_text)
            return None
        return super(SearchBox, self).keypress(size, key)


class SearchPage(urwid.Columns, Page):
    """
    Search page.

    Allows to perform searches & displays search results.
    """
    @property
    def name(self):
        return 'Search'

    @property
    def key(self):
        return 4

    def __init__(self, app):
        self.app = app
        self.songlist = SongListBox(app)

        self.search_box = SearchBox()

        urwid.connect_signal(self.search_box, 'search-requested', self.perform_search)

        super(SearchPage, self).__init__([
            urwid.Pile([
                ('pack', self.search_box),
                ('pack', urwid.Divider(u'\u2500')),
                self.songlist
            ])
        ])

    def perform_search(self, query):
        """
        Search tracks by query.
        """
        GP.get().search_async(query, callback=self.search_finished)

    def search_finished(self, results, error):
        """
        Populate song list with search results.
        """
        if error:
            NotificationArea.notify('Failed to search: {}'.format(str(error)))
            return

        self.songlist.populate(results.get_tracks())

    def activate(self):
        pass
