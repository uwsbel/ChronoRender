def convert(data=[], *args, **kwargs):
    for entry in data:
        entry['pos_z'] = entry['pos_z'] * 555
    return data
