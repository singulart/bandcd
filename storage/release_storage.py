import abc


class IReleaseStore(metaclass=abc.ABCMeta):
    """Interface to the underlying Bandcamp releases store"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'save') and
                callable(subclass.save) and
                hasattr(subclass, 'load') and
                callable(subclass.load) and
                hasattr(subclass, 'save_all') and
                callable(subclass.saveAll) and
                hasattr(subclass, 'load_all') and
                callable(subclass.loadAll)
        )
