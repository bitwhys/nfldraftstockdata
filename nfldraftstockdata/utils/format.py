def remove_instance_of(str_value, chars):
    str_value = str_value.strip()
    if type(chars) == "list":
        for c in chars:
            str_value = str_value.strip(c)
    else:
        str_value = str_value.strip(chars)

    return str_value
