# typethief/client/textutils.py

def render_text(x, y, text, font, color=(0, 0, 0), background=None):
    surf = font.render(text, True, color, background)
    rect = surf.get_rect()
    rect.x = x
    rect.y = y
    return surf, rect


def wrap_text(text, font, width=None):
    lines = text.split('\n')
    if not width or width == 0:
        return lines

    wrapped_lines = []
    for l in lines:
        wrapped = ''
        words = [w + ' ' for w in l.split(' ')]
        words[-1].rstrip() # todo: deal with empty case

        for w in words:
            if wrapped and font.size('{} {}'.format(wrapped, w))[0] <= width:
                wrapped += w
            elif not wrapped:
                wrapped = w
            else:
                wrapped_lines.append(wrapped)
                wrapped = w

        if wrapped:
            wrapped_lines.append(wrapped)
        wrapped_lines.append('')

    if wrapped_lines:
        del wrapped_lines[-1]

    return wrapped_lines


def render_lines(x, y, lines, font, color=(0, 0, 0)):
    surfrects = []
    for l in lines:
        surfrects.append(render_text(x, y, l, font, color))
        y += font.size(l)[1]
    return surfrects


_KEYS = {
    48:  ('0', ')'),
    49:  ('1', '!'),
    50:  ('2', '@'),
    51:  ('3', '#'),
    52:  ('4', '$'),
    53:  ('5', '%'),
    54:  ('6', '^'),
    55:  ('7', '&'),
    56:  ('8', '*'),
    57:  ('9', '('),
    97:  ('a', 'A'),
    98:  ('b', 'B'),
    99:  ('c', 'C'),
    100: ('d', 'D'),
    101: ('e', 'E'),
    102: ('f', 'F'),
    103: ('g', 'G'),
    104: ('h', 'H'),
    105: ('i', 'I'),
    106: ('j', 'J'),
    107: ('k', 'K'),
    108: ('l', 'L'),
    109: ('m', 'M'),
    110: ('n', 'N'),
    111: ('o', 'O'),
    112: ('p', 'P'),
    113: ('q', 'Q'),
    114: ('r', 'R'),
    115: ('s', 'S'),
    116: ('t', 'T'),
    117: ('u', 'U'),
    118: ('v', 'V'),
    119: ('w', 'W'),
    120: ('x', 'X'),
    121: ('y', 'Y'),
    122: ('z', 'Z'),
    96: ('`', '~'),
    45: ('-', '_'),
    61: ('=', '+'),
    91: ('[', '{'),
    93: (']', '}'),
    92: ('\\', '|'),
    59: (';', ':'),
    39: ("'", '"'),
    44: (',', '<'),
    46: ('.', '>'),
    47: ('/', '?'),
    32: (' ', None)
}


def to_char(n, shifted=False):
    if n not in _KEYS:
        return None
    base, shift = _KEYS[n]
    return shift if shifted else base
