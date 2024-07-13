from deepdiff import DeepDiff

def have_json(
    should_be,
    data,
    eq_length=False,
    ignore_order=False,
    exclude_ids=False
):
    exclude = ['dictionary_item_added', 'iterable_item_added']
    if eq_length:
        exclude.remove('iterable_item_added')
    
    def exclude_obj_callback(obj, path):
        if exclude_ids:
            return True if "id" in path else False
        return False

    diff = DeepDiff(should_be, data, ignore_order=ignore_order, exclude_obj_callback=exclude_obj_callback)
    for diff_type in exclude:
        if diff_type in diff:
            del diff[diff_type]

    return diff


def assert_have_json(
    should_be: dict,
    other: dict,
    eq_length: bool = True,
    ignore_order: bool = False,
    exclude_ids: bool = False,
):
    assert have_json(
        should_be,
        other,
        eq_length=eq_length,
        ignore_order=ignore_order,
        exclude_ids=exclude_ids
    ) == {}