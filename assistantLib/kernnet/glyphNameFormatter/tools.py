import struct


def camelCase(pattern):
    if len(pattern) == 0:
        return ""
    if "-" in pattern:
        t = ""
        for p in pattern.split("-"):
            t += camelCase(p)
        return t
    return pattern[0].upper()+pattern[1:].lower()


def unicodeToChar(uni):
    if uni < 0xFFFF:
        return unichr(uni)
    else:
        return struct.pack('i', uni).decode('utf-32')


def charToUnicode(char):
    if len(char) != 2:
        return ord(char)
    return 0x10000 + (ord(char[0]) - 0xD800) * 0x400 + (ord(char[1]) - 0xDC00)


def debug(uniNumber):
    # dump the steps of building the name
    import glyphNameFormatter
    g = glyphNameFormatter.GlyphName(uniNumber)
    name = g.getName(extension=True)
    count = 0
    print("Debugging: %s" % name)
    print("uninumber: %04X" % uniNumber)
    print("uni range: %s" % g.uniRangeName)
    print("{0:<5} {1:<30} {2:<30} {3:<30} {4:<30}".format("Step", "Look For", "Replace With", "Before", "After"))
    for lookFor, replaceWith, before, after in g._log:
        count += 1
        print("{0:<5} {1:<30} {2:<30} {3:<30} {4:<30}".format(count, lookFor, replaceWith, before, after))
    print("\nSuffixes: %s" % " ".join(g.suffixParts))


class GlyphNameFormatterError(Exception):
    pass


if __name__ == "__main__":
    assert camelCase("aaaa") == "Aaaa"
    assert camelCase("aaaA") == "Aaaa"
    assert camelCase("aaaa-aaaa") == "AaaaAaaa"
    assert camelCase("aaaa-") == "Aaaa"
    assert camelCase("-") == ""
    assert camelCase("") == ""

    debug(0x0300)
