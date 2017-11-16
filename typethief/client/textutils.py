# typethief/client/textutils.py

def render_text(x, y, text, font, color=(0, 0, 0)):
    surf = font.render(text, True, color)
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
        for w in [w for w in l.split(' ') if w != '']:
            if wrapped and font.size('{} {}'.format(wrapped, w))[0] <= width:
                wrapped += ' ' + w
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
