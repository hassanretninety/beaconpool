"""Draws src/art/rickshaw.svg: a painted Lahore rickshaw with a roof garden.

The SVG carries its own CSS animations (wheels turning, body idling, flowers and
fringe swaying in the breeze, painted panels glowing). They run when the SVG is
inline or in an <img>, and freeze to a still frame when drawn onto the map canvas.
"""
import math, pathlib
NAVY, GOLD, RED, PINK, TEAL, GREEN, LIME, CREAM, INK = '#061D7B', '#FFC72C', '#E4002B', '#E6007E', '#14A3A8', '#13915A', '#9BD14B', '#FFF8EC', '#1E2433'

def g(t, inner, cls='', style=''):
    c = f' class="{cls}"' if cls else ''
    st = f' style="{style}"' if style else ''
    return f'<g transform="{t}"{c}{st}>{inner}</g>' if t else f'<g{c}{st}>{inner}</g>'

def flower(cx, cy, s, petal=PINK, inner=GOLD, core=RED, n=8, rot=0, sw=1.4):
    o = ''
    for i in range(n):
        a = rot + i * 360 / n
        o += f'<path transform="translate({cx:.1f} {cy:.1f}) rotate({a:.1f}) scale({s:.3f})" d="M0 -4C7 -8 9 -20 0 -27C-9 -20 -7 -8 0 -4Z" fill="{petal}" stroke="{NAVY}" stroke-width="{sw}"/>'
    for i in range(n):
        a = rot + i * 360 / n + 180 / n
        o += f'<path transform="translate({cx:.1f} {cy:.1f}) rotate({a:.1f}) scale({s:.3f})" d="M0 -3C4 -6 5 -12 0 -16C-5 -12 -4 -6 0 -3Z" fill="{inner}" stroke="{NAVY}" stroke-width="{sw*.8}"/>'
    o += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{7*s:.1f}" fill="{core}" stroke="{NAVY}" stroke-width="{sw}"/><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{3*s:.1f}" fill="{GOLD}"/>'
    return o

def leaf(x, y, a, s, fill=GREEN, vein=LIME):
    return f'<g transform="translate({x:.1f} {y:.1f}) rotate({a:.1f}) scale({s:.3f})"><path d="M0 0C8 -11 24 -11 34 0C24 11 8 11 0 0Z" fill="{fill}" stroke="{NAVY}" stroke-width="1.4"/><path d="M3 0L28 0" stroke="{vein}" stroke-width="1.3" stroke-linecap="round"/></g>'

def wheel(cx, cy, r, dur):
    spokes = ''.join(f'<path d="M0 0L{r*.56*math.cos(math.radians(i*45)):.1f} {r*.56*math.sin(math.radians(i*45)):.1f}" stroke="{RED}" stroke-width="2.2" stroke-linecap="round"/>' for i in range(8))
    dots = ''.join(f'<circle cx="{r*.74*math.cos(math.radians(i*30)):.1f}" cy="{r*.74*math.sin(math.radians(i*30)):.1f}" r="1.6" fill="#fff" opacity=".8"/>' for i in range(12))
    inner = (f'<circle r="{r}" fill="{INK}"/><circle r="{r*.82}" fill="none" stroke="#3A4256" stroke-width="2" stroke-dasharray="3 5"/>'
             f'<circle r="{r*.6}" fill="url(#rk-rim)" stroke="{NAVY}" stroke-width="2"/>{spokes}{dots}<circle r="{r*.18}" fill="{PINK}" stroke="{NAVY}" stroke-width="1.6"/>')
    return f'<g transform="translate({cx} {cy})"><g class="rk-spin" style="animation-duration:{dur}s">{inner}</g></g>'

STYLE = """
.rk-body{animation:rk-bob .46s ease-in-out infinite alternate}
@keyframes rk-bob{from{transform:translateY(0)}to{transform:translateY(-2.4px)}}
.rk-spin{animation:rk-spin .8s linear infinite}
@keyframes rk-spin{to{transform:rotate(-360deg)}}
.rk-sway{animation:rk-sway 2.4s ease-in-out infinite alternate;transform-box:fill-box;transform-origin:50% 100%}
@keyframes rk-sway{from{transform:rotate(-7deg)}to{transform:rotate(8deg)}}
.rk-tassel{animation:rk-tassel 1s ease-in-out infinite alternate;transform-box:fill-box;transform-origin:50% 0}
@keyframes rk-tassel{from{transform:rotate(-12deg)}to{transform:rotate(10deg)}}
.rk-glow{animation:rk-glow 1.7s ease-in-out infinite alternate}
@keyframes rk-glow{from{opacity:.3}to{opacity:.95}}
.rk-glint{animation:rk-glint 2.2s ease-in-out infinite}
@keyframes rk-glint{0%,100%{opacity:.4}50%{opacity:1}}
.rk-leaf{opacity:0;animation:rk-leaf 2.6s ease-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes rk-leaf{0%{opacity:0;transform:translate(0,0) rotate(0)}15%{opacity:1}100%{opacity:0;transform:translate(50px,-42px) rotate(220deg)}}
.rk-shadow{animation:rk-shadow .46s ease-in-out infinite alternate;transform-box:fill-box;transform-origin:center}
@keyframes rk-shadow{to{transform:scaleX(.95);opacity:.13}}
.rk-flap{animation:rk-flap .6s ease-in-out infinite alternate;transform-box:fill-box;transform-origin:50% 0}
@keyframes rk-flap{from{transform:rotate(-4deg)}to{transform:rotate(6deg)}}
@media (prefers-reduced-motion:reduce){.rk-body,.rk-spin,.rk-sway,.rk-tassel,.rk-glow,.rk-glint,.rk-leaf,.rk-shadow,.rk-flap{animation:none}.rk-leaf{opacity:.8}}
"""

defs = f'''<defs>
<linearGradient id="rk-gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE07A"/><stop offset=".55" stop-color="{GOLD}"/><stop offset="1" stop-color="#F2A900"/></linearGradient>
<linearGradient id="rk-green" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2DBA74"/><stop offset="1" stop-color="#0D7A48"/></linearGradient>
<linearGradient id="rk-roof" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3B63F0"/><stop offset=".6" stop-color="#1B3CC4"/><stop offset="1" stop-color="#10289A"/></linearGradient>
<linearGradient id="rk-chrome" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".5" stop-color="#C9D3E6"/><stop offset="1" stop-color="#8C98B3"/></linearGradient>
<radialGradient id="rk-rim"><stop offset="0" stop-color="#FFE07A"/><stop offset="1" stop-color="{GOLD}"/></radialGradient>
<radialGradient id="rk-halo"><stop offset="0" stop-color="#FFE9A0" stop-opacity=".95"/><stop offset=".45" stop-color="{GOLD}" stop-opacity=".45"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
<radialGradient id="rk-panelglow" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="#FFF6C9"/><stop offset="1" stop-color="#FFF6C9" stop-opacity="0"/></radialGradient>
<pattern id="rk-stripe" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(40)"><rect width="16" height="16" fill="{RED}"/><rect width="4" height="16" fill="{GOLD}"/><rect x="8" width="4" height="16" fill="{GREEN}"/><rect x="12" width="2" height="16" fill="#fff"/></pattern>
</defs>'''

o = []
o.append(f'<ellipse class="rk-shadow" cx="180" cy="238" rx="150" ry="9" fill="#000" opacity=".18"/>')
# leaves puffing out of the back instead of exhaust smoke
for i, (x, y, c) in enumerate([(318, 196, LIME), (322, 188, GREEN), (316, 202, '#7FD6D9')]):
    o.append(g('', leaf(x, y, -30, .36, c), 'rk-leaf', f'animation-delay:{i*.85:.2f}s'))
body = []
# mudflap
body.append(g('', f'<path d="M300 198h16v30q-8 5-16 0z" fill="{RED}" stroke="{NAVY}" stroke-width="2.5"/>' + flower(308, 212, .22, '#fff', GOLD, PINK, 6), 'rk-flap'))
# rear cabin
body.append(f'<path d="M140 104H298Q314 104 314 120V198H140Z" fill="url(#rk-gold)" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>')
body.append(f'<path d="M296 108h12v88h-12z" fill="url(#rk-stripe)" opacity=".9"/>')
body.append(f'<path d="M140 170H314V198H140Z" fill="url(#rk-green)" stroke="{NAVY}" stroke-width="3"/>')
body.append(f'<path d="M140 167H314" stroke="{RED}" stroke-width="4"/><path d="M146 184H308" stroke="{GOLD}" stroke-width="2.4" stroke-dasharray="7 6"/>')
# chamak patti: reflective studs along the skirt
for i, x in enumerate(range(152, 306, 14)):
    col = [PINK, '#fff', TEAL, GOLD][i % 4]
    body.append(f'<path class="rk-glint" style="animation-delay:{(i*0.18)%2.2:.2f}s" d="M{x} 192l4 -4 4 4 -4 4z" fill="{col}" stroke="{NAVY}" stroke-width="1"/>')
# painted side panel with a soft glow behind the flowers
panel = (f'<rect x="174" y="112" width="118" height="48" rx="10" fill="{CREAM}" stroke="{NAVY}" stroke-width="2.6"/>'
         f'<rect class="rk-glow" x="176" y="114" width="114" height="44" rx="9" fill="url(#rk-panelglow)"/>'
         f'<rect x="179" y="117" width="108" height="38" rx="7" fill="none" stroke="{PINK}" stroke-width="1.4" stroke-dasharray="1 4" stroke-linecap="round"/>')
panel += leaf(208, 136, 195, .5, GREEN) + leaf(258, 136, -15, .5, GREEN) + leaf(214, 128, 220, .34, LIME) + leaf(252, 128, -40, .34, LIME)
panel += flower(233, 136, .62, PINK, GOLD, RED)
panel += flower(194, 136, .4, TEAL, '#fff', GOLD, 6, 30)
# a little painted parrot on the panel
panel += f'<g transform="translate(284 134) scale(.72)"><path d="M0 0C-6 -9 -18 -8 -20 2C-21 10 -12 16 -2 12L8 22L6 10C8 6 4 2 0 0Z" fill="{GREEN}" stroke="{NAVY}" stroke-width="1.6"/><path d="M-20 0L-26 3L-20 5Z" fill="{RED}"/><circle cx="-14" cy="-1" r="1.6" fill="{NAVY}"/></g>'
body.append(panel)
# passenger doorway with a red cushion and a hanging tassel
body.append(f'<path d="M144 108H170V164H144Z" fill="{INK}" stroke="{NAVY}" stroke-width="2.5"/><path d="M146 148H168V162H146Z" fill="{RED}" opacity=".85"/>')
body.append(g('', f'<path d="M157 108V122" stroke="{GOLD}" stroke-width="1.6"/><circle cx="157" cy="125" r="3.2" fill="{PINK}" stroke="{NAVY}" stroke-width="1"/><path d="M155 128h4l1 7h-6z" fill="{GOLD}"/>', 'rk-tassel'))
# front cowl
body.append(f'<path d="M146 198H74Q46 196 48 172L60 126Q66 106 88 106H146Z" fill="url(#rk-green)" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>')
body.append(f'<path d="M58 152H146" stroke="{GOLD}" stroke-width="5"/><path d="M54 164H146" stroke="{RED}" stroke-width="3"/><path d="M62 140H146" stroke="#fff" stroke-width="1.6" stroke-dasharray="2 5" stroke-linecap="round"/>')
body.append(flower(104, 128, .42, GOLD, RED, PINK, 10) + leaf(118, 128, -10, .36, LIME) + leaf(90, 128, 190, .36, LIME))
for i, x in enumerate(range(70, 146, 12)):
    body.append(f'<circle class="rk-glint" style="animation-delay:{(i*0.25)%2.2:.2f}s" cx="{x}" cy="176" r="2.6" fill="{[PINK, "#fff", TEAL][i % 3]}" stroke="{NAVY}" stroke-width=".8"/>')
# windscreen frame, mirror, handlebar
# headlight with a warm pulsing halo
body.append(f'<circle class="rk-glow" cx="50" cy="146" r="26" fill="url(#rk-halo)"/><circle cx="52" cy="146" r="10.5" fill="{GOLD}" stroke="{NAVY}" stroke-width="2.6"/><circle cx="50" cy="144" r="4" fill="#fff"/>')
body.append(f'<rect x="40" y="186" width="34" height="9" rx="4.5" fill="url(#rk-chrome)" stroke="{NAVY}" stroke-width="2"/>')
# canopy with a truck-art stripe band
body.append(f'<path d="M72 106Q76 54 132 50H300Q324 50 326 76L328 106Z" fill="url(#rk-roof)" stroke="{NAVY}" stroke-width="5" stroke-linejoin="round"/>')
body.append(f'<path d="M75 104Q79 57 132 53H300Q321 53 323 76L325 104" fill="none" stroke="{GOLD}" stroke-width="1.8" stroke-linejoin="round" opacity=".9"/>')
body.append(f'<path d="M86 66Q96 60 132 60H300" stroke="{GOLD}" stroke-width="2.6" fill="none"/>')
body.append(f'<path d="M74 92H328V106H72Z" fill="url(#rk-stripe)" stroke="{NAVY}" stroke-width="2"/>')
for i, x in enumerate(range(112, 316, 22)):
    body.append(f'<circle class="rk-glint" style="animation-delay:{(i*0.3)%2.2:.2f}s" cx="{x}" cy="76" r="3" fill="{[GOLD, PINK, "#fff", TEAL][i % 4]}"/>')
body.append(f'<path d="M84 78L70 54" stroke="#8C98B3" stroke-width="3" stroke-linecap="round"/><ellipse cx="68" cy="49" rx="8" ry="6" fill="url(#rk-chrome)" stroke="{PINK}" stroke-width="2.4"/>')
body.append(f'<path d="M92 72Q100 66 112 64" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".5"/>')
# jhalar: the swinging fringe under the canopy
for i, x in enumerate(range(80, 326, 11)):
    col = [RED, GOLD, TEAL, PINK, '#fff'][i % 5]
    body.append(g('', f'<path d="M{x} 106h7l-3.5 10z" fill="{col}" stroke="{NAVY}" stroke-width=".8"/><circle cx="{x+3.5}" cy="118" r="1.8" fill="{col}"/>', 'rk-tassel', f'animation-delay:{-(i*0.13)%1:.2f}s'))
# roof garden: planter and flowers swaying in the breeze
body.append(f'<rect x="118" y="36" width="184" height="16" rx="5" fill="#8B5A2B" stroke="{NAVY}" stroke-width="2.6"/>')
for i, x in enumerate(range(128, 296, 16)):
    body.append(f'<circle cx="{x}" cy="44" r="2" fill="{[GOLD, PINK, TEAL][i % 3]}"/>')
plants = [
    (134, 38, 'leaf', LIME, 0), (152, 38, 'flower', (TEAL, '#fff', GOLD, 6), 26), (172, 38, 'leaf', GREEN, 0),
    (192, 38, 'flower', (PINK, GOLD, RED, 8), 34), (214, 38, 'leaf', LIME, 0), (234, 38, 'flower', (GOLD, RED, PINK, 10), 28),
    (256, 38, 'leaf', GREEN, 0), (276, 38, 'flower', (TEAL, '#fff', GOLD, 6), 22), (292, 38, 'leaf', LIME, 0)]
for i, (x, y, kind, c, h) in enumerate(plants):
    if kind == 'leaf':
        inner = leaf(x, y, -112, .62, c) + leaf(x, y, -68, .55, GREEN if c == LIME else LIME)
    else:
        p, q, r, n = c
        inner = f'<path d="M{x} {y}V{y-h}" stroke="#0F6B3A" stroke-width="2.6" stroke-linecap="round"/>' + leaf(x, y - h * .45, -150, .4, GREEN) + leaf(x, y - h * .6, -30, .36, LIME) + flower(x, y - h, .5, p, q, r, n)
    body.append(g('', inner, 'rk-sway', f'animation-delay:{-i*0.37:.2f}s;animation-duration:{2.1 + (i % 3) * .45:.2f}s'))
o.append(g('', ''.join(body), 'rk-body'))
o.append(wheel(80, 208, 24, .62))
o.append(wheel(262, 204, 30, .78))
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="360" height="250" viewBox="0 0 360 250"><style>{STYLE}</style>{defs}' + ''.join(o) + '</svg>')
out = pathlib.Path(__file__).resolve().parent.parent / 'src' / 'art' / 'rickshaw.svg'
out.write_text(svg)
print(out.name, len(svg), 'bytes')
