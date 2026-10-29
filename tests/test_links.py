import os
import re
import glob
from collections import Counter

def test_links_and_assets():
    html_files = sorted(glob.glob('*.html'))
    print(f"Scanning HTML files: {html_files}")
    
    errors = []
    checked_srcs = 0
    checked_hrefs = 0
    checked_meta_assets = 0
    checked_headings = 0
    checked_images_alt = 0
    
    for hf in html_files:
        with open(hf, 'r', encoding='utf-8') as f:
            raw_content = f.read()
        
        # Strip HTML comments to only evaluate active DOM elements
        active_content = re.sub(r'<!--.*?-->', '', raw_content, flags=re.DOTALL)
        
        # 1. Duplicate ID validation
        all_ids = re.findall(r'id=["\']([^"\']+)["\']', active_content)
        counts = Counter(all_ids)
        for element_id, count in counts.items():
            if count > 1:
                errors.append(f"[{hf}] Duplicate element id detected: '{element_id}' appears {count} times")
        page_ids = set(all_ids)
        
        # 2. Check active src attributes
        srcs = re.findall(r'src=["\']([^"\']+)["\']', active_content)
        for src in srcs:
            if src.startswith(('http://', 'https://', 'data:')):
                continue
            checked_srcs += 1
            if not os.path.exists(src):
                errors.append(f"[{hf}] Missing active src file: {src}")
                
        # 3. Check active href attributes
        hrefs = re.findall(r'href=["\']([^"\']+)["\']', active_content)
        for href in hrefs:
            if href.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                continue
            if href.startswith('#'):
                anchor = href[1:]
                if anchor and anchor not in page_ids:
                    errors.append(f"[{hf}] Target anchor #{anchor} not found on page")
                continue
            checked_hrefs += 1
            target_path = href.split('#')[0]
            anchor = href.split('#')[1] if '#' in href else None
            if target_path and not os.path.exists(target_path):
                errors.append(f"[{hf}] Missing local link target: {target_path}")
            elif target_path and anchor:
                with open(target_path, 'r', encoding='utf-8') as tf:
                    target_content = tf.read()
                target_ids = set(re.findall(r'id=["\']([^"\']+)["\']', target_content))
                if anchor not in target_ids:
                    errors.append(f"[{hf}] Cross-page anchor #{anchor} not found in {target_path}")

        # 4. Check meta image assets (og:image, twitter:image, icon)
        meta_images = re.findall(r'<meta[^>]+(?:property|name)=["\'](?:og:image|twitter:image)["\'][^>]+content=["\']([^"\']+)["\']', active_content)
        meta_images += re.findall(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\'](?:og:image|twitter:image)["\']', active_content)
        icon_links = re.findall(r'<link[^>]+rel=["\']icon["\'][^>]+href=["\']([^"\']+)["\']', active_content)
        
        for m_asset in meta_images + icon_links:
            if m_asset.startswith(('http://', 'https://', 'data:')):
                continue
            checked_meta_assets += 1
            if not os.path.exists(m_asset):
                errors.append(f"[{hf}] Missing meta asset referenced: {m_asset}")

        # 5. Heading hierarchy check
        headings = re.findall(r'<h([1-6])[\s>]', active_content, flags=re.IGNORECASE)
        h_levels = [int(h) for h in headings]
        checked_headings += len(h_levels)
        if h_levels.count(1) != 1:
            errors.append(f"[{hf}] Document must have exactly one <h1>, found {h_levels.count(1)}")
        for i in range(len(h_levels) - 1):
            curr, nxt = h_levels[i], h_levels[i+1]
            if nxt > curr + 1:
                errors.append(f"[{hf}] Heading level skipped: <h{curr}> followed by <h{nxt}>")

        # 6. Image alt attribute check
        img_tags = re.findall(r'<img([^>]+)>', active_content, flags=re.IGNORECASE)
        for tag in img_tags:
            checked_images_alt += 1
            if not re.search(r'alt=["\']', tag):
                errors.append(f"[{hf}] Image missing alt attribute: <img{tag}>")

        # 7. External link security check (target="_blank" -> rel="noopener")
        blank_links = re.findall(r'<a[^>]+target=["\']_blank["\'][^>]*>', active_content, flags=re.IGNORECASE)
        for bl in blank_links:
            if not re.search(r'rel=["\'][^"\']*noopener', bl):
                errors.append(f"[{hf}] External blank link missing rel='noopener': {bl}")

    print(f"Verified:")
    print(f"  • {checked_srcs} active local src assets")
    print(f"  • {checked_hrefs} active local href links & targets")
    print(f"  • {checked_meta_assets} meta/social preview assets & favicons")
    print(f"  • {checked_headings} headings checked for hierarchy (h1-h6)")
    print(f"  • {checked_images_alt} image tags checked for accessibility alt text")
    
    if errors:
        print(f"\nFAILED with {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        exit(1)
    else:
        print("\nALL QUALITY, ACCESSIBILITY, LINK, AND ASSET TESTS PASSED!")

if __name__ == '__main__':
    test_links_and_assets()
