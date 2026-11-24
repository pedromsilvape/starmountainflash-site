import re, html as H
TAG = re.compile(r'(<script\b.*?</script>|<style\b.*?</style>|<svg\b.*?</svg>|<[^>]+>)', re.S | re.I)
ATTR = re.compile(r'\b(alt|aria-label|title|data-txt|data-name|placeholder)="([^"]*)"')
def has_word(s): return re.search(r'[A-Za-zÀ-ÿ]{2,}', s) is not None
def texts(h):
    out = []
    for part in TAG.split(h):
        if not part or part.startswith('<'):
            if part and part.startswith('<') and not part.startswith(('<script', '<style', '<svg')):
                for m in ATTR.finditer(part):
                    v = H.unescape(m.group(2)).strip()
                    if v and has_word(v): out.append(v)
            continue
        v = H.unescape(part).strip()
        if v and has_word(v): out.append(re.sub(r'\s+', ' ', v))
    return out
def translate(h, D, miss=None):
    res = []
    for part in TAG.split(h):
        if not part: continue
        if part.startswith('<'):
            if not part.startswith(('<script', '<style', '<svg')):
                def ra(m):
                    v = H.unescape(m.group(2)).strip()
                    if v in D: return f'{m.group(1)}="{H.escape(D[v], quote=True)}"'
                    if miss is not None and v and has_word(v): miss.add(v)
                    return m.group(0)
                part = ATTR.sub(ra, part)
            res.append(part); continue
        raw = H.unescape(part); v = re.sub(r'\s+', ' ', raw).strip()
        if v and v in D:
            lead = raw[:len(raw) - len(raw.lstrip())]; trail = raw[len(raw.rstrip()):]
            res.append(H.escape(lead + D[v] + trail, quote=False))
        else:
            if miss is not None and v and has_word(v): miss.add(v)
            res.append(part)
    return ''.join(res)
