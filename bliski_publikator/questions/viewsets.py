from rest_framework import filters, viewsets

from .models import Question, Sheet
from .serializers import (
    QuestionSerializer,
    SheetSerializer
)


class SheetFilter(filters.FilterSet):
    class Meta:
        model = Sheet
        fields = ['monitoring_institution__institution',
                  'monitoring_institution__monitoring',
                  ]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.prefetch_related('condition_related', 'choice_set').all()
    serializer_class = QuestionSerializer


class SheetViewSet(viewsets.ModelViewSet):
    queryset = (Sheet.objects.
                select_related('monitoring_institution').
                select_related('monitoring_institution__monitoring').
                select_related('monitoring_institution__institution').
                with_answer().
                all())
    serializer_class = SheetSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SheetFilter
