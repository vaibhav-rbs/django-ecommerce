from rest_framework import mixins, generics, request, permissions
from main.serializer import StatusReportSerializer
from main.models import StatusReport
from main.permissions import IsOwnerOrReadOnly

class StatusCollection(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = StatusReport.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = StatusReportSerializer

    def get(self, requst):
        return self.list(request)

    def post(self, reqeust):
        return self.create(reqeust)


class StatusMember(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = StatusReport.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
    serializer_class = StatusReportSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):    
        return self.put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):    
        return self.destroy(request, *args, **kwargs)
