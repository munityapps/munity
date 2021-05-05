from django.contrib import admin

from .models import Device
from django.conf import settings

from django.template.response import TemplateResponse
from django.urls import path
import csv
import io


def is_device_model(key):
    fields = (
        "name",
        "reference",
        "address",
        "position",
        "description",
        "custom_field",
    )
    if key not in fields:
        return False, key
    else:
        return True, key


# Device Model
class DeviceAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "reference",
        "address",
        "position",
        "description",
        "last_triggered_timestamps",
        "custom_field",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = (
        "name",
        "reference",
        "address",
        "position",
        "description",
        "last_triggered_timestamps",
        "custom_field",
    )
    # A handy constant for the name of the alternate database.

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path("add_devices/", self.admin_site.admin_view(self.add_devices, cacheable=True))]

        return my_urls + urls

    def add_devices(self, request):

        context = dict(self.admin_site.each_context(request),)
        if request.method == "POST":
            devices = []
            info = []
            if "bulk-create-paste" in request.FILES.keys():

                f = request.FILES["bulk-create-paste"]
                file = f.read().decode("utf-8")
                reader = csv.DictReader(io.StringIO(file))
                headers = reader.fieldnames

                headers_result = map(is_device_model, headers)
                header_error = False
                for header_result in headers_result:
                    header_result_list = list(header_result)
                    if not header_result_list[0]:
                        info.append(f"'{header_result_list[1]}' is not a field compliant with Device Model")
                        header_error = True
                if not header_error:
                    for key, line in enumerate(reader):
                        if "reference" in line.keys():
                            device = Device(
                                reference=line["reference"],
                                name=line["name"]
                                if "name" in line.keys()
                                else line["reference"],
                                address=line["address"] if "address" in line.keys() else "",
                                position=line["position"] if "address" in line.keys() else "",
                                description=line["description"]
                                if "address" in line.keys()
                                else "",
                                custom_field=line["custom_field"] if "custom_field" in line.keys() else {},
                            )
                            devices.append(device)

                    devices_created_ref = [device.reference for device in devices]
                    self.get_db_using(request)
                    devices_created = Device.objects.using(self.using).filter(reference__in=devices_created_ref)
                    num_results = devices_created.count()

                    if num_results == 0:
                        devices_created = Device.objects.using(self.using).bulk_create(devices)
                        context["created"] = created
                    else:
                        info.append(
                            f"{[device.reference for device in devices_created]} already exist in workspace_{self.using}"
                        )
                else:
                    info.append(
                        "'reference', "
                        "'name', "
                        "'address', "
                        "'position', "
                        "'description' and "
                        "'custom_field' are accepted"
                    )
            else:
                info.append("No file loaded")

            context["info"] = info
        return TemplateResponse(request, "admin/devices/device/add-devices.html", context)

    def has_add_permission(self, request):
        return True

admin.site.register(Device, DeviceAdmin)
