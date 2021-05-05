from data_connector import views
from django.conf.urls import url

PREFIX = r"^data-connector/"

urlpatterns = [
    url(PREFIX + r"data-types-for-devices$", views.get_data_types_for_devices),
    url(PREFIX + r"get-graph-data$", views.get_graph_data),
]
