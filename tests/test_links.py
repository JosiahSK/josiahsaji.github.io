import os
import glob
from collections import Counter
from html.parser import HTMLParser

class ComprehensiveDOMParser(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.ids = []
        self.srcs = []
        self.hrefs = []
        self.meta_tags = []
        self.link_tags = []
        self.headings = []
        self.images = []
        self.anchors = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)

        # 1. Element ID
        if 'id' in attr_dict:
            self.ids.append(attr_dict['id'])

        # 2. Local/external href
        if 'href' in attr_dict:
            self.hrefs.append({
                'tag': tag,
                'href': attr_dict['href'],
                'target': attr_dict.get('target'),
                'rel': attr_dict.get('rel', '')
            })

        # 3. Source assets
        if 'src' in attr_dict:
            self.srcs.append({
                'tag': tag,
                'src': attr_dict['src']
            })

        # 4. Meta tags (OpenGraph & Twitter)
        if tag == 'meta':
            self.meta_tags.append(attr_dict)

        # 5. Link tags (favicon / preconnect / stylesheet)
        if tag == 'link':
            self.link_tags.append(attr_dict)

        # 6. Heading hierarchy
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            level = int(tag[1])
            self.headings.append(level)

        # 7. Images alt text
        if tag == 'img':
            self.images.append({
                'src': attr_dict.get('src', ''),
                'alt': attr_dict.get('alt')
            })

def test_portfolio_quality():
    html_files = sorted(glob.glob('*.html'))
    print(f"Scanning HTML files with html.parser: {html_files}")

    errors = []
    total_ids = 0
    total_srcs = 0
    total_hrefs = 0
    total_headings = 0
    total_images = 0

    # 1. Parse all documents
    parsed_docs = {}
    for hf in html_files:
        with open(hf, 'r', encoding='utf-8') as f:
            content = f.read()

        parser = ComprehensiveDOMParser(hf)
        parser.feed(content)
        parsed_docs[hf] = (parser, content)

    # 2. Audit each document
    for hf, (parser, raw_content) in parsed_docs.items():
        # A. Unique element IDs
        id_counts = Counter(parser.ids)
        total_ids += len(parser.ids)
        for el_id, count in id_counts.items():
            if count > 1:
                errors.append(f"[{hf}] Duplicate element id: '{el_id}' appears {count} times")
        page_id_set = set(parser.ids)

        # B. Heading hierarchy
        total_headings += len(parser.headings)
        h1_count = parser.headings.count(1)
        if h1_count != 1:
            errors.append(f"[{hf}] Document must have exactly one <h1>, found {h1_count}")
        for i in range(len(parser.headings) - 1):
            curr, nxt = parser.headings[i], parser.headings[i+1]
            if nxt > curr + 1:
                errors.append(f"[{hf}] Heading level skipped: <h{curr}> followed by <h{nxt}>")

        # C. Image alt attributes
        total_images += len(parser.images)
        for img in parser.images:
            if img['alt'] is None:
                errors.append(f"[{hf}] Image missing alt attribute: {img['src']}")

        # D. Source assets exist locally
        for item in parser.srcs:
            src = item['src']
            if src.startswith(('http://', 'https://', 'data:')):
                continue
            total_srcs += 1
            if not os.path.exists(src):
                errors.append(f"[{hf}] Missing active src file: {src}")

        # E. Href targets & Anchor validity
        for link in parser.hrefs:
            href = link['href']
            # External target="_blank" safety
            if link['target'] == '_blank':
                rel = link['rel'].lower()
                if 'noopener' not in rel or 'noreferrer' not in rel:
                    errors.append(f"[{hf}] Blank link missing rel='noopener noreferrer': href={href}")

            if href.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                continue

            # Local anchor on same page
            if href.startswith('#'):
                anchor = href[1:]
                if anchor and anchor not in page_id_set:
                    errors.append(f"[{hf}] Target anchor #{anchor} not found on page")
                continue

            total_hrefs += 1
            target_path = href.split('#')[0]
            anchor = href.split('#')[1] if '#' in href else None
            if target_path and not os.path.exists(target_path):
                errors.append(f"[{hf}] Missing local link target: {target_path}")
            elif target_path and anchor:
                if target_path in parsed_docs:
                    target_id_set = set(parsed_docs[target_path][0].ids)
                    if anchor not in target_id_set:
                        errors.append(f"[{hf}] Cross-page anchor #{anchor} not found in {target_path}")

        # F. Social Meta Image Absolute URLs
        for m in parser.meta_tags:
            prop = m.get('property', '')
            name = m.get('name', '')
            if prop in ('og:image', 'twitter:image') or name in ('og:image', 'twitter:image'):
                content_val = m.get('content', '')
                if not content_val.startswith('https://'):
                    errors.append(f"[{hf}] Meta tag {prop or name} must use absolute https URL, found: '{content_val}'")

        # G. Strict Claim Verification (Banned / Unsupported substrings)
        # Check for unverified compiled latency claim in quadruped locomotion context
        if 'quadruped' in hf or hf == 'index.html':
            banned_patterns = [
                'sub-10 µs compiled',
                'sub-10 us compiled',
                '<10 µs c++',
                '< 10 µs compiled'
            ]
            for bp in banned_patterns:
                if bp in raw_content.lower():
                    errors.append(f"[{hf}] Found unverified compiled latency claim: '{bp}'")

    print("\nVerified across DOM elements:")
    print(f"  • {len(html_files)} HTML documents parsed via html.parser")
    print(f"  • {total_ids} element IDs (all unique per document)")
    print(f"  • {total_headings} headings checked (strict h1-h6 hierarchy)")
    print(f"  • {total_images} images verified for accessible alt text")
    print(f"  • {total_srcs} local source assets confirmed on disk")
    print(f"  • {total_hrefs} local href and cross-document anchors verified")
    print("  • All social meta images use absolute https URLs")
    print("  • All external target='_blank' links have rel='noopener noreferrer'")
    print("  • Quadruped IK benchmarks purged of unverified compiled claims")

    if errors:
        print(f"\nFAILED with {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        exit(1)
    else:
        print("\nALL PORTFOLIO V4.1 PRODUCTION HARDENING TESTS PASSED!")

if __name__ == '__main__':
    test_portfolio_quality()
