from rest_framework import mixins, generics, request
from main.serializer import StatusReportSerializer
from main.models import StatusReport

class StatusCollection(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = StatusReport.objects.all()
    serializer_class = StatusReportSerializer

    def get(self, requst):
        return self.list(request)

    def post(self, reqeust):
        return self.create(reqeust)


class StatusMember(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = StatusReport.objects.all()
    serializer_class = StatusReportSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):    
        return self.destroy(request, *args, **kwargs)
