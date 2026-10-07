class ObjectModel:
    def __init__(self, object_id, class_name, value=None, elements=None):
        self.object_id = object_id
        self.class_name = class_name
        self.value = value
        self.elements = elements
        self.attributes = {}

    def set_attribute(self, name, value):
        self.attributes[name] = value

    def get_attribute(self, name):
        return self.attributes.get(name)

    def get_display_name(self):
        display_id = self.object_id.removeprefix("object_")
        return f"Object #{display_id} ({self.class_name})"

    def to_dict(self):
        result = {
            "object_id": self.object_id,
            "class_name": self.class_name,
            "attributes": self.attributes.copy()
        }
        if self.value is not None:
            result["value"] = self.value
        if self.elements is not None:
            result["elements"] = self.elements.copy() if isinstance(self.elements, (list, dict)) else self.elements
        return result

    def __repr__(self):
        return (
            f"ObjectModel("
            f"id={self.object_id}, "
            f"class={self.class_name}, "
            f"value={self.value}, "
            f"attributes={self.attributes}"
            f")"
        )