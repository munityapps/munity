from rest_framework import serializers


class ModelSerializerWithFields(serializers.ModelSerializer):
    """Custom ModelSerializer that lets you choose which fields will be returned by the serializer
    when you instanciate it.
    """

    def __init__(self, *args, **kwargs):

        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)
        exclude = kwargs.pop("exclude", None)
        assert not (
            fields and exclude
        ), f"Cannot set both 'fields' and 'exclude' options on serializer ModelSerializerWithFields."

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        elif exclude is not None:
            # Drop any fields that are specified in the `exclude` argument.
            for field_name in exclude:
                self.fields.pop(field_name)
