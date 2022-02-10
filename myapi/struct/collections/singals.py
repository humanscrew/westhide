from datetime import datetime
from mongoengine import signals


def handler(event):
    def decorator(fn):
        def apply(cls):
            event.connect(fn, sender=cls)
            return cls

        fn.apply = apply
        return fn

    return decorator


@handler(signals.pre_save)
def onupdate(sender, document):
    document.updatedAt = datetime.utcnow()
