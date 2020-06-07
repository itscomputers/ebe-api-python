def string_to_list(string, data_type):
    return list(map(data_type, string.split(',')))

def string_to_int_list(string):
    return string_to_list(string, int)

