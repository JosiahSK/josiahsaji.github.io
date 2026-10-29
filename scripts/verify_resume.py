import zlib
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

def parse_to_unicode(cmap_str):
    mapping = {}
    for block in re.findall(r'beginbfrange(.*?)endbfrange', cmap_str, re.DOTALL):
        for line in block.strip().splitlines():
            parts = line.strip().split()
            if len(parts) >= 3:
                start = int(parts[0].strip('<>'), 16)
                end = int(parts[1].strip('<>'), 16)
                if parts[2].startswith('['):
                    # Array of destinations
                    dests = [int(x.strip('<>'), 16) for x in parts[2:] if x not in '[]']
                    for idx, code in enumerate(range(start, end + 1)):
                        if idx < len(dests):
                            mapping[code] = chr(dests[idx])
                else:
                    dest_start = int(parts[2].strip('<>'), 16)
                    for code in range(start, end + 1):
                        mapping[code] = chr(dest_start + (code - start))

    for block in re.findall(r'beginbfchar(.*?)endbfchar', cmap_str, re.DOTALL):
        for line in block.strip().splitlines():
            parts = line.strip().split()
            if len(parts) >= 2:
                code = int(parts[0].strip('<>'), 16)
                dest = int(parts[1].strip('<>'), 16)
                mapping[code] = chr(dest)
    return mapping

def extract_pdf_text(pdf_path):
    with open(pdf_path, 'rb') as f:
        data = f.read()

    # Find fonts and their ToUnicode streams
    # Decompress all streams
    streams = re.findall(rb'stream[\r\n]+(.*?)[\r\n]+endstream', data, re.DOTALL)
    cmaps = []
    content_streams = []

    for s in streams:
        try:
            decomp = zlib.decompress(s).decode('latin1', errors='ignore')
            if 'beginbfrange' in decomp or 'beginbfchar' in decomp:
                cmaps.append(parse_to_unicode(decomp))
            elif 'BT' in decomp and 'ET' in decomp:
                content_streams.append(decomp)
        except Exception:
            pass

    # Merge all cmaps
    master_cmap = {}
    for cm in cmaps:
        master_cmap.update(cm)

    # Decode hex strings
    full_text = []
    for cs in content_streams:
        # Extract <hex> Tj or [(<hex>)...] TJ
        hex_tokens = re.findall(r'<([0-9a-fA-F]+)>', cs)
        for h in hex_tokens:
            # 4 hex chars = 1 code (usually 2 bytes)
            for i in range(0, len(h), 4):
                code = int(h[i:i+4], 16)
                full_text.append(master_cmap.get(code, ''))

    return "".join(full_text)

if __name__ == '__main__':
    text = extract_pdf_text('assets/resume/resume.pdf')
    print("Extracted text preview (first 400 chars):")
    print(repr(text[:400]))
    for kw in ['JOSIAH', 'SAJI', 'Evolve Robotics', 'Saintgits', 'Quadruped', 'micro-ROS', 'Jazzy', 'LiFePO4']:
        print(f"Keyword '{kw}': {'FOUND' if kw.lower() in text.lower() else 'MISSING'}")
