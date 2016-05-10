class M2MFieldFormMixin(object):
    def save_m2m_field(self, field, left, right, thr=None):
        thr = thr or getattr(self._meta.model, field).through
        form_data = self.cleaned_data[field]
        model_data = getattr(self.instance, field).all()

        to_remove = set(model_data) - set(form_data)
        thr.objects.filter(**{left: self.instance, (right+"__in"): to_remove}).all().delete()

        to_add = set(form_data) - set(model_data)
        thr.objects.bulk_create(thr(**{left: self.instance, right: obj}) for obj in to_add)
