from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from .serializers import PackageSerializer
from .models import Package


class PackageAPISet(viewsets.ModelViewSet):
    """
    Model View Set for Packages
    """

    serializer_class = PackageSerializer
    queryset = Package.objects.all()
    permission_classes = []
    lookup_field = "pk"
    http_method_names = ("get", "post", "patch", "delete")
    filter_backends = (SearchFilter,)
    search_fields = ("title", "registry__title")
