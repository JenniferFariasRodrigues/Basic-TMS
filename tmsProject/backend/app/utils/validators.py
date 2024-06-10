def are_items_compatible(items):
    incompatible_pairs = [
        ('apple', 'broccoli'),
        ('banana', 'lettuce'),
        ('tomato', 'cucumber'),
        ('potato', 'onion'),
        ('melon', None)
    ]
    item_names = [item.name for item in items]
    for pair in incompatible_pairs:
        if pair[1] is None and pair[0] in item_names:
            if len(item_names) > 1:
                return False
        elif pair[0] in item_names and pair[1] in item_names:
            return False
    return True
