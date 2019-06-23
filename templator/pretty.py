import json


def jsonify(obj):
    """
    Convert serializable object to string.

    If Pygments is present, it will be used to colorify the json blob.
    :param list[dict] obj: object to be serialized.
    :returns: serialized json string.
    :rtype: string
    """
    formatted_json = json.dumps(obj, indent=4)

    try:
        from pygments import highlight, lexers, formatters
        colorful_json = highlight(
            formatted_json,
            lexers.JsonLexer(),
            formatters.TerminalFormatter()
        )
    except ImportError:
        return formatted_json

    return colorful_json
