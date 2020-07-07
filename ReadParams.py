
def read_dict(filepath):

    send = {}
    with open(filepath) as file:
        for line in file:
            key, value = line.partition('=')[::2]
            send[key.strip()] = value.strip()
    return send