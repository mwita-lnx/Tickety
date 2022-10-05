import django_filters
from django_filters import DateFilter, CharFilter

from .models import Event

class EventFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name="start_date", lookup_expr='gte')
	end_date = DateFilter(field_name="start_date", lookup_expr='lte')
	title = CharFilter(field_name='title', lookup_expr='icontains')
	about = CharFilter(field_name='about', lookup_expr='icontains')


	class Meta:
		model = Event
		fields = '__all__'
		exclude = [ 'has_categories','pin_location','thumbnail','ticket_size','user']