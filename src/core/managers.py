from safedelete.managers import SafeDeleteManager


class ZenBaseManager(SafeDeleteManager):
    """
    Custom Base Manager
    """

    def get_queryset(self):
        return super().get_queryset().order_by("-created_on")
