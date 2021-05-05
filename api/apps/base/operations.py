from django.core import serializers


# Convert various data types into JSON serialzable
# @param {*} value Value to be converted
# @param {*} field Django model field type
# @return {*} data which is JSON serializable
def convert_data_format(value, field):
    field_type = field.get_internal_type()

    if type(value) == str:
        return value
    if field_type == "DateTimeField" and value is not None:
        value = value.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    elif field_type == "DurationField" and value is not None:
        value = value.total_seconds()
    elif field_type == "TimeField" and value is not None:
        value = value.strftime("%H:%M:%S")
    elif field_type == "ArrayField" and value is not None:
        value = list([convert_data_format(sub_value, field.base_field) for sub_value in value])
    elif field_type == "UUIDField" and value is not None:
        value = str(value)
    elif field_type == "ForeignKey" or field_type == "ManyToManyField" or field_type == "OneToOneField":
        try:
            value = serializers.serialize("json", value.all())
        except AttributeError:
            value = value.__repr__()
    return value


def set_custom_field_logs(old_value, new_value, field):

    customfields = set(old_value.keys())
    if new_value:
        customfields.update(new_value.keys())

    new_custom_field = {"custom_field": {}}
    old_custom_field = {"custom_field": {}}
    for f in customfields:
        new_value_to_update = {}
        old_value_to_update = {}
        if f in new_value.keys() and f in old_value.keys():
            if old_value[f] != new_value[f]:
                new_value_to_update = {f: new_value[f]}
                old_value_to_update = {f: old_value[f]}
        elif f in old_value.keys() and f not in new_value.keys():
            new_value_to_update = {f: "null"}
            old_value_to_update = {f: old_value[f]}
        elif f in new_value.keys() and f not in old_value.keys():
            new_value_to_update = {f: new_value[f]}
            old_value_to_update = {f: "null"}
        new_custom_field["custom_field"].update(convert_data_format(new_value_to_update, field))
        old_custom_field["custom_field"].update(convert_data_format(old_value_to_update, field))

    return new_custom_field, old_custom_field


# Get modification when Model is updated
# @param {object} old Old Model instance
# @param {object} new Modified Model instance
# @param {list} model_fields Model instance field list
# @param {string} action_type Model instance save action - "CREATE", "UPDATE", "REMOVE", "ACTIVATE"...
# @param {list} drop_fields, fields that you don't want to get
# @return {JSON} JSON data which contains `old` and `new` attr
def get_modification(old, new, model_fields, action_type, drop_fields=[]):
    new_json = {}
    old_json = {}

    if action_type == "CREATE":
        for field in model_fields:
            new_json[field.name] = convert_data_format(getattr(new, field.name, None), field)
    elif action_type == "REMOVE":
        for field in model_fields:
            old_json[field.name] = convert_data_format(getattr(old, field.name, None), field)
    else:
        diff_fields = list(
            filter(lambda field: (getattr(old, field.name, None) != getattr(new, field.name, None)), model_fields)
        )

        for field in diff_fields:
            if field.name not in drop_fields:
                new_value = getattr(new, field.name, None)
                old_value = getattr(old, field.name, None)
                if field.name is "custom_field":
                    old_custom_field, new_custom_field = set_custom_field_logs(new_value, old_value, field)
                    new_json.update(new_custom_field)
                    old_json.update(old_custom_field)
                else:
                    new_json[field.name] = convert_data_format(new_value, field)
                    old_json[field.name] = convert_data_format(old_value, field)

    if new_json or old_json:
        return {"old": old_json, "new": new_json}

    return False


def update_or_delete_custom_field(current_model, instance):
    custom_field_to_delete = []
    for cf in instance.custom_field:
        if instance.custom_field[cf] is None:
            custom_field_to_delete.append(cf)
        if cf in current_model.custom_field.keys():
            current_model.custom_field[cf] = instance.custom_field[cf]

    for e in custom_field_to_delete:
        if e in instance.custom_field:
            instance.custom_field.pop(e)
        if e in current_model.custom_field:
            current_model.custom_field.pop(e)
    instance.custom_field.update(current_model.custom_field)
