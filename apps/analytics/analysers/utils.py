try:
    import ifcopenshell
except Exception:  # pragma: no cover
    ifcopenshell = None


def open_ifc(file_path):
    if not ifcopenshell:
        return None
    return ifcopenshell.open(file_path)


def count_products_by_class(model):
    if model is None:
        return {}
    counts = {}
    for product in model.by_type("IfcProduct"):
        cls = product.is_a()
        counts[cls] = counts.get(cls, 0) + 1
    return counts
