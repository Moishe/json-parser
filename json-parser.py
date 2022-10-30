import re

def eval_bool(v):
    if v == 'true':
        return True
    elif v == 'false':
        return False
    else:
        raise Exception('invalid boolean %s' % v)

xlat = [
    ('".*?"', str),
    ('\d+', int),
    ('true|false', eval_bool),
    ('null', lambda x: None)
]

JSON_TOKENS = ['{', '}', '[', ']', ',', ':']

def match(str, regex):
    m = re.match(regex, str)
    if not m:
        return (None, str)
    else:
        return (m[0], str[len(m[0]):])

def tokenize(str):
    tokens = []
    while str:
        for (x, f) in xlat:
            t, str = match(str, x)
            if t:
                tokens.append(f(t))
                break

        if str[0] in JSON_TOKENS:
            tokens.append(str[0])
        elif not str[0].isspace():
            raise Exception('invalid character')

        str = str[1:]

    return tokens

def parse_object(tokens):
    obj = {}
    while tokens[0] != '}':
        key = tokens[0]
        if tokens[1] != ':':
            raise Exception('bad separator')
        tokens, value = parse(tokens[2:])
        obj[key] = value
        if tokens[0] == ',':
            tokens = tokens[1:]
    return (tokens[1:], obj)

def parse_array(tokens):
    arr = []
    while tokens[0] != ']':
        tokens, value = parse(tokens)
        arr.append(value)
        if tokens[0] == ',':
            tokens = tokens[1:]

    return (tokens[1:], arr)

def parse(tokens):
    if tokens[0] == '{':
        return parse_object(tokens[1:])
    elif tokens[0] == '[':
        return parse_array(tokens[1:])
    elif tokens[0] not in JSON_TOKENS:
        return (tokens[1:], tokens[0])

def loads(str):
    tokens = tokenize(str)
    parsed = parse(tokens)
    return parsed[1]

if __name__ == "__main__":
    test = '{"aardvark": "bird", "cockatoo": 5, "dingo": [1,23,345,4567], "cat": true, null: "dog"}'
    result = loads(test)
    print(result)

