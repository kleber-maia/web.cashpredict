#!/usr/bin/env python3
"""Check the production site; optionally include local design review pages."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib,json,struct,re,sys
import xml.etree.ElementTree as ET
from urllib.robotparser import RobotFileParser

ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self,path):
        super().__init__(convert_charrefs=True)
        self.path,self.ids,self.refs,self.images=path,set(),[],[]
        self.schemas,self.script,self.h1_count=[],None,0
        self.metadata,self.canonicals={},[]
        self.text,self.devices,self.divs=[],[],[]
        self.feed(path.read_text())
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='meta':
            key=attrs.get('property') or attrs.get('name')
            if key and (key.startswith('og:') or key.startswith('twitter:')):
                assert key not in self.metadata,f'Duplicate social tag: {key}'
                self.metadata[key]=attrs.get('content','')
        if tag=='link' and attrs.get('rel')=='canonical':self.canonicals.append(attrs.get('href'))
        if 'id' in attrs:
            assert attrs['id'] not in self.ids,f'Duplicate id: {self.path} {attrs["id"]}'
            self.ids.add(attrs['id'])
        self.h1_count+=tag=='h1'
        for key in ['src','href','aria-controls']:
            if attrs.get(key):self.refs.append((key,attrs[key]))
        if attrs.get('srcset'):
            self.refs.extend(('srcset',item.strip().split()[0]) for item in attrs['srcset'].split(','))
        if tag=='div':
            device={'attrs':attrs,'images':[]} if attrs.get('data-capture') else None
            if device:self.devices.append(device)
            self.divs.append(device)
        if tag=='img':
            assert attrs.get('alt') or attrs.get('aria-hidden')=='true',f'Missing alternative: {attrs}'
            self.images.append(attrs)
            for device in reversed(self.divs):
                if device is not None:device['images'].append(attrs);break
        if tag=='script' and attrs.get('type')=='application/ld+json':self.script=''
        elif tag=='script':assert not urlsplit(attrs.get('src','')).netloc,'External script runtime'
    def handle_data(self,data):
        self.text.append(data)
        if self.script is not None:self.script+=data
    def handle_endtag(self,tag):
        if tag=='div':self.divs.pop()
        if tag=='script' and self.script is not None:
            self.schemas.append(json.loads(self.script));self.script=None

main_path=ROOT/'index.html'
paths=[main_path,ROOT/'scripts/social-card.html']
if '--include-previews' in sys.argv:
    paths += [ROOT/'previews/system/index.html',ROOT/'previews/system/light.html',ROOT/'previews/system/dark.html',*[ROOT/f'previews/{d}/index.html' for d in ['dark','light','editorial']]]
pages={p:Page(p) for p in paths}
for path,page in pages.items():
    assert page.h1_count==1,f'One main heading required: {path}'
    for key,ref in page.refs:
        if key=='aria-controls':assert ref in page.ids;continue
        parts=urlsplit(ref)
        if parts.scheme or parts.netloc:continue
        target=(ROOT/parts.path.lstrip('/') if parts.path.startswith('/') else path.parent/unquote(parts.path)).resolve() if parts.path else path
        assert target.is_relative_to(ROOT),f'Escaping reference: {ref}'
        if target.is_dir():target=target/'index.html'
        assert target.is_file(),f'Missing reference: {path} {ref}'
        if parts.fragment:
            other=pages.get(target) or Page(target)
            assert unquote(parts.fragment) in other.ids,f'Missing anchor: {ref}'

captures=json.loads((ROOT/'img/current/provenance.json').read_text())
entries={entry['file']:entry for entry in captures['images']}
assert len(entries)==7
for source,entry in entries.items():
    data=(ROOT/source).read_bytes()
    assert data[:8]==b'\x89PNG\r\n\x1a\n'
    assert struct.unpack('>II',data[16:24])==(entry['width'],entry['height'])
    assert hashlib.sha256(data).hexdigest()==entry['sha256'],f'Original capture changed: {source}'

art=json.loads((ROOT/'img/apple/provenance.json').read_text())
assert art['approval_quote']=='Yes, accept the Apple resource license'
assets={entry['model']:entry for entry in art['assets']}
for entry in assets.values():
    data=(ROOT/'img/apple'/entry['file']).read_bytes()
    assert hashlib.sha256(data).hexdigest()==entry['sha256'],'Apple artwork changed'
    assert struct.unpack('>II',data[16:24])==tuple(entry['canvas'])
    assert entry['url'].startswith('https://devimages-cdn.apple.com/')
assert (ROOT/'img/apple/Apple-Design-Resources-License.txt').is_file()

page=pages[main_path];html=main_path.read_text();text=' '.join(' '.join(page.text).split())
assert len(page.devices)==7,'Every capture needs its own complete device frame'
seen=set()
for device in page.devices:
    assert 'has-frame' in device['attrs']['class']
    screen=[i for i in device['images'] if i.get('class')=='app-screen']
    bezel=[i for i in device['images'] if i.get('class')=='device-bezel']
    assert len(screen)==len(bezel)==1,'One native screen and one Apple frame per figure'
    screen,bezel=screen[0],bezel[0]
    source=unquote(urlsplit(screen['src']).path);assert source in entries
    assert source not in seen;seen.add(source)
    entry=entries[source]
    assert (int(screen['width']),int(screen['height']))==(entry['width'],entry['height'])
    ipad=source.endswith('/ipad.png');frame=assets['iPad (A16)' if ipad else 'iPhone 18 Pro']
    assert urlsplit(bezel['src']).path=='img/apple/'+frame['file']
    assert (int(bezel['width']),int(bezel['height']))==tuple(frame['canvas'])
    expected=(entry['height'],entry['width']) if ipad else (entry['width'],entry['height'])
    assert tuple(frame['screen'][2:])==expected,'Native screen proportions must match the Apple opening'
assert seen==set(entries)
assert 'Micromanaging expenses is ancient thinking.' in text
assert 'Cash Predict is all about your present and future.' in text
assert len(page.schemas)==1 and page.schemas[0]['@type']=='MobileApplication'
assert 'aggregateRating' not in page.schemas[0]
assert not any(claim in html for claim in ["we don't transmit your data anywhere",'watchOS','top-rated','Compare designs','editorial'])
for dest in ['https://apps.apple.com/app/apple-store/id6444193844?pt=119005924&ct=website&mt=8','https://medium.com/@cashpredict','mailto:support@cashpredict.app']:
    assert dest in [ref for _,ref in page.refs]
css=(ROOT/'assets/css/custom.css').read_text()
assert '@media(prefers-color-scheme:dark)' in css
assert 'color-scheme:light dark' in css
assert not any(effect in css for effect in ['object-fit:cover','box-shadow:','clip-path:','filter:'])
# Motion belongs only to the decorative line and copy reveal, never Apple artwork.
for selectors, declarations in re.findall(r'([^{}]+)\{([^{}]*)\}', css):
    if any(effect in declarations for effect in ['animation:', 'transform:']):
        assert all(selector.strip() in ['.flow-line::after', '.flow-line:nth-of-type(4)::after', '.reveal-in', 'from', 'to', '*', '*::before', '*::after'] for selector in selectors.split(',')), f'Unexpected motion target: {selectors}'
js=(ROOT/'assets/js/site.js').read_text()
assert "'.hero-copy, .section-copy, .manifesto h2, .section-heading, .principles article, .price-card'" in js
assert 'prefers-reduced-motion: reduce' in js
assert 'prefers-reduced-motion:reduce' in css
assert 'max-width:none' in css and 'height:auto' in css
assert page.canonicals==['https://cashpredict.app/'],'One HTTPS canonical required'
meta=page.metadata
assert meta['og:url']==page.canonicals[0]
assert meta['og:type']=='website' and meta['og:site_name']=='Cash Predict'
assert meta['twitter:card']=='summary_large_image'
image_url='https://cashpredict.app/img/social/cash-predict-v1.jpg'
assert meta['og:image']==meta['twitter:image']==image_url
assert meta['og:image:type']=='image/jpeg'
assert (meta['og:image:width'],meta['og:image:height'])==('1200','630')
assert meta['og:image:alt']==meta['twitter:image:alt'] and len(meta['og:image:alt'])>30
for field in ['title','description']:assert meta['og:'+field]==meta['twitter:'+field]
image=(ROOT/urlsplit(image_url).path.lstrip('/')).read_bytes()
assert image.startswith(b'\xff\xd8') and len(image)<5*1024*1024,'JPEG social card under 5 MB'
assert (ROOT/'CNAME').read_text().strip()=='cashpredict.app'
print('PASS: selected system-appearance site; seven full native captures with matching original Apple frames; original hashes, aspect ratios, links, anchors, schema, message, license, unique social metadata, JPEG share artwork and Pages CNAME.')

# Discoverability is crawl access and useful facts, not a ranking guarantee.
assert '<title>Cash Predict | Cash Flow Forecast App for iPhone &amp; iPad</title>' in html or '<title>Cash Predict | Cash Flow Forecast App for iPhone & iPad</title>' in html
assert '$20' in text and 'year' in text
assert page.schemas[0]['offers'][0]['price']=='0'
assert page.schemas[0]['offers'][1]['price']=='20'
assert page.schemas[0]['offers'][1]['priceCurrency']=='USD'
assert page.schemas[0]['offers'][1]['priceSpecification']['unitText']=='year'
assert 'analytics may include aggregate cash, savings, credit and debt balances' in text
assert 'does not move money at your bank' in text
sitemap=ET.fromstring((ROOT/'sitemap.xml').read_text())
assert [el.text for el in sitemap.findall('{*}url/{*}loc')]==['https://cashpredict.app/']
robots=RobotFileParser();robots.parse((ROOT/'robots.txt').read_text().splitlines())
for bot in ['Googlebot','Bingbot','OAI-SearchBot']:
    assert robots.can_fetch(bot,'https://cashpredict.app/')
    assert robots.can_fetch(bot,'https://cashpredict.app/assets/css/custom.css')
    assert not robots.can_fetch(bot,'https://cashpredict.app/private/')
assert not robots.can_fetch('GPTBot','https://cashpredict.app/')
assert robots.site_maps()==['https://cashpredict.app/sitemap.xml']
print('PASS: search/ChatGPT crawl policy, sitemap, descriptive metadata, free and annual pricing, analytics disclosure, reduced-motion and artwork motion boundaries.')
