import abc


class IReleaseStore(metaclass=abc.ABCMeta):
    """
    Interface to the underlying Bandcamp releases store
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'save') and
                callable(subclass.save) and
                hasattr(subclass, 'load') and
                callable(subclass.load) and
                hasattr(subclass, 'save_all') and
                callable(subclass.save_all) and
                hasattr(subclass, 'load_tags') and
                callable(subclass.load_tags) and
                hasattr(subclass, 'save_tags') and
                callable(subclass.save_tags) and
                hasattr(subclass, 'load_all') and
                callable(subclass.load_all) and
                hasattr(subclass, 'load_downloadable') and
                callable(subclass.load_downloadable)
        )


class PagedData:
    def __init__(self, page, cursor):
        self.page = page
        self.cursor = cursor
