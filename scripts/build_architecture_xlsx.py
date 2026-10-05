#!/usr/bin/env python3
"""Monotone system-architecture Excel template (Meiryo UI, 16-point connectors)."""

from __future__ import annotations

import json
import math
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

ROOT = Path("/workspace")
OUT_PUBLIC = ROOT / "public" / "system-architecture-template.xlsx"
OUT_ARTIFACT = ROOT / "artifacts" / "システム構成図テンプレート.xlsx"
OUT_CATALOG = ROOT / "src" / "data" / "catalog.ts"

# Square-cell target at 96dpi: row 15pt = 20px. Column width assumes Meiryo UI MDW ≈ 8.
ROW_PT = 15
ROW_EMU = ROW_PT * 12700  # 190500
COL_EMU = ROW_EMU
COL_WIDTH = round((20 * 256 / 8 - (128 // 7)) / 256, 4)  # 2.4297

PAPER = "F7F6F3"
INK = "1C1C1C"
MUTED = "5E5E5A"
GRID_MINOR = "D9D8D2"
GRID_MAJOR = "B7B6B0"
TITLE_BG = "1C1C1C"

# 墨 + 6. First three route colors are the established set; last three are added.
COLORS = [
    {
        "key": "sumi",
        "name": "墨",
        "hex": "1C1C1C",
        "role": "標準・未分類・境界",
        "group": "基調",
        "hint": "色を決めない線、枠、補足",
    },
    {
        "key": "ai",
        "name": "藍",
        "hex": "2A4668",
        "role": "イントラ・社内LAN",
        "group": "従来",
        "hint": "拠点間、VPC内の通常通信",
    },
    {
        "key": "suoh",
        "name": "蘇芳",
        "hex": "7C3A3A",
        "role": "外部・インターネット",
        "group": "従来",
        "hint": "公開側、利用者、Ingress",
    },
    {
        "key": "koke",
        "name": "苔",
        "hex": "3C5644",
        "role": "現場・オンプレ",
        "group": "従来",
        "hint": "工場、拠点、閉域の機器",
    },
    {
        "key": "kincha",
        "name": "金茶",
        "hex": "7A5A2C",
        "role": "Salesforce・SaaS",
        "group": "追加",
        "hint": "外部SaaSとの業務連携",
    },
    {
        "key": "murasaki",
        "name": "江戸紫",
        "hex": "53425F",
        "role": "運用・監視・管理",
        "group": "追加",
        "hint": "監視、ログ、運用者の経路",
    },
    {
        "key": "asagi",
        "name": "浅葱",
        "hex": "1F5C58",
        "role": "データ連携・API",
        "group": "追加",
        "hint": "API、バッチ、キュー、DB",
    },
]
COLOR_BY = {c["key"]: c for c in COLORS}

FRACS = (0.125, 0.375, 0.625, 0.875)
KAPPA = 0.5522847498


def xe(text: str) -> str:
    quote = "&" + "quot;"
    return xml_escape(text, {'"': quote})


def mix(a: str, b: str, t: float) -> str:
    def rgb(h):
        return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))

    ar, ag, ab = rgb(a)
    br, bg, bb = rgb(b)
    return "{:02X}{:02X}{:02X}".format(
        round(ar * (1 - t) + br * t),
        round(ag * (1 - t) + bg * t),
        round(ab * (1 - t) + bb * t),
    )


def glass_hex(hex_color: str) -> str:
    return mix(hex_color, "FFFFFF", 0.38)


def zone_fill(hex_color: str) -> str:
    return mix(hex_color, PAPER, 0.90)


def emu_pt(pt: float) -> int:
    return int(round(pt * 12700))


def rect_cxns():
    pts = []
    for f in FRACS:
        pts.append((int(round(21600 * f)), 0, 16200000))
    for f in FRACS:
        pts.append((21600, int(round(21600 * f)), 0))
    for f in FRACS:
        pts.append((int(round(21600 * f)), 21600, 5400000))
    for f in FRACS:
        pts.append((0, int(round(21600 * f)), 10800000))
    return pts


def ellipse_cxns():
    pts = []
    for i in range(16):
        deg = i * 22.5
        rad = math.radians(deg)
        x = int(round(10800 + 10800 * math.cos(rad)))
        y = int(round(10800 + 10800 * math.sin(rad)))
        pts.append((x, y, int(deg * 60000)))
    return pts


def cubic(x1, y1, x2, y2, x3, y3) -> str:
    return (
        "<a:cubicBezTo>"
        f'<a:pt x="{int(x1)}" y="{int(y1)}"/>'
        f'<a:pt x="{int(x2)}" y="{int(y2)}"/>'
        f'<a:pt x="{int(x3)}" y="{int(y3)}"/>'
        "</a:cubicBezTo>"
    )


def rr_path(l, t, r, b, rad) -> str:
    rad = min(rad, (r - l) // 2, (b - t) // 2)
    k = KAPPA
    cmds = [f'<a:moveTo><a:pt x="{l + rad}" y="{t}"/></a:moveTo>']
    cmds.append(f'<a:lnTo><a:pt x="{r - rad}" y="{t}"/></a:lnTo>')
    cmds.append(cubic(r - rad + k * rad, t, r, t + rad - k * rad, r, t + rad))
    cmds.append(f'<a:lnTo><a:pt x="{r}" y="{b - rad}"/></a:lnTo>')
    cmds.append(cubic(r, b - rad + k * rad, r - rad + k * rad, b, r - rad, b))
    cmds.append(f'<a:lnTo><a:pt x="{l + rad}" y="{b}"/></a:lnTo>')
    cmds.append(cubic(l + rad - k * rad, b, l, b - rad + k * rad, l, b - rad))
    cmds.append(f'<a:lnTo><a:pt x="{l}" y="{t + rad}"/></a:lnTo>')
    cmds.append(cubic(l, t + rad - k * rad, l + rad - k * rad, t, l + rad, t))
    cmds.append("<a:close/>")
    return "".join(cmds)


def ellipse_path() -> str:
    cx = cy = rx = ry = 10800
    k = KAPPA
    cmds = [f'<a:moveTo><a:pt x="{cx + rx}" y="{cy}"/></a:moveTo>']
    cmds.append(cubic(cx + rx, cy + k * ry, cx + k * rx, cy + ry, cx, cy + ry))
    cmds.append(cubic(cx - k * rx, cy + ry, cx - rx, cy + k * ry, cx - rx, cy))
    cmds.append(cubic(cx - rx, cy - k * ry, cx - k * rx, cy - ry, cx, cy - ry))
    cmds.append(cubic(cx + k * rx, cy - ry, cx + rx, cy - k * ry, cx + rx, cy))
    cmds.append("<a:close/>")
    return "".join(cmds)


def callout_path() -> str:
    """Rounded card with a tail at the lower left. Box is 0..21600."""
    l, t, r = 0, 0, 21600
    body_b = 16800
    rad = 900
    k = KAPPA
    tail_l, tail_tip_x, tail_r = 2800, 1600, 6400
    cmds = [f'<a:moveTo><a:pt x="{l + rad}" y="{t}"/></a:moveTo>']
    cmds.append(f'<a:lnTo><a:pt x="{r - rad}" y="{t}"/></a:lnTo>')
    cmds.append(cubic(r - rad + k * rad, t, r, t + rad - k * rad, r, t + rad))
    cmds.append(f'<a:lnTo><a:pt x="{r}" y="{body_b - rad}"/></a:lnTo>')
    cmds.append(cubic(r, body_b - rad + k * rad, r - rad + k * rad, body_b, r - rad, body_b))
    cmds.append(f'<a:lnTo><a:pt x="{tail_r}" y="{body_b}"/></a:lnTo>')
    cmds.append(f'<a:lnTo><a:pt x="{tail_tip_x}" y="21600"/></a:lnTo>')
    cmds.append(f'<a:lnTo><a:pt x="{tail_l}" y="{body_b}"/></a:lnTo>')
    cmds.append(f'<a:lnTo><a:pt x="{l + rad}" y="{body_b}"/></a:lnTo>')
    cmds.append(cubic(l + rad - k * rad, body_b, l, body_b - rad + k * rad, l, body_b - rad))
    cmds.append(f'<a:lnTo><a:pt x="{l}" y="{t + rad}"/></a:lnTo>')
    cmds.append(cubic(l, t + rad - k * rad, l + rad - k * rad, t, l + rad, t))
    cmds.append("<a:close/>")
    return "".join(cmds)


def callout_cxns():
    body_b = 16800
    pts = []
    for f in FRACS:
        pts.append((int(round(21600 * f)), 0, 16200000))
    for f in FRACS:
        pts.append((21600, int(round(body_b * f)), 0))
    # bottom of card, skipping the tail notch, plus the tip as the second point
    pts.append((9000, body_b, 5400000))
    pts.append((1600, 21600, 5400000))
    pts.append((14000, body_b, 5400000))
    pts.append((19000, body_b, 5400000))
    for f in FRACS:
        pts.append((0, int(round(body_b * f)), 10800000))
    return pts


def cust_geom(path_xml: str, cxns) -> str:
    cx = "".join(
        f'<a:cxn ang="{ang}"><a:pos x="{x}" y="{y}"/></a:cxn>' for x, y, ang in cxns
    )
    return (
        "<a:custGeom><a:avLst/><a:gdLst/><a:ahLst/>"
        f"<a:cxnLst>{cx}</a:cxnLst>"
        '<a:rect l="l" t="t" r="r" b="b"/>'
        f'<a:pathLst><a:path w="21600" h="21600">{path_xml}</a:path></a:pathLst>'
        "</a:custGeom>"
    )


def runs_xml(paragraphs, align="ctr", anchor="ctr", insets=None) -> str:
    l, t, r, b = insets or (90000, 40000, 70000, 36000)
    body = (
        f'<a:bodyPr wrap="square" lIns="{l}" tIns="{t}" rIns="{r}" bIns="{b}" '
        f'anchor="{anchor}" rtlCol="0"/>'
    )
    ps = []
    for p in paragraphs:
        text = p.get("t", "")
        sz = p.get("sz", 1000)
        color = p.get("c", INK)
        bold = "1" if p.get("b") else "0"
        al = p.get("al", align)
        ps.append(
            "<a:p>"
            f'<a:pPr algn="{al}"><a:lnSpc><a:spcPct val="108000"/></a:lnSpc></a:pPr>'
            "<a:r>"
            f'<a:rPr lang="ja-JP" altLang="en-US" sz="{sz}" b="{bold}" dirty="0">'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            '<a:latin typeface="Meiryo UI"/><a:ea typeface="Meiryo UI"/><a:cs typeface="Meiryo UI"/>'
            "</a:rPr>"
            f"<a:t>{xe(text)}</a:t></a:r></a:p>"
        )
    if not ps:
        ps.append(
            '<a:p><a:endParaRPr lang="ja-JP" sz="800">'
            '<a:latin typeface="Meiryo UI"/><a:ea typeface="Meiryo UI"/>'
            "</a:endParaRPr></a:p>"
        )
    return f"<xdr:txBody>{body}<a:lstStyle/>{''.join(ps)}</xdr:txBody>"


def fill_solid(hex_color: str) -> str:
    return f'<a:solidFill><a:srgbClr val="{hex_color}"/></a:solidFill>'


def fill_rail(hex_color: str, stop=7000) -> str:
    return (
        '<a:gradFill rotWithShape="1"><a:gsLst>'
        f'<a:gs pos="0"><a:srgbClr val="{hex_color}"/></a:gs>'
        f'<a:gs pos="{stop}"><a:srgbClr val="{hex_color}"/></a:gs>'
        f'<a:gs pos="{stop + 1}"><a:srgbClr val="{PAPER}"/></a:gs>'
        f'<a:gs pos="100000"><a:srgbClr val="{PAPER}"/></a:gs>'
        "</a:gsLst>"
        '<a:lin ang="0" scaled="0"/>'
        "</a:gradFill>"
    )


def fill_topbar(hex_color: str, stop=12000) -> str:
    return (
        '<a:gradFill rotWithShape="1"><a:gsLst>'
        f'<a:gs pos="0"><a:srgbClr val="{hex_color}"/></a:gs>'
        f'<a:gs pos="{stop}"><a:srgbClr val="{hex_color}"/></a:gs>'
        f'<a:gs pos="{stop + 1}"><a:srgbClr val="{PAPER}"/></a:gs>'
        f'<a:gs pos="100000"><a:srgbClr val="{PAPER}"/></a:gs>'
        "</a:gsLst>"
        '<a:lin ang="5400000" scaled="0"/>'
        "</a:gradFill>"
    )


def line_style(hex_color, pt, alpha=None, dash="solid", arrow="triangle", join="round", head="none", width_arrow="med"):
    w = emu_pt(pt)
    color = f'<a:srgbClr val="{hex_color}">'
    if alpha is not None:
        color += f'<a:alpha val="{alpha}"/>'
    color += "</a:srgbClr>"
    join_xml = "<a:round/>" if join == "round" else '<a:miter lim="800000"/>'
    return (
        f'<a:ln w="{w}" cap="rnd" cmpd="sng">'
        f"<a:solidFill>{color}</a:solidFill>"
        f'<a:prstDash val="{dash}"/>'
        f"{join_xml}"
        f'<a:headEnd type="{head}" w="{width_arrow}" len="med"/>'
        f'<a:tailEnd type="{arrow}" w="{width_arrow}" len="med"/>'
        "</a:ln>"
    )


class Drawing:
    def __init__(self):
        self.parts: list[str] = []
        self.nid = 2
        self.registry: dict[str, dict] = {}

    def add_shape(
        self,
        name,
        c1,
        r1,
        c2,
        r2,
        geom,
        fill,
        ln,
        paragraphs,
        key=None,
        anchor="ctr",
        align="ctr",
        insets=None,
        preview=None,
    ):
        sid = self.nid
        self.nid += 1
        x = c1 * COL_EMU
        y = r1 * ROW_EMU
        cx = (c2 - c1) * COL_EMU
        cy = (r2 - r1) * ROW_EMU
        if cx <= 0 or cy <= 0:
            raise ValueError(f"bad extent {name}")
        sp = (
            '<xdr:twoCellAnchor editAs="oneCell">'
            "<xdr:from>"
            f"<xdr:col>{c1}</xdr:col><xdr:colOff>0</xdr:colOff>"
            f"<xdr:row>{r1}</xdr:row><xdr:rowOff>0</xdr:rowOff>"
            "</xdr:from><xdr:to>"
            f"<xdr:col>{c2}</xdr:col><xdr:colOff>0</xdr:colOff>"
            f"<xdr:row>{r2}</xdr:row><xdr:rowOff>0</xdr:rowOff>"
            "</xdr:to><xdr:sp><xdr:nvSpPr>"
            f'<xdr:cNvPr id="{sid}" name="{xe(name)}"/>'
            "<xdr:cNvSpPr/><xdr:nvPr/></xdr:nvSpPr><xdr:spPr>"
            "<a:xfrm>"
            f'<a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/>'
            "</a:xfrm>"
            f"{geom}{fill}{ln}</xdr:spPr>"
            f"{runs_xml(paragraphs, align=align, anchor=anchor, insets=insets)}"
            "</xdr:sp><xdr:clientData/></xdr:twoCellAnchor>"
        )
        self.parts.append(sp)
        if key:
            self.registry[key] = {
                "id": sid,
                "c1": c1,
                "r1": r1,
                "c2": c2,
                "r2": r2,
                "form": preview.get("form", "rect") if preview else "rect",
            }
        return sid

    def add_connector(
        self,
        name,
        c1,
        r1,
        c2,
        r2,
        preset,
        ln,
        flip_h=0,
        flip_v=0,
        start=None,
        end=None,
    ):
        sid = self.nid
        self.nid += 1
        x = c1 * COL_EMU
        y = r1 * ROW_EMU
        cx = max((c2 - c1) * COL_EMU, 20000)
        cy = max((r2 - r1) * ROW_EMU, 20000)
        # When the anchor is expanded to a minimum, keep xfrm in sync with the anchor box.
        st = ""
        if start:
            st += f'<a:stCxn id="{start[0]}" idx="{start[1]}"/>'
        if end:
            st += f'<a:endCxn id="{end[0]}" idx="{end[1]}"/>'
        xml = (
            '<xdr:twoCellAnchor editAs="oneCell">'
            "<xdr:from>"
            f"<xdr:col>{c1}</xdr:col><xdr:colOff>0</xdr:colOff>"
            f"<xdr:row>{r1}</xdr:row><xdr:rowOff>0</xdr:rowOff>"
            "</xdr:from><xdr:to>"
            f"<xdr:col>{max(c2, c1 + 1)}</xdr:col><xdr:colOff>0</xdr:colOff>"
            f"<xdr:row>{max(r2, r1 + 1)}</xdr:row><xdr:rowOff>0</xdr:rowOff>"
            "</xdr:to><xdr:cxnSp><xdr:nvCxnSpPr>"
            f'<xdr:cNvPr id="{sid}" name="{xe(name)}"/>'
            f"<xdr:cNvCxnSpPr>{st}</xdr:cNvCxnSpPr>"
            "</xdr:nvCxnSpPr><xdr:spPr>"
            f'<a:xfrm flipH="{flip_h}" flipV="{flip_v}">'
            f'<a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/>'
            "</a:xfrm>"
            f'<a:prstGeom prst="{preset}"><a:avLst/></a:prstGeom>'
            "<a:noFill/>"
            f"{ln}</xdr:spPr></xdr:cxnSp><xdr:clientData/></xdr:twoCellAnchor>"
        )
        self.parts.append(xml)
        return sid

    def connect(self, name, key_a, idx_a, key_b, idx_b, preset, ln):
        a = self.registry[key_a]
        b = self.registry[key_b]
        pa = point_of(a, idx_a)
        pb = point_of(b, idx_b)
        box = box_of_points(pa, pb)
        flip_h = 1 if pa[0] > pb[0] else 0
        flip_v = 1 if pa[1] > pb[1] else 0
        return self.add_connector(
            name,
            box[0],
            box[1],
            box[2],
            box[3],
            preset,
            ln,
            flip_h,
            flip_v,
            start=(a["id"], idx_a),
            end=(b["id"], idx_b),
        )

    def xml(self) -> str:
        body = "".join(self.parts)
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<xdr:wsDr xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing" '
            'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            f"{body}</xdr:wsDr>"
        )


def point_of(shape, idx):
    c1, r1, c2, r2 = shape["c1"], shape["r1"], shape["c2"], shape["r2"]
    if shape["form"] == "ellipse":
        deg = idx * 22.5
        rad = math.radians(deg)
        cx = (c1 + c2) / 2
        cy = (r1 + r2) / 2
        rx = (c2 - c1) / 2
        ry = (r2 - r1) / 2
        return (cx + rx * math.cos(rad), cy + ry * math.sin(rad))
    side, frac = divmod(idx, 4)
    f = FRACS[frac]
    if side == 0:
        return (c1 + (c2 - c1) * f, r1)
    if side == 1:
        return (c2, r1 + (r2 - r1) * f)
    if side == 2:
        return (c1 + (c2 - c1) * f, r2)
    return (c1, r1 + (r2 - r1) * f)


def box_of_points(pa, pb):
    x1, x2 = sorted((pa[0], pb[0]))
    y1, y2 = sorted((pa[1], pb[1]))
    # Snap the bounding box outward onto cell edges so the anchor stays on the grid.
    c1 = int(math.floor(x1))
    r1 = int(math.floor(y1))
    c2 = int(math.ceil(x2))
    r2 = int(math.ceil(y2))
    if c2 <= c1:
        c2 = c1 + 1
    if r2 <= r1:
        r2 = r1 + 1
    return c1, r1, c2, r2


def node_geom(form):
    if form == "ellipse":
        return cust_geom(ellipse_path(), ellipse_cxns())
    if form == "callout":
        return cust_geom(callout_path(), callout_cxns())
    rad = 700 if form == "zone" else 1100
    return cust_geom(rr_path(0, 0, 21600, 21600, rad), rect_cxns())


def node_paragraphs(kicker, title, sub, route_hex, large=True):
    ps = []
    if kicker:
        ps.append({"t": kicker, "sz": 800 if large else 700, "c": route_hex, "b": True, "al": "l"})
    if title:
        ps.append({"t": title, "sz": 1100 if large else 900, "c": INK, "b": True, "al": "l"})
    if sub:
        ps.append({"t": sub, "sz": 800 if large else 700, "c": MUTED, "b": False, "al": "l"})
    return ps


class Sheet:
    def __init__(self, name, cols, rows, grid=True, tab="5C5C5C"):
        self.name = name
        self.cols = cols
        self.rows = rows
        self.grid = grid
        self.tab = tab
        self.cells: dict[tuple[int, int], tuple[str, str | None]] = {}
        self.merges: list[tuple[int, int, int, int]] = []
        self.drawing = Drawing() if grid else None
        self.col_widths: dict[int, float] | None = None
        self.row_heights: dict[int, float] = {}
        self.freeze = None
        self.fit = (1, 1)
        self.footer = name

    def put(self, r, c, style, text=None):
        self.cells[(r, c)] = (style, text)
        self.rows = max(self.rows, r + 1)
        self.cols = max(self.cols, c + 1)

    def merge(self, r1, c1, r2, c2):
        self.merges.append((r1, c1, r2, c2))

    def title(self, text):
        split = self.freeze[0] if self.freeze else 0
        if split and split < self.cols:
            self.put(0, 0, "title", "構成図")
            for c in range(1, split):
                self.put(0, c, "title", None)
            if split > 1:
                self.merge(0, 0, 0, split - 1)
            self.put(0, split, "title", text)
            for c in range(split + 1, self.cols):
                self.put(0, c, "title", None)
            if self.cols - 1 > split:
                self.merge(0, split, 0, self.cols - 1)
        else:
            self.put(0, 0, "title", text)
            for c in range(1, self.cols):
                self.put(0, c, "title", None)
            if self.cols > 1:
                self.merge(0, 0, 0, self.cols - 1)


def side_kind(index, last, major_every=5):
    if index == 0 or index % major_every == 0:
        return "major"
    return "minor"


class Styles:
    def __init__(self):
        self.fonts = []
        self.fills = []
        self.borders = []
        self.xfs = []
        self.font_id = {}
        self.fill_id = {}
        self.border_id = {}
        self.xf_id = {}
        self._defaults()

    def _defaults(self):
        self.font("base", 10, "FF1A1A1A", False)
        self.fill_raw("none", '<fill><patternFill patternType="none"/></fill>')
        self.fill_raw("gray125", '<fill><patternFill patternType="gray125"/></fill>')
        self.border("none", None, None, None, None)
        self.xf("normal", "base", "none", "none", "left", "center", False)

    def font(self, key, sz, rgb, bold=False):
        if key in self.font_id:
            return self.font_id[key]
        b = "<b/>" if bold else ""
        xml = (
            f"<font>{b}<sz val=\"{sz}\"/><color rgb=\"{rgb}\"/>"
            '<name val="Meiryo UI"/><family val="2"/><charset val="128"/></font>'
        )
        self.font_id[key] = len(self.fonts)
        self.fonts.append(xml)
        return self.font_id[key]

    def fill_raw(self, key, xml):
        self.fill_id[key] = len(self.fills)
        self.fills.append(xml)

    def fill(self, key, rgb):
        if key in self.fill_id:
            return self.fill_id[key]
        xml = (
            "<fill><patternFill patternType=\"solid\">"
            f'<fgColor rgb="{rgb}"/><bgColor indexed="64"/>'
            "</patternFill></fill>"
        )
        self.fill_id[key] = len(self.fills)
        self.fills.append(xml)
        return self.fill_id[key]

    def border(self, key, left, top, right, bottom):
        if key in self.border_id:
            return self.border_id[key]

        def edge(spec):
            if not spec:
                return "<{n}/>".format(n=spec and "" or "")  # placeholder replaced below

        def one(tag, spec):
            if not spec:
                return f"<{tag}/>"
            style, color = spec
            return f'<{tag} style="{style}"><color rgb="{color}"/></{tag}>'

        xml = f"<border>{one('left', left)}{one('right', right)}{one('top', top)}{one('bottom', bottom)}<diagonal/></border>"
        self.border_id[key] = len(self.borders)
        self.borders.append(xml)
        return self.border_id[key]

    def xf(self, key, font, fill, border, h, v, wrap, hz=None):
        if key in self.xf_id:
            return self.xf_id[key]
        xml = (
            f'<xf numFmtId="0" fontId="{self.font_id[font]}" fillId="{self.fill_id[fill]}" '
            f'borderId="{self.border_id[border]}" xfId="0" applyFont="1" applyFill="1" '
            f'applyBorder="1" applyAlignment="1">'
            f'<alignment horizontal="{hz or h}" vertical="{v}" wrapText="{"1" if wrap else "0"}"/>'
            "</xf>"
        )
        self.xf_id[key] = len(self.xfs)
        self.xfs.append(xml)
        return self.xf_id[key]

    def xml(self) -> str:
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            f'<fonts count="{len(self.fonts)}">{"".join(self.fonts)}</fonts>'
            f'<fills count="{len(self.fills)}">{"".join(self.fills)}</fills>'
            f'<borders count="{len(self.borders)}">{"".join(self.borders)}</borders>'
            '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
            f'<cellXfs count="{len(self.xfs)}">{"".join(self.xfs)}</cellXfs>'
            '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
            '<dxfs count="0"/>'
            '<tableStyles count="0" defaultTableStyle="TableStyleMedium2" defaultPivotStyle="PivotStyleLight16"/>'
            "</styleSheet>"
        )


def prepare_styles() -> Styles:
    s = Styles()
    s.font("title", 10, "FFFFFFFF", True)
    s.font("section", 10, "FF1A1A1A", True)
    s.font("body", 9, "FF1C1C1C", False)
    s.font("small", 8, "FF5E5E5A", False)
    s.font("white", 9, "FFFFFFFF", True)
    s.font("inkb", 10, "FF1A1A1A", True)
    s.fill("ink", "FF1C1C1C")
    s.fill("paper", "FFF7F6F3")
    s.fill("section", "FFE8E7E2")
    s.fill("white", "FFFBFBFA")
    for c in COLORS:
        s.fill("c_" + c["key"], "FF" + c["hex"])
        s.font("on_" + c["key"], 9, "FFFFFFFF", True)
    minor = ("hair", "FF" + GRID_MINOR)
    major = ("thin", "FF" + GRID_MAJOR)
    kinds = {"none": None, "minor": minor, "major": major}
    for l in ("none", "minor", "major"):
        for t in ("none", "minor", "major"):
            for r in ("none", "minor", "major"):
                for b in ("none", "minor", "major"):
                    s.border(f"g_{l}_{t}_{r}_{b}", kinds[l], kinds[t], kinds[r], kinds[b])
                    s.xf(
                        f"g_{l}_{t}_{r}_{b}",
                        "small",
                        "none",
                        f"g_{l}_{t}_{r}_{b}",
                        "center",
                        "center",
                        False,
                    )
    s.xf("title", "title", "ink", "none", "left", "center", False)
    s.xf("section", "section", "section", "none", "left", "center", False)
    s.xf("body", "body", "none", "none", "left", "center", True)
    s.xf("small", "small", "none", "none", "left", "center", True)
    s.xf("label", "inkb", "none", "none", "left", "center", False)
    s.xf("hint", "small", "paper", "none", "left", "center", True)
    for c in COLORS:
        s.xf("sw_" + c["key"], "on_" + c["key"], "c_" + c["key"], "none", "center", "center", False)
    return s


def grid_style_key(r, c, rows, cols):
    if r == 0:
        return "title"

    def edge(i, last):
        if i == 0 or i % 5 == 0:
            return "major"
        if i == last:
            return "major"
        return "minor"

    # Draw every edge once: left+top, plus the outer right/bottom.
    left = edge(c, cols)
    top = edge(r, rows)
    right = "major" if c == cols - 1 else "none"
    bottom = "major" if r == rows - 1 else "none"
    return f"g_{left}_{top}_{right}_{bottom}"


def col_letter(n: int) -> str:
    s = ""
    n += 1
    while n:
        n, rem = divmod(n - 1, 26)
        s = chr(65 + rem) + s
    return s


def cell_ref(r, c) -> str:
    return f"{col_letter(c)}{r + 1}"


def sheet_xml(sh: Sheet, styles: Styles) -> str:
    cols = sh.cols
    rows = sh.rows
    if sh.grid and sh.col_widths is None:
        col_xml = f'<col min="1" max="{cols}" width="{COL_WIDTH}" customWidth="1"/>'
    else:
        parts = []
        if sh.col_widths:
            for idx, w in sorted(sh.col_widths.items()):
                parts.append(f'<col min="{idx + 1}" max="{idx + 1}" width="{w}" customWidth="1"/>')
            col_xml = "".join(parts)
        else:
            col_xml = f'<col min="1" max="{max(cols, 1)}" width="18" customWidth="1"/>'

    row_xml = []
    for r in range(rows):
        ht = sh.row_heights.get(r, ROW_PT if sh.grid else 18)
        cells = []
        for c in range(cols):
            if (r, c) in sh.cells:
                style, text = sh.cells[(r, c)]
            elif sh.grid:
                style, text = grid_style_key(r, c, rows, cols), None
            else:
                continue
            xf = styles.xf_id[style]
            ref = cell_ref(r, c)
            if text is None:
                cells.append(f'<c r="{ref}" s="{xf}"/>')
            else:
                cells.append(f'<c r="{ref}" s="{xf}" t="inlineStr"><is><t>{xe(text)}</t></is></c>')
        row_xml.append(
            f'<row r="{r + 1}" ht="{ht}" customHeight="1" spans="1:{cols}">{"".join(cells)}</row>'
        )

    merges = ""
    if sh.merges:
        inner = "".join(
            f'<mergeCell ref="{cell_ref(r1, c1)}:{cell_ref(r2, c2)}"/>'
            for r1, c1, r2, c2 in sh.merges
        )
        merges = f'<mergeCells count="{len(sh.merges)}">{inner}</mergeCells>'

    freeze = ""
    if sh.freeze:
        x, y = sh.freeze
        pane = f'<pane xSplit="{x}" ySplit="{y}" topLeftCell="{cell_ref(y, x)}" activePane="bottomRight" state="frozen"/>'
        freeze = pane

    drawing = '<drawing r:id="rId1"/>' if sh.drawing and sh.drawing.parts else ""
    tab = sh.tab
    fit_w, fit_h = sh.fit
    dim = f"{cell_ref(0, 0)}:{cell_ref(rows - 1, cols - 1)}"
    amp = chr(38)
    odd_header = xe(f'{amp}L{amp}"Meiryo UI"{amp}8システム構成図{amp}C{amp}A{amp}R{amp}D')
    odd_footer = xe(f'{amp}L{amp}"Meiryo UI"{amp}8{sh.footer}{amp}R{amp}P / {amp}N')
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'<sheetPr><tabColor rgb="FF{tab}"/><pageSetUpPr fitToPage="1"/></sheetPr>'
        f'<dimension ref="{dim}"/>'
        "<sheetViews>"
        f'<sheetView workbookViewId="0" showGridLines="0" zoomScale="110" zoomScaleNormal="110" view="normal">'
        f"{freeze}<selection activeCell=\"A1\" sqref=\"A1\"/>"
        "</sheetView></sheetViews>"
        f'<sheetFormatPr defaultColWidth="{COL_WIDTH}" defaultRowHeight="{ROW_PT}" customHeight="1"/>'
        f"<cols>{col_xml}</cols>"
        f"<sheetData>{''.join(row_xml)}</sheetData>"
        f"{merges}"
        '<printOptions horizontalCentered="0"/>'
        '<pageMargins left="0.4" right="0.4" top="0.55" bottom="0.45" header="0.22" footer="0.22"/>'
        f'<pageSetup paperSize="8" orientation="landscape" fitToWidth="{fit_w}" fitToHeight="{fit_h}"/>'
        "<headerFooter>"
        f"<oddHeader>{odd_header}</oddHeader>"
        f"<oddFooter>{odd_footer}</oddFooter>"
        "</headerFooter>"
        f"{drawing}"
        "</worksheet>"
    )


def ln_base(color_hex, dashed=False, both=False, pt=1.35):
    return line_style(
        color_hex,
        pt,
        dash="dash" if dashed else "solid",
        arrow="triangle",
        head="triangle" if both else "none",
        join="miter",
        width_arrow="sm",
    )


def ln_overlay(color_hex, curved=False):
    return line_style(
        glass_hex(color_hex),
        4.0,
        alpha=62000,
        dash="solid",
        arrow="triangle",
        join="round" if curved else "miter",
        width_arrow="med",
    )


def place_node(drawing: Drawing, key, name, c, r, w, h, form, color_key, kicker, title, sub, large=True, zone=False, dash=None):
    color = COLOR_BY[color_key]
    x2, y2 = c + w, r + h
    if form == "zone":
        fill = fill_solid(zone_fill(color["hex"]))
        weight = 1.5 if dash == "dash" else 1.15
        ln = line_style(color["hex"], weight, dash=dash or "solid", arrow="none", join="round")
        paras = node_paragraphs(kicker, title, sub, color["hex"], large=True)
        insets = (120000, 70000, 80000, 50000)
        anchor, align = "t", "l"
    elif form == "callout":
        fill = fill_topbar(color["hex"], 14000)
        ln = line_style(color["hex"], 1.15, arrow="none", join="round")
        paras = node_paragraphs(kicker, title, sub, color["hex"], large=large)
        insets = (110000, 150000, 80000, 360000)
        anchor, align = "ctr", "l"
    elif form == "pin":
        fill = fill_solid(color["hex"])
        ln = line_style(color["hex"], 1.0, arrow="none", join="round")
        paras = [{"t": title or "1", "sz": 1400, "c": "FFFFFF", "b": True, "al": "ctr"}]
        insets = (20000, 20000, 20000, 20000)
        anchor, align = "ctr", "ctr"
    elif form == "note":
        fill = fill_topbar(color["hex"], 16000)
        ln = line_style(color["hex"], 1.15, arrow="none", join="round")
        paras = node_paragraphs(kicker, title, sub, color["hex"], large=large)
        insets = (110000, 120000, 80000, 50000)
        anchor, align = "ctr", "l"
    elif form == "label":
        fill = fill_solid(PAPER)
        ln = line_style(color["hex"], 1.25, arrow="none", join="round")
        paras = [{"t": title, "sz": 900, "c": color["hex"], "b": True, "al": "ctr"}]
        insets = (40000, 20000, 40000, 20000)
        anchor, align = "ctr", "ctr"
    elif form == "icon":
        fill = "<a:noFill/>"
        ln = line_style(INK, 1.25, arrow="none", join="round")
        paras = [{"t": title, "sz": 800, "c": INK, "b": True, "al": "ctr"}]
        insets = (50000, 140000, 50000, 50000)
        anchor, align = "b", "ctr"
    else:
        if form == "ellipse":
            fill = fill_solid(PAPER)
        else:
            fill = fill_rail(color["hex"])
        ln = line_style(color["hex"], 1.35, arrow="none", join="round")
        paras = node_paragraphs(kicker, title, sub, color["hex"], large=large)
        insets = (150000, 50000, 70000, 40000) if form != "ellipse" else (70000, 40000, 70000, 40000)
        anchor, align = "ctr", "ctr" if form == "ellipse" else "l"
        if form == "ellipse":
            for p in paras:
                p["al"] = "ctr"
    preview_form = "ellipse" if form == "ellipse" else ("zone" if form == "zone" else form)
    drawing.add_shape(
        name,
        c,
        r,
        x2,
        y2,
        geom_for(form),
        fill,
        ln,
        paras,
        key=key,
        anchor=anchor,
        align=align,
        insets=insets,
        preview={"form": preview_form},
    )
    if key and key in drawing.registry:
        drawing.registry[key]["form"] = "ellipse" if form == "ellipse" else "rect"


def geom_for(form):
    if form == "icon":
        return cust_geom(rr_path(0, 0, 21600, 21600, 900), rect_cxns())
    return node_geom("ellipse" if form == "ellipse" else ("callout" if form == "callout" else ("zone" if form == "zone" else "node")))


def icon_geom(kind: str) -> str:
    """Monoline icon drawn in the upper portion of a 21600 box, plus a card outline."""
    outline = rr_path(300, 300, 21300, 21300, 800)
    glyph = ICON_GLYPHS[kind]()
    return cust_geom(outline + glyph, rect_cxns())


def _box(x, y, w, h):
    return (
        f'<a:moveTo><a:pt x="{x}" y="{y}"/></a:moveTo>'
        f'<a:lnTo><a:pt x="{x + w}" y="{y}"/></a:lnTo>'
        f'<a:lnTo><a:pt x="{x + w}" y="{y + h}"/></a:lnTo>'
        f'<a:lnTo><a:pt x="{x}" y="{y + h}"/></a:lnTo><a:close/>'
    )


def _line(x1, y1, x2, y2):
    return (
        f'<a:moveTo><a:pt x="{x1}" y="{y1}"/></a:moveTo>'
        f'<a:lnTo><a:pt x="{x2}" y="{y2}"/></a:lnTo>'
    )


def g_server():
    s = ""
    for i, y in enumerate((2200, 5600, 9000)):
        s += _box(6200, y, 9200, 2600)
        s += _line(7800, y + 1300, 9800, y + 1300)
    return s


def g_lambda():
    return (
        _line(7600, 11200, 10800, 2400)
        + _line(10800, 2400, 14600, 11200)
        + _line(8600, 7600, 6400, 11200)
    )


def g_bucket():
    return (
        ellipse_local(10800, 3400, 4600, 1200)
        + _line(6200, 3400, 7000, 10400)
        + _line(15400, 3400, 14600, 10400)
        + ellipse_local(10800, 10400, 3800, 1100)
    )


def g_cylinder():
    return (
        ellipse_local(10800, 3200, 4200, 1200)
        + _line(6600, 3200, 6600, 9800)
        + _line(15000, 3200, 15000, 9800)
        + ellipse_local(10800, 9800, 4200, 1200)
    )


def g_cloud():
    # Three lobes as a single stroked cloud using cubics, kept in the upper band.
    return (
        '<a:moveTo><a:pt x="5600" y="9800"/></a:moveTo>'
        + cubic(5600, 7600, 7000, 6200, 8600, 6800)
        + cubic(9000, 4600, 11200, 4200, 12400, 6200)
        + cubic(14200, 5000, 16800, 6200, 16200, 8600)
        + cubic(17600, 9000, 17000, 10800, 15000, 10400)
        + f'<a:lnTo><a:pt x="6800" y="10400"/></a:lnTo>'
        + cubic(5200, 10400, 4800, 9000, 5600, 9800)
        + "<a:close/>"
    )


def g_user():
    return ellipse_local(10800, 4200, 1800, 1800) + (
        '<a:moveTo><a:pt x="6800" y="11200"/></a:moveTo>'
        + cubic(6800, 8600, 8200, 7600, 10800, 7600)
        + cubic(13400, 7600, 14800, 8600, 14800, 11200)
    )


def g_factory():
    return (
        _line(5000, 11200, 5000, 6400)
        + _line(5000, 6400, 7600, 4200)
        + _line(7600, 4200, 10200, 6400)
        + _line(10200, 6400, 12800, 4200)
        + _line(12800, 4200, 15400, 6400)
        + _line(15400, 6400, 16600, 6400)
        + _line(16600, 6400, 16600, 11200)
        + _line(5000, 11200, 16600, 11200)
        + _box(7600, 8600, 2200, 2600)
    )


def g_fw():
    s = _box(5200, 2800, 11200, 8400)
    s += _line(5200, 5600, 16400, 5600)
    s += _line(5200, 8400, 16400, 8400)
    s += _line(8900, 2800, 8900, 5600)
    s += _line(12600, 5600, 12600, 8400)
    s += _line(8900, 8400, 8900, 11200)
    return s


def g_lb():
    s = ellipse_local(10800, 3000, 900, 900)
    s += _line(10800, 3900, 10800, 6200)
    s += _line(6200, 6200, 15400, 6200)
    for x in (6200, 10800, 15400):
        s += _line(x, 6200, x, 8600)
        s += ellipse_local(x, 9800, 800, 800)
    return s


def g_queue():
    s = ""
    for i, y in enumerate((2800, 5200, 7600)):
        s += _box(6400 + i * 200, y, 8600, 2000)
    return s


def g_eye():
    s = (
        '<a:moveTo><a:pt x="4200" y="6800"/></a:moveTo>'
        + cubic(6800, 4000, 14800, 4000, 17400, 6800)
        + cubic(14800, 9600, 6800, 9600, 4200, 6800)
        + "<a:close/>"
    )
    s += ellipse_local(10800, 6800, 1600, 1600)
    return s


def g_globe():
    s = ellipse_local(10800, 6800, 4200, 4200)
    s += ellipse_local(10800, 6800, 1800, 4200)
    s += _line(6600, 6800, 15000, 6800)
    s += _line(7200, 5000, 14400, 5000)
    s += _line(7200, 8600, 14400, 8600)
    return s


def g_vpn():
    s = ellipse_local(6200, 7000, 1600, 1600)
    s += ellipse_local(15400, 7000, 1600, 1600)
    s += _line(7800, 7000, 13800, 7000)
    s += _box(9200, 4600, 3200, 2600)
    s += (
        '<a:moveTo><a:pt x="10400" y="5800"/></a:moveTo>'
        + cubic(10400, 4600, 12400, 4600, 12400, 5800)
    )
    return s


def g_api():
    return (
        _line(8600, 3000, 6200, 6800)
        + _line(6200, 6800, 8600, 10600)
        + _line(13000, 3000, 15400, 6800)
        + _line(15400, 6800, 13000, 10600)
    )


def g_vpc():
    return g_cloud() + ellipse_local(10800, 8200, 900, 900)


def ellipse_local(cx, cy, rx, ry):
    k = KAPPA
    return (
        f'<a:moveTo><a:pt x="{cx + rx}" y="{cy}"/></a:moveTo>'
        + cubic(cx + rx, cy + k * ry, cx + k * rx, cy + ry, cx, cy + ry)
        + cubic(cx - k * rx, cy + ry, cx - rx, cy + k * ry, cx - rx, cy)
        + cubic(cx - rx, cy - k * ry, cx - k * rx, cy - ry, cx, cy - ry)
        + cubic(cx + k * rx, cy - ry, cx + rx, cy - k * ry, cx + rx, cy)
        + "<a:close/>"
    )


ICON_GLYPHS = {
    "server": g_server,
    "lambda": g_lambda,
    "bucket": g_bucket,
    "cylinder": g_cylinder,
    "cloud": g_cloud,
    "user": g_user,
    "factory": g_factory,
    "fw": g_fw,
    "lb": g_lb,
    "queue": g_queue,
    "eye": g_eye,
    "globe": g_globe,
    "vpn": g_vpn,
    "api": g_api,
    "vpc": g_vpc,
}


def place_icon(drawing: Drawing, key, name, c, r, w, h, glyph, caption):
    drawing.add_shape(
        name,
        c,
        r,
        c + w,
        r + h,
        icon_geom(glyph),
        "<a:noFill/>",
        line_style(INK, 1.2, arrow="none", join="round"),
        [{"t": caption, "sz": 800, "c": INK, "b": True, "al": "ctr"}],
        key=key,
        anchor="b",
        align="ctr",
        insets=(60000, 150000, 60000, 70000),
        preview={"form": "icon"},
    )
    if key:
        drawing.registry[key]["form"] = "rect"


# --- content -----------------------------------------------------------------

LABEL_W = 14


def add_color_headers(sh: Sheet, start_col, pitch, row=1):
    for i, c in enumerate(COLORS):
        col = start_col + i * pitch
        sh.put(row, col, "sw_" + c["key"], c["name"])
        for k in range(1, min(pitch - 1, 6)):
            sh.put(row, col + k, "sw_" + c["key"], None)
        span = min(pitch - 1, 6) - 1
        if span > 0:
            sh.merge(row, col, row, col + span)
        sh.put(row + 0, col, "sw_" + c["key"], c["name"])


def section_bar(sh: Sheet, row, text):
    split = sh.freeze[0] if sh.freeze else 0
    if split and split < sh.cols:
        sh.put(row, 0, "section", text)
        for c in range(1, split):
            sh.put(row, c, "section", None)
        if split > 1:
            sh.merge(row, 0, row, split - 1)
        for c in range(split, sh.cols):
            sh.put(row, c, "section", None)
        if sh.cols - 1 > split:
            sh.merge(row, split, row, sh.cols - 1)
    else:
        sh.put(row, 0, "section", text)
        for c in range(1, sh.cols):
            sh.put(row, c, "section", None)
        if sh.cols > 1:
            sh.merge(row, 0, row, sh.cols - 1)


def paint_color_labels(sh: Sheet, row, pitch, width):
    sh.put(row, 0, "hint", "経路色")
    for c in range(1, LABEL_W):
        sh.put(row, c, "hint", None)
    sh.merge(row, 0, row, LABEL_W - 1)
    span = max(1, min(width, 6))
    for i, color in enumerate(COLORS):
        col = LABEL_W + i * pitch
        sh.put(row, col, "sw_" + color["key"], color["name"])
        for k in range(1, span):
            sh.put(row, col + k, "sw_" + color["key"], None)
        if span > 1:
            sh.merge(row, col, row, col + span - 1)


def catalog_nodes(sh: Sheet, drawing: Drawing, sections, start_row, tile_w, tile_h, large, form_default="node"):
    """Place a matrix of color variants. Returns next row."""
    row = start_row
    pitch = tile_w + 1
    start_col = LABEL_W
    for section in sections:
        section_bar(sh, row, section["title"])
        row += 1
        sample = section["items"][0]
        width = sample.get("w", tile_w)
        if not sample.get("mono"):
            paint_color_labels(sh, row, width + 1, width)
            row += 1
        for item in section["items"]:
            w = item.get("w", tile_w)
            h = item.get("h", tile_h)
            form = item.get("form", form_default)
            pitch_i = w + 1
            sh.put(row, 0, "label", item.get("label") or item["title"])
            for c in range(1, LABEL_W):
                sh.put(row, c, "label", None)
            sh.merge(row, 0, row + h - 1, LABEL_W - 1)
            colors = COLORS if not item.get("mono") else COLORS[:1]
            for i, color in enumerate(colors):
                col = start_col + i * pitch_i
                # If this row uses a wider pitch than the header, still fine.
                key = None
                place_node(
                    drawing,
                    key,
                    f"{item['title']}_{color['name']}",
                    col,
                    row,
                    w,
                    h,
                    form,
                    color["key"],
                    item.get("kicker", ""),
                    item.get("title", ""),
                    item.get("sub", ""),
                    large=large,
                    dash=item.get("dash"),
                )
            row += h + 1
    return row


def line_library(sh: Sheet, overlay=False):
    d = sh.drawing
    variants = (
        [
            ("直線・太", "straightConnector1", False),
            ("直角", "bentConnector3", False),
            ("直角・迂回", "bentConnector5", False),
            ("曲線", "curvedConnector3", True),
            ("S字", "curvedConnector4", True),
        ]
        if overlay
        else [
            ("直線", "straightConnector1", False, False, False),
            ("直角", "bentConnector3", False, False, False),
            ("曲線", "curvedConnector3", True, False, False),
            ("直角・破線", "bentConnector3", False, True, False),
            ("双方向", "straightConnector1", False, False, True),
        ]
    )
    # header
    sh.title(
        "07  上書き線（半透明の太線。下の線を隠さず、ハンドルで直角にも曲線にもできる）"
        if overlay
        else "06  経路線（図の本線。端点を図形の接続点までドラッグしてつなぐ）"
    )
    pitch_x = 18
    start = LABEL_W
    row = 2
    for i, color in enumerate(COLORS):
        col0 = start + (i % 7) * 0
    # one band per color, variants across
    row = 2
    section_bar(sh, row, "色を選び、必要な線種をコピーする。貼り付け後、黄色い◆をドラッグして曲げる。Altで升目に吸着。")
    row += 1
    # column captions
    captions = [v[0] for v in variants]
    for i, cap in enumerate(captions):
        c = 2 + i * pitch_x
        sh.put(row, c, "label", cap)
        for k in range(1, 10):
            sh.put(row, c + k, "label", None)
        sh.merge(row, c, row, c + 9)
    row += 1
    for color in COLORS:
        sh.put(row, 0, "sw_" + color["key"], color["name"])
        for c in range(1, LABEL_W):
            sh.put(row, c, "sw_" + color["key"], None)
        sh.merge(row, 0, row + 5, LABEL_W - 1)
        for i, var in enumerate(variants):
            c = 2 + i * pitch_x
            if overlay:
                _label, preset, curved = var
                ln = ln_overlay(color["hex"], curved=curved)
            else:
                _label, preset, curved, dashed, both = var
                ln = ln_base(color["hex"], dashed=dashed, both=both, pt=1.5 if not curved else 1.5)
                if curved:
                    ln = line_style(color["hex"], 1.5, dash="solid", arrow="triangle", join="round", width_arrow="sm")
            d.add_connector(
                f"{color['name']}_{_label}",
                c,
                row + 1,
                c + 15,
                row + 5,
                preset,
                ln,
            )
        row += 7
    sh.rows = max(sh.rows, row + 1)
    sh.cols = max(sh.cols, 2 + 5 * pitch_x)


def build_howto(styles: Styles) -> Sheet:
    sh = Sheet("00_使い方", 6, 48, grid=False, tab="3A3A3A")
    sh.col_widths = {0: 4, 1: 28, 2: 22, 3: 36, 4: 18, 5: 22}
    sh.fit = (1, 1)
    sh.row_heights = {i: 18 for i in range(48)}
    sh.row_heights[0] = 28
    sh.put(0, 1, "label", "システム構成図テンプレート")
    sh.merge(0, 1, 0, 4)
    sh.row_heights[1] = 20
    sh.put(1, 1, "small", "現場・社内・AWS・外部SaaSを、概要と詳細に分けて描く。フォントは Meiryo UI。基調は墨、経路だけ7色。")
    sh.merge(1, 1, 1, 4)

    steps = [
        "描くシートを選ぶ。全体は「02_概要図」、サブネットやサービス単位は「03_詳細図」。",
        "「04_部品_概要」または「05_部品_詳細」から図形をコピーし、キャンバスへ貼り付ける。",
        "移動とサイズ変更は Alt を押しながら。セルの枠（方眼）に吸着する。",
        "「06_線_経路」から線をコピーする。端点を図形へドラッグし、青く光った接続点で離す。",
        "四角の接続点は各辺4つ、計16。円は外周を16等分。角に集中しないので線が重なりにくい。",
        "線を曲げたいときは線を選択し、黄色い◆をドラッグ。直角はカギ線、なめらかな曲げは曲線。",
        "Shift を押しながら◆を動かすと、水平・垂直にそろえやすい。",
        "すでに引いた線の上に、別の流れを足すときは「07_線_上書き」。半透明の太線なので下線が残る。",
        "付記・番号・吹き出しは「08_コメント」。色は経路の色と揃える。",
        "意味の固定は「01_凡例」。色を経路以外（重要度など）に流用しない。",
    ]
    sh.put(3, 1, "label", "描き方")
    sh.merge(3, 1, 3, 4)
    for i, text in enumerate(steps):
        sh.row_heights[4 + i] = 20
        sh.put(4 + i, 1, "body", f"{i + 1}")
        sh.put(4 + i, 2, "body", text)
        sh.merge(4 + i, 2, 4 + i, 5)

    sh.put(15, 1, "label", "升目")
    sh.merge(15, 1, 15, 4)
    sh.row_heights[16] = 36
    sh.put(
        16,
        1,
        "body",
        "キャンバスと部品シートは同じ升目です。行の高さ 15pt、列幅 "
        f"{COL_WIDTH}（Meiryo UI 10pt・表示100%・拡大率100%でほぼ正方形）。"
        "表示倍率が125%や150%のPCでは縦横比がわずかにずれます。その場合も Alt を押した移動は枠に吸着するので、配置は崩れません。"
        "正方形に戻すときは、行をすべて選択して高さ15、列をすべて選択して幅を微調整します。",
    )
    sh.merge(16, 1, 16, 5)

    sh.put(18, 1, "label", "経路の7色")
    sh.put(19, 1, "small", "見本")
    sh.put(19, 2, "small", "色名")
    sh.put(19, 3, "small", "意味")
    sh.put(19, 4, "small", "区分")
    for i, c in enumerate(COLORS):
        r = 20 + i
        sh.row_heights[r] = 20
        sh.put(r, 1, "sw_" + c["key"], c["name"])
        sh.put(r, 2, "body", c["name"])
        sh.put(r, 3, "body", f"{c['role']}　{c['hint']}")
        sh.put(r, 4, "body", "基調" if c["group"] == "基調" else ("従来の3色" if c["group"] == "従来" else "今回追加"))

    sh.put(28, 1, "label", "上書き線の読み方")
    sh.merge(28, 1, 28, 4)
    sh.row_heights[29] = 48
    sh.put(
        29,
        1,
        "body",
        "本線（06）は細く不透明です。その上から、業務の流れや強調したい経路だけを上書き線（07）でなぞります。"
        "色は同じ7色ですが、白を混ぜた半透明の太線なので、下に既にある線・升目・枠を消しません。"
        "直角に折るときは「直角」か「直角・迂回」（折れを2回までハンドルで動かせます）。"
        "曲線にしたいときは「曲線」か「S字」。どちらも端点を16点のどこかへ接続できます。",
    )
    sh.merge(29, 1, 29, 5)

    sh.put(31, 1, "label", "シート")
    sheets = [
        ("00_使い方", "このページ"),
        ("01_凡例", "色、線、接続点の見本"),
        ("02_概要図", "システム単位のキャンバス。サンプル配置済み"),
        ("03_詳細図", "AWSと現場機器のキャンバス。サンプル配置済み"),
        ("04_部品_概要", "大きめの図形。7色"),
        ("05_部品_詳細", "AWSサービス名つきの図形。7色と図記号"),
        ("06_線_経路", "本線。直線・直角・曲線・破線・双方向"),
        ("07_線_上書き", "下線の上に足す太線。7色"),
        ("08_コメント", "付記カード、吹き出し、番号"),
    ]
    for i, (n, desc) in enumerate(sheets):
        sh.put(32 + i, 1, "label", n)
        sh.merge(32 + i, 1, 32 + i, 2)
        sh.put(32 + i, 3, "body", desc)
        sh.merge(32 + i, 3, 32 + i, 5)
    sh.rows = 42
    return sh


def build_legend() -> Sheet:
    sh = Sheet("01_凡例", 96, 78, grid=True, tab="3A3A3A")
    sh.freeze = (LABEL_W, 2)
    sh.title("01  凡例    経路の色はこの7色だけ。図形・本線・上書き線・付記を同じ色で揃える")
    d = sh.drawing
    sh.put(1, 0, "hint", "色")
    sh.merge(1, 0, 1, LABEL_W - 1)
    headers = [(16, "図形"), (34, "本線・直角"), (52, "上書き・直角"), (70, "付記")]
    for c, text in headers:
        sh.put(1, c, "label", text)
        for k in range(1, 12):
            sh.put(1, c + k, "label", None)
        sh.merge(1, c, 1, c + 11)
    row = 3
    for color in COLORS:
        sh.put(row, 0, "sw_" + color["key"], color["name"])
        for c in range(1, LABEL_W):
            sh.put(row, c, "sw_" + color["key"], None)
        sh.merge(row, 0, row + 5, LABEL_W - 1)
        place_node(d, None, f"凡例_{color['name']}", 16, row, 14, 5, "node", color["key"], color["name"], color["role"], "", True)
        d.add_connector(f"凡例線_{color['name']}", 34, row + 1, 48, row + 4, "bentConnector3", ln_base(color["hex"]))
        d.add_connector(
            f"凡例上書き_{color['name']}",
            52,
            row + 1,
            66,
            row + 4,
            "bentConnector3",
            ln_overlay(color["hex"]),
        )
        place_node(
            d,
            None,
            f"凡例付記_{color['name']}",
            70,
            row,
            16,
            5,
            "note",
            color["key"],
            color["name"],
            "付記を書く",
            color["hint"],
            True,
        )
        row += 7

    section_bar(sh, row, "接続点は各辺4か所（端から 12.5% / 37.5% / 62.5% / 87.5%）。角には置かない。円は22.5度間隔で16点。")
    row += 2
    place_node(d, "demo_a", "接続元", 16, row, 16, 8, "node", "ai", "NODE", "接続元", "辺の青い点で離す", True)
    place_node(d, "demo_b", "接続先", 40, row + 3, 16, 8, "node", "koke", "NODE", "接続先", "16点の任意の位置", True)
    d.connect("凡例_接続見本", "demo_a", 5, "demo_b", 13, "bentConnector3", ln_base(COLOR_BY["ai"]["hex"]))
    add_cxn_dots(d, "demo_a")
    place_node(d, "demo_c", "円", 64, row, 10, 10, "ellipse", "suoh", "", "円は16等分", "", True)
    add_cxn_dots(d, "demo_c")
    sh.rows = max(sh.rows, row + 16)
    return sh


def add_cxn_dots(d: Drawing, key):
    shape = d.registry[key]
    for i in range(16):
        x, y = point_of(shape, i)
        # Pull slightly inward so the dot illustrates the site without covering the hit target.
        cx = (shape["c1"] + shape["c2"]) / 2
        cy = (shape["r1"] + shape["r2"]) / 2
        x = cx + (x - cx) * 0.86
        y = cy + (y - cy) * 0.86
        c = int(math.floor(x))
        r = int(math.floor(y))
        # 1x1 dot sits on the cell containing the inset point. Skip if it would be 0-size.
        d.add_shape(
            f"点{i + 1}",
            c,
            r,
            c + 1,
            r + 1,
            cust_geom(ellipse_path(), []),
            fill_solid(INK),
            line_style(INK, 0.5, arrow="none"),
            [],
            anchor="ctr",
        )


def build_parts_overview() -> Sheet:
    sh = Sheet("04_部品_概要", 160, 20, grid=True, tab="6A6A66")
    sh.freeze = (LABEL_W, 1)
    sh.title("04  概要用の部品    大きい図形をコピーして 02_概要図 へ。左の色帯が経路色。Altで升目に吸着")
    sections = [
        {
            "title": "システムの箱",
            "items": [
                {"kicker": "SYS", "title": "システム名", "sub": "役割", "label": "システム"},
                {"kicker": "SRV", "title": "サーバ名", "sub": "役割", "label": "サーバ"},
                {"kicker": "DB", "title": "データベース", "sub": "用途", "label": "データベース"},
                {"kicker": "STR", "title": "ストレージ", "sub": "用途", "label": "ストレージ"},
                {"kicker": "LB", "title": "ロードバランサ", "sub": "受け口", "label": "ロードバランサ"},
                {"kicker": "FW", "title": "ファイアウォール", "sub": "境界", "label": "ファイアウォール"},
                {"kicker": "VPN", "title": "VPN / 専用線", "sub": "閉域", "label": "VPN・専用線"},
                {"kicker": "API", "title": "API", "sub": "インターフェース", "label": "API"},
                {"kicker": "QUE", "title": "キュー", "sub": "非同期", "label": "キュー"},
                {"kicker": "BAT", "title": "バッチ", "sub": "夜間 / 定時", "label": "バッチ"},
                {"kicker": "OPS", "title": "監視", "sub": "運用", "label": "監視"},
                {"kicker": "SITE", "title": "拠点名", "sub": "現場・工場", "label": "拠点・現場"},
                {"kicker": "SAAS", "title": "SaaS名", "sub": "外部サービス", "label": "外部SaaS"},
                {"kicker": "SFDC", "title": "Salesforce", "sub": "業務システム", "label": "Salesforce"},
            ],
        }
    ]
    row = catalog_nodes(sh, sh.drawing, sections, 2, 12, 5, True, "node")
    ell = [
        {
            "title": "人と外部の入口（円）",
            "items": [
                {"kicker": "", "title": "利用者", "sub": "", "label": "利用者", "form": "ellipse", "w": 8, "h": 8},
                {"kicker": "", "title": "インターネット", "sub": "", "label": "インターネット", "form": "ellipse", "w": 8, "h": 8},
            ],
        }
    ]
    # Ellipse pitch differs; catalog_nodes uses each item's w for pitch but headers were for 12.
    # Place ellipses with the standard 13-col pitch by padding w to stay readable — 8 is ok, gaps differ per row.
    row = catalog_nodes(sh, sh.drawing, ell, row, 8, 8, True, "ellipse")
    zones = [
        {
            "title": "領域の枠（中にシステムを置く。線は破線または実線）",
            "items": [
                {"kicker": "ZONE", "title": "領域名", "sub": "説明", "label": "領域", "form": "zone", "w": 18, "h": 8, "dash": "solid"},
                {"kicker": "CLOUD", "title": "クラウド", "sub": "アカウント", "label": "クラウド境界", "form": "zone", "w": 18, "h": 8, "dash": "dash"},
                {"kicker": "NET", "title": "ネットワーク", "sub": "VPC / セグメント", "label": "ネットワーク", "form": "zone", "w": 18, "h": 8, "dash": "sysDash"},
                {"kicker": "DMZ", "title": "DMZ / 公開", "sub": "境界", "label": "DMZ", "form": "zone", "w": 18, "h": 8, "dash": "dash"},
            ],
        }
    ]
    row = catalog_nodes(sh, sh.drawing, zones, row, 18, 8, True, "zone")
    row = icon_row(sh, sh.drawing, row, "概要で使う図記号（墨）。色分けはノードと線で行う")
    sh.rows = row + 2
    sh.cols = max(sh.cols, LABEL_W + 7 * 19)
    return sh


def icon_row(sh, drawing, row, title):
    section_bar(sh, row, title)
    row += 1
    icons = [
        ("server", "サーバ"),
        ("lambda", "関数"),
        ("bucket", "ストレージ"),
        ("cylinder", "DB"),
        ("cloud", "クラウド"),
        ("vpc", "VPC"),
        ("lb", "LB"),
        ("fw", "FW"),
        ("vpn", "VPN"),
        ("user", "利用者"),
        ("factory", "現場"),
        ("globe", "外部"),
        ("queue", "キュー"),
        ("api", "API"),
        ("eye", "監視"),
    ]
    sh.put(row, 0, "label", "図記号")
    for c in range(1, LABEL_W):
        sh.put(row, c, "label", None)
    sh.merge(row, 0, row + 7, LABEL_W - 1)
    for i, (glyph, caption) in enumerate(icons):
        col = LABEL_W + i * 9
        place_icon(drawing, None, f"図記号_{caption}", col, row, 8, 8, glyph, caption)
    return row + 10


def build_parts_detail() -> Sheet:
    sh = Sheet("05_部品_詳細", 150, 20, grid=True, tab="6A6A66")
    sh.freeze = (LABEL_W, 1)
    sh.title("05  詳細用の部品    サービス名つき。コピーして 03_詳細図 へ。領域の枠は下の方")
    def item(kicker, title, label=None, sub=""):
        return {"kicker": kicker, "title": title, "sub": sub, "label": label or f"{kicker}  {title}"}

    sections = [
        {
            "title": "汎用",
            "items": [
                item("SYS", "システム"),
                item("SRV", "サーバ"),
                item("DB", "データベース"),
                item("STR", "ストレージ"),
                item("LB", "ロードバランサ"),
                item("FW", "ファイアウォール"),
                item("VPN", "VPN / 専用線"),
                item("API", "API"),
                item("QUE", "キュー"),
                item("BAT", "バッチ"),
                item("OPS", "監視"),
                item("SITE", "現場機器"),
                item("SAAS", "外部SaaS"),
                item("SFDC", "Salesforce"),
            ],
        },
        {
            "title": "AWS  コンピュート",
            "items": [
                item("EC2", "仮想サーバ"),
                item("Lambda", "関数"),
                item("ECS", "コンテナ"),
                item("EKS", "Kubernetes"),
                item("Fargate", "サーバレス"),
                item("ASG", "Auto Scaling"),
                item("Batch", "バッチ"),
            ],
        },
        {
            "title": "AWS  ストレージ",
            "items": [
                item("S3", "オブジェクト"),
                item("EBS", "ブロック"),
                item("EFS", "ファイル"),
            ],
        },
        {
            "title": "AWS  データベース",
            "items": [
                item("RDS", "リレーショナル"),
                item("Aurora", "RDS互換"),
                item("DynamoDB", "キーバリュー"),
                item("ElastiCache", "キャッシュ"),
                item("Redshift", "分析"),
            ],
        },
        {
            "title": "AWS  ネットワーク",
            "items": [
                item("VPC", "仮想ネット"),
                item("Subnet", "サブネット"),
                item("IGW", "Internet GW"),
                item("NAT", "NAT GW"),
                item("ALB", "Application LB"),
                item("NLB", "Network LB"),
                item("Route53", "DNS"),
                item("CloudFront", "CDN"),
                item("APIGW", "API Gateway"),
                item("VPN", "Site-to-Site"),
                item("DX", "Direct Connect"),
                item("TGW", "Transit GW"),
                item("VPCE", "Endpoint"),
            ],
        },
        {
            "title": "AWS  セキュリティ",
            "items": [
                item("IAM", "権限"),
                item("WAF", "Web ACL"),
                item("SG", "Security Group"),
                item("KMS", "暗号鍵"),
                item("Secrets", "シークレット"),
            ],
        },
        {
            "title": "AWS  連携・運用",
            "items": [
                item("SQS", "キュー"),
                item("SNS", "通知"),
                item("EventBridge", "イベント"),
                item("SFN", "Step Functions"),
                item("CloudWatch", "監視"),
                item("CloudTrail", "監査"),
                item("SSM", "Systems Manager"),
            ],
        },
    ]
    row = catalog_nodes(sh, sh.drawing, sections, 2, 9, 4, False, "node")
    ell = [
        {
            "title": "円",
            "items": [
                {"kicker": "", "title": "利用者", "sub": "", "label": "利用者", "form": "ellipse", "w": 6, "h": 6},
                {"kicker": "", "title": "インターネット", "sub": "", "label": "インターネット", "form": "ellipse", "w": 6, "h": 6},
            ],
        }
    ]
    row = catalog_nodes(sh, sh.drawing, ell, row, 6, 6, False, "ellipse")
    zones = [
        {
            "title": "領域の枠",
            "items": [
                {"kicker": "ACCT", "title": "AWSアカウント", "sub": "ap-northeast-1", "label": "アカウント", "form": "zone", "w": 16, "h": 7, "dash": "dash"},
                {"kicker": "VPC", "title": "VPC", "sub": "10.0.0.0/16", "label": "VPC", "form": "zone", "w": 16, "h": 7, "dash": "solid"},
                {"kicker": "SUB", "title": "Subnet", "sub": "10.0.1.0/24", "label": "サブネット", "form": "zone", "w": 16, "h": 7, "dash": "sysDash"},
                {"kicker": "SITE", "title": "現場セグメント", "sub": "閉域", "label": "現場", "form": "zone", "w": 16, "h": 7, "dash": "dash"},
            ],
        }
    ]
    row = catalog_nodes(sh, sh.drawing, zones, row, 16, 7, True, "zone")
    row = icon_row(sh, sh.drawing, row, "図記号（墨・モノライン）。サービス名のタイルと組み合わせて使う")
    sh.rows = row + 2
    sh.cols = max(sh.cols, LABEL_W + 7 * 17)
    return sh


def build_comments() -> Sheet:
    sh = Sheet("08_コメント", 140, 40, grid=True, tab="53425F")
    sh.freeze = (LABEL_W, 1)
    sh.title("08  コメント    経路と同じ色で置く。カードは説明、吹き出しは一点を指す、番号は書き換える")
    sections = [
        {
            "title": "付記カード（複数行。図形の文字を直接編集する）",
            "items": [
                {"kicker": "NOTE", "title": "付記を書く", "sub": "二行目", "label": "付記カード", "form": "note", "w": 15, "h": 6}
            ],
        },
        {
            "title": "吹き出し（尾で対象を指す。尾の先端も接続点）",
            "items": [
                {"kicker": "", "title": "注釈", "sub": "対象を指す", "label": "吹き出し", "form": "callout", "w": 15, "h": 8}
            ],
        },
        {
            "title": "番号ピン（数字は書き換える）",
            "items": [
                {"kicker": "", "title": "1", "sub": "", "label": "番号", "form": "pin", "w": 4, "h": 4}
            ],
        },
        {
            "title": "短いラベル（線の脇に置く）",
            "items": [
                {"kicker": "", "title": "本番系", "sub": "", "label": "短ラベル", "form": "label", "w": 12, "h": 3}
            ],
        },
    ]
    row = catalog_nodes(sh, sh.drawing, sections, 2, 15, 6, True, "note")
    sh.rows = row + 2
    return sh


def overlaps(a, b):
    return not (a[0] + a[2] <= b[0] or b[0] + b[2] <= a[0] or a[1] + a[3] <= b[1] or b[1] + b[3] <= a[1])


def assert_layout(nodes, zones):
    for i, a in enumerate(nodes):
        for b in nodes[i + 1 :]:
            if overlaps(a["box"], b["box"]):
                raise SystemExit(f"overlap {a['key']} {b['key']} {a['box']} {b['box']}")
    for n in nodes:
        if n.get("zone"):
            z = zones[n["zone"]]
            x, y, w, h = n["box"]
            zx, zy, zw, zh = z
            if not (x >= zx + 1 and y >= zy + 1 and x + w <= zx + zw - 1 and y + h <= zy + zh - 1):
                raise SystemExit(f"outside {n['key']} {n['box']} zone {n['zone']} {z}")


def build_canvas(name, title, tab, cols, rows, spec) -> tuple[Sheet, dict]:
    sh = Sheet(name, cols, rows, grid=True, tab=tab)
    sh.title(title)
    d = sh.drawing
    preview = {"cols": cols, "rows": rows, "title": title, "shapes": [], "lines": []}
    # zones first (back)
    for z in spec["zones"]:
        place_node(
            d,
            z["key"],
            z["title"],
            z["x"],
            z["y"],
            z["w"],
            z["h"],
            "zone",
            z["color"],
            z.get("kicker", ""),
            z["title"],
            z.get("sub", ""),
            True,
            dash=z.get("dash", "dash"),
        )
        preview["shapes"].append({**z, "form": "zone"})
    for n in spec["nodes"]:
        place_node(
            d,
            n["key"],
            n["title"],
            n["x"],
            n["y"],
            n["w"],
            n["h"],
            n.get("form", "node"),
            n["color"],
            n.get("kicker", ""),
            n["title"],
            n.get("sub", ""),
            n.get("large", True),
        )
        preview["shapes"].append({**{k: n[k] for k in n if k != "zone"}, "form": n.get("form", "node")})
    for ln in spec["lines"]:
        color = COLOR_BY[ln["color"]]["hex"]
        if ln.get("overlay"):
            style = ln_overlay(color, curved=ln.get("preset", "").startswith("curved"))
        else:
            style = ln_base(color, dashed=ln.get("dashed", False), pt=1.35)
            if str(ln.get("preset", "")).startswith("curved"):
                style = line_style(color, 1.5, arrow="triangle", join="round", width_arrow="sm")
        d.connect(
            ln["name"],
            ln["a"],
            ln["ia"],
            ln["b"],
            ln["ib"],
            ln.get("preset", "bentConnector3"),
            style,
        )
        preview["lines"].append(
            {
                "a": ln["a"],
                "ia": ln["ia"],
                "b": ln["b"],
                "ib": ln["ib"],
                "color": ln["color"],
                "preset": ln.get("preset", "bentConnector3"),
                "overlay": bool(ln.get("overlay")),
                "dashed": bool(ln.get("dashed")),
            }
        )
    for note in spec.get("notes", []):
        place_node(
            d,
            note["key"],
            note["title"],
            note["x"],
            note["y"],
            note["w"],
            note["h"],
            note.get("form", "note"),
            note["color"],
            note.get("kicker", ""),
            note["title"],
            note.get("sub", ""),
            True,
        )
        preview["shapes"].append({**note, "form": note.get("form", "note")})
    return sh, preview


def overview_spec():
    zones = {
        "site": (1, 2, 24, 34),
        "intra": (26, 2, 16, 34),
        "aws": (43, 2, 36, 52),
        "saas": (80, 2, 18, 18),
        "users": (80, 21, 18, 24),
    }
    zone_list = [
        {"key": "z_site", "title": "現場・工場", "sub": "オンプレ", "kicker": "SITE", "color": "koke", "x": 1, "y": 2, "w": 24, "h": 34, "dash": "dash"},
        {"key": "z_intra", "title": "拠点閉域", "sub": "社内WAN", "kicker": "WAN", "color": "ai", "x": 26, "y": 2, "w": 16, "h": 34, "dash": "dash"},
        {"key": "z_aws", "title": "AWS  東京", "sub": "アカウント", "kicker": "CLOUD", "color": "sumi", "x": 43, "y": 2, "w": 36, "h": 52, "dash": "dash"},
        {"key": "z_vpc", "title": "VPC", "sub": "10.0.0.0/16", "kicker": "VPC", "color": "ai", "x": 45, "y": 6, "w": 32, "h": 44, "dash": "solid"},
        {"key": "z_pub", "title": "Public", "sub": "10.0.1.0/24", "kicker": "SUB", "color": "suoh", "x": 47, "y": 10, "w": 28, "h": 10, "dash": "sysDash"},
        {"key": "z_app", "title": "App", "sub": "10.0.2.0/24", "kicker": "SUB", "color": "ai", "x": 47, "y": 21, "w": 28, "h": 12, "dash": "sysDash"},
        {"key": "z_data", "title": "Data", "sub": "10.0.3.0/24", "kicker": "SUB", "color": "asagi", "x": 47, "y": 34, "w": 28, "h": 12, "dash": "sysDash"},
        {"key": "z_saas", "title": "外部SaaS", "sub": "業務", "kicker": "SAAS", "color": "kincha", "x": 80, "y": 2, "w": 18, "h": 18, "dash": "dash"},
        {"key": "z_users", "title": "利用者・外部", "sub": "公開側", "kicker": "EXT", "color": "suoh", "x": 80, "y": 21, "w": 18, "h": 24, "dash": "dash"},
    ]
    nodes = [
        {"key": "factory", "title": "工場拠点", "kicker": "SITE", "sub": "現場", "color": "koke", "x": 4, "y": 6, "w": 16, "h": 5, "zone": "site"},
        {"key": "term", "title": "現場端末", "kicker": "CLT", "sub": "作業", "color": "koke", "x": 4, "y": 13, "w": 16, "h": 5, "zone": "site"},
        {"key": "fw", "title": "拠点FW", "kicker": "FW", "sub": "境界", "color": "koke", "x": 4, "y": 20, "w": 16, "h": 5, "zone": "site"},
        {"key": "odb", "title": "オンプレDB", "kicker": "DB", "sub": "実績", "color": "koke", "x": 4, "y": 27, "w": 16, "h": 5, "zone": "site"},
        {"key": "router", "title": "拠点ルータ", "kicker": "L3", "sub": "閉域", "color": "ai", "x": 28, "y": 7, "w": 12, "h": 5, "zone": "intra"},
        {"key": "vpn", "title": "VPN", "kicker": "VPN", "sub": "対AWS", "color": "ai", "x": 28, "y": 16, "w": 12, "h": 5, "zone": "intra"},
        {"key": "mon", "title": "監視基盤", "kicker": "OPS", "sub": "死活", "color": "murasaki", "x": 28, "y": 25, "w": 12, "h": 5, "zone": "intra"},
        {"key": "alb", "title": "ALB", "kicker": "ALB", "sub": "公開", "color": "suoh", "x": 49, "y": 13, "w": 12, "h": 4, "zone": "pub"},
        {"key": "igw", "title": "IGW", "kicker": "IGW", "sub": "入口", "color": "suoh", "x": 63, "y": 13, "w": 10, "h": 4, "zone": "pub"},
        {"key": "web", "title": "Web", "kicker": "EC2", "sub": "フロント", "color": "ai", "x": 49, "y": 24, "w": 12, "h": 4, "zone": "app"},
        {"key": "api", "title": "API", "kicker": "EC2", "sub": "業務", "color": "ai", "x": 63, "y": 24, "w": 10, "h": 4, "zone": "app"},
        {"key": "rds", "title": "業務DB", "kicker": "RDS", "sub": "本番", "color": "asagi", "x": 49, "y": 37, "w": 12, "h": 4, "zone": "data"},
        {"key": "s3", "title": "証跡", "kicker": "S3", "sub": "保管", "color": "asagi", "x": 63, "y": 37, "w": 10, "h": 4, "zone": "data"},
        {"key": "sfdc", "title": "Salesforce", "kicker": "SFDC", "sub": "顧客", "color": "kincha", "x": 82, "y": 7, "w": 14, "h": 5, "zone": "saas"},
        {"key": "net", "title": "Internet", "kicker": "", "sub": "", "color": "suoh", "x": 83, "y": 24, "w": 12, "h": 8, "form": "ellipse", "zone": "users"},
        {"key": "user", "title": "本部利用者", "kicker": "", "sub": "", "color": "suoh", "x": 83, "y": 34, "w": 12, "h": 8, "form": "ellipse", "zone": "users"},
    ]
    # zone keys in nodes refer to short ids; map boxes
    zone_boxes = {
        "site": zones["site"],
        "intra": zones["intra"],
        "aws": zones["aws"],
        "pub": (47, 10, 28, 10),
        "app": (47, 21, 28, 12),
        "data": (47, 34, 28, 12),
        "saas": zones["saas"],
        "users": zones["users"],
        "vpc": (45, 6, 32, 44),
    }
    # pub/app/data nodes must sit inside those tighter zones, which are inside vpc/aws.
    # factory etc use site. The containment check uses the immediate zone.
    laid = []
    for n in nodes:
        laid.append({**n, "box": (n["x"], n["y"], n["w"], n["h"])})
    assert_layout(laid, zone_boxes)
    lines = [
        {"name": "現場縦1", "a": "factory", "ia": 9, "b": "term", "ib": 1, "color": "koke"},
        {"name": "現場縦2", "a": "term", "ia": 9, "b": "fw", "ib": 1, "color": "koke"},
        {"name": "現場縦3", "a": "fw", "ia": 9, "b": "odb", "ib": 1, "color": "koke"},
        {"name": "拠点へ", "a": "fw", "ia": 6, "b": "router", "ib": 12, "color": "koke"},
        {"name": "閉域", "a": "router", "ia": 9, "b": "vpn", "ib": 1, "color": "ai"},
        {"name": "VPNからALB", "a": "vpn", "ia": 7, "b": "alb", "ib": 12, "color": "ai"},
        {"name": "ALBからWeb", "a": "alb", "ia": 9, "b": "web", "ib": 1, "color": "ai"},
        {"name": "WebからAPI", "a": "web", "ia": 6, "b": "api", "ib": 13, "color": "ai"},
        {"name": "APIからDB", "a": "api", "ia": 10, "b": "rds", "ib": 2, "color": "asagi"},
        {"name": "APIからS3", "a": "api", "ia": 11, "b": "s3", "ib": 1, "color": "asagi"},
        {"name": "SaaS連携", "a": "api", "ia": 5, "b": "sfdc", "ib": 15, "color": "kincha"},
        {"name": "利用者入口", "a": "user", "ia": 8, "b": "igw", "ib": 7, "color": "suoh"},
        {"name": "IGWからALB", "a": "igw", "ia": 12, "b": "alb", "ib": 7, "color": "suoh"},
        {"name": "外部から", "a": "net", "ia": 8, "b": "igw", "ib": 5, "color": "suoh"},
        {"name": "監視", "a": "mon", "ia": 7, "b": "web", "ib": 12, "color": "murasaki", "dashed": True},
        {"name": "上書き_SaaSの流れ", "a": "term", "ia": 7, "b": "sfdc", "ib": 13, "color": "kincha", "overlay": True, "preset": "bentConnector5"},
        {"name": "上書き_データ", "a": "api", "ia": 9, "b": "rds", "ib": 3, "color": "asagi", "overlay": True, "preset": "curvedConnector3"},
    ]
    notes = [
        {"key": "n1", "title": "受注はSalesforce", "sub": "金茶でたどる", "kicker": "金茶", "color": "kincha", "x": 82, "y": 13, "w": 14, "h": 5, "form": "note"},
        {"key": "n2", "title": "監視は紫", "sub": "死活・ログ", "kicker": "紫", "color": "murasaki", "x": 28, "y": 31, "w": 12, "h": 4, "form": "note"},
    ]
    return {"zones": zone_list, "nodes": nodes, "lines": lines, "notes": notes}


def detail_spec():
    zone_boxes = {
        "site": (1, 2, 28, 46),
        "wan": (30, 2, 16, 46),
        "aws": (47, 2, 64, 56),
        "vpc": (49, 6, 42, 40),
        "pub": (51, 9, 38, 9),
        "app": (51, 19, 38, 12),
        "data": (51, 32, 38, 11),
        "ops": (92, 8, 16, 36),
        "saas": (112, 2, 18, 20),
        "ext": (112, 24, 18, 22),
    }
    zone_list = [
        {"key": "dz_site", "title": "現場セグメント", "sub": "工場LAN", "kicker": "OT", "color": "koke", "x": 1, "y": 2, "w": 28, "h": 46, "dash": "dash"},
        {"key": "dz_wan", "title": "閉域・DC", "sub": "専用線", "kicker": "WAN", "color": "ai", "x": 30, "y": 2, "w": 16, "h": 46, "dash": "dash"},
        {"key": "dz_aws", "title": "AWS ap-northeast-1", "sub": "本番アカウント", "kicker": "ACCT", "color": "sumi", "x": 47, "y": 2, "w": 64, "h": 56, "dash": "dash"},
        {"key": "dz_vpc", "title": "VPC prod", "sub": "10.20.0.0/16", "kicker": "VPC", "color": "ai", "x": 49, "y": 6, "w": 42, "h": 40, "dash": "solid"},
        {"key": "dz_pub", "title": "public-a", "sub": "10.20.0.0/24", "kicker": "SUB", "color": "suoh", "x": 51, "y": 9, "w": 38, "h": 9, "dash": "sysDash"},
        {"key": "dz_app", "title": "app-a", "sub": "10.20.1.0/24", "kicker": "SUB", "color": "ai", "x": 51, "y": 19, "w": 38, "h": 12, "dash": "sysDash"},
        {"key": "dz_data", "title": "data-a", "sub": "10.20.2.0/24", "kicker": "SUB", "color": "asagi", "x": 51, "y": 32, "w": 38, "h": 11, "dash": "sysDash"},
        {"key": "dz_ops", "title": "共通サービス", "sub": "アカウント共通", "kicker": "OPS", "color": "murasaki", "x": 92, "y": 8, "w": 16, "h": 36, "dash": "sysDash"},
        {"key": "dz_saas", "title": "SaaS", "sub": "業務", "kicker": "SAAS", "color": "kincha", "x": 112, "y": 2, "w": 18, "h": 20, "dash": "dash"},
        {"key": "dz_ext", "title": "外部", "sub": "インターネット", "kicker": "EXT", "color": "suoh", "x": 112, "y": 24, "w": 18, "h": 22, "dash": "dash"},
    ]
    N = []

    def add(key, title, kicker, color, x, y, zone, w=10, h=3, sub="", form="node"):
        N.append(
            {
                "key": key,
                "title": title,
                "kicker": kicker,
                "sub": sub,
                "color": color,
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "zone": zone,
                "form": form,
                "large": False,
            }
        )

    add("plc", "PLC", "OT", "koke", 3, 6, "site")
    add("sensor", "センサ", "OT", "koke", 15, 6, "site")
    add("hist", "ヒストリアン", "SRV", "koke", 3, 12, "site")
    add("scada", "SCADA", "SRV", "koke", 15, 12, "site")
    add("sfw", "現場FW", "FW", "koke", 3, 18, "site")
    add("l3", "L3スイッチ", "L3", "koke", 15, 18, "site")
    add("fs", "ファイル", "STR", "koke", 3, 24, "site", sub="図面")
    add("hmi", "現場端末", "CLT", "koke", 15, 24, "site")
    add("rt", "拠点ルータ", "L3", "ai", 32, 8, "wan", w=12)
    add("vpn2", "VPN GW", "VPN", "ai", 32, 16, "wan", w=12)
    add("dx", "Direct Connect", "DX", "ai", 32, 24, "wan", w=12)
    add("proxy", "Proxy", "SRV", "ai", 32, 32, "wan", w=12)
    add("igw2", "IGW", "IGW", "suoh", 53, 12, "pub", w=8)
    add("waf", "WAF", "WAF", "suoh", 63, 12, "pub", w=8)
    add("alb2", "ALB", "ALB", "suoh", 73, 12, "pub", w=8)
    add("nat", "NAT", "NAT", "ai", 83, 12, "pub", w=5)
    add("ec2w", "Web", "EC2", "ai", 53, 23, "app", w=8)
    add("ec2a", "API", "EC2", "ai", 63, 23, "app", w=8)
    add("ecs", "Worker", "ECS", "ai", 73, 23, "app", w=8)
    add("lam", "Webhook", "Lambda", "asagi", 83, 23, "app", w=5)
    add("rds2", "Aurora", "RDS", "asagi", 53, 36, "data", w=8)
    add("cache", "Cache", "ElastiCache", "asagi", 63, 36, "data", w=8)
    add("s3b", "Bucket", "S3", "asagi", 73, 36, "data", w=8)
    add("sqs", "Queue", "SQS", "asagi", 83, 36, "data", w=5)
    add("cw", "CloudWatch", "OPS", "murasaki", 94, 12, "ops", w=12)
    add("iam", "IAM", "IAM", "murasaki", 94, 18, "ops", w=12)
    add("trail", "CloudTrail", "OPS", "murasaki", 94, 24, "ops", w=12)
    add("r53", "Route 53", "DNS", "suoh", 94, 30, "ops", w=12)
    add("sfn", "Step Functions", "SFN", "asagi", 94, 36, "ops", w=12)
    add("sfdc2", "Salesforce", "SFDC", "kincha", 114, 8, "saas", w=14, h=4)
    add("inet", "Internet", "", "suoh", 115, 28, "ext", w=12, h=8, form="ellipse")
    add("hq", "本部ユーザ", "", "suoh", 115, 38, "ext", w=12, h=6, form="ellipse")
    laid = [{**n, "box": (n["x"], n["y"], n["w"], n["h"])} for n in N]
    assert_layout(laid, zone_boxes)
    lines = [
        {"name": "PLCから履歴", "a": "plc", "ia": 9, "b": "hist", "ib": 1, "color": "koke"},
        {"name": "センサからSCADA", "a": "sensor", "ia": 9, "b": "scada", "ib": 1, "color": "koke"},
        {"name": "履歴からFW", "a": "hist", "ia": 9, "b": "sfw", "ib": 1, "color": "koke"},
        {"name": "SCADAからL3", "a": "scada", "ia": 9, "b": "l3", "ib": 1, "color": "koke"},
        {"name": "FWからルータ", "a": "sfw", "ia": 7, "b": "rt", "ib": 12, "color": "koke"},
        {"name": "ルータからVPN", "a": "rt", "ia": 9, "b": "vpn2", "ib": 1, "color": "ai"},
        {"name": "VPNからNAT", "a": "vpn2", "ia": 7, "b": "nat", "ib": 12, "color": "ai"},
        {"name": "DXからAPI", "a": "dx", "ia": 6, "b": "ec2a", "ib": 12, "color": "ai"},
        {"name": "InternetからIGW", "a": "inet", "ia": 8, "b": "igw2", "ib": 4, "color": "suoh"},
        {"name": "利用者からCDN経由IGW", "a": "hq", "ia": 12, "b": "r53", "ib": 7, "color": "suoh"},
        {"name": "IGWからWAF", "a": "igw2", "ia": 6, "b": "waf", "ib": 13, "color": "suoh"},
        {"name": "WAFからALB", "a": "waf", "ia": 6, "b": "alb2", "ib": 13, "color": "suoh"},
        {"name": "ALBからWeb", "a": "alb2", "ia": 9, "b": "ec2w", "ib": 3, "color": "ai"},
        {"name": "WebからAPI", "a": "ec2w", "ia": 6, "b": "ec2a", "ib": 13, "color": "ai"},
        {"name": "APIからWorker", "a": "ec2a", "ia": 6, "b": "ecs", "ib": 13, "color": "ai"},
        {"name": "APIからAurora", "a": "ec2a", "ia": 10, "b": "rds2", "ib": 2, "color": "asagi"},
        {"name": "APIからCache", "a": "ec2a", "ia": 11, "b": "cache", "ib": 1, "color": "asagi"},
        {"name": "WorkerからSQS", "a": "ecs", "ia": 10, "b": "sqs", "ib": 2, "color": "asagi"},
        {"name": "LambdaからSFN", "a": "lam", "ia": 7, "b": "sfn", "ib": 12, "color": "asagi"},
        {"name": "APIからSalesforce", "a": "ec2a", "ia": 5, "b": "sfdc2", "ib": 15, "color": "kincha"},
        {"name": "監視", "a": "cw", "ia": 12, "b": "ecs", "ib": 7, "color": "murasaki", "dashed": True},
        {"name": "上書き_現場からSaaS", "a": "plc", "ia": 7, "b": "sfdc2", "ib": 13, "color": "kincha", "overlay": True, "preset": "bentConnector5"},
        {"name": "上書き_データ経路", "a": "ec2a", "ia": 9, "b": "rds2", "ib": 3, "color": "asagi", "overlay": True, "preset": "curvedConnector3"},
        {"name": "上書き_公開経路", "a": "inet", "ia": 12, "b": "alb2", "ib": 3, "color": "suoh", "overlay": True, "preset": "bentConnector3"},
    ]
    notes = [
        {"key": "dn1", "title": "マスタはSalesforce", "sub": "金茶の太線が業務の流れ", "kicker": "金茶", "color": "kincha", "x": 114, "y": 14, "w": 14, "h": 5, "form": "note"},
        {"key": "dn2", "title": "データは浅葱", "sub": "API・DB・キュー", "kicker": "浅葱", "color": "asagi", "x": 53, "y": 40, "w": 14, "h": 4, "form": "note"},
        {"key": "dn3", "title": "監視は紫の破線", "sub": "本線と混ぜない", "kicker": "紫", "color": "murasaki", "x": 94, "y": 42, "w": 12, "h": 4, "form": "label"},
    ]
    return {"zones": zone_list, "nodes": N, "lines": lines, "notes": notes}


def check_sheet(sh: Sheet):
    boxes = []
    fx, fy = sh.freeze if sh.freeze else (0, 0)
    for r1, c1, r2, c2 in sh.merges:
        if r1 > r2 or c1 > c2:
            raise SystemExit(f"bad merge {sh.name} {(r1, c1, r2, c2)}")
        if fx and c1 < fx <= c2:
            raise SystemExit(f"merge crosses freeze col {sh.name} {(r1, c1, r2, c2)}")
        if fy and r1 < fy <= r2:
            raise SystemExit(f"merge crosses freeze row {sh.name} {(r1, c1, r2, c2)}")
        for o in boxes:
            if not (r2 < o[0] or o[2] < r1 or c2 < o[1] or o[3] < c1):
                raise SystemExit(f"merge overlap {sh.name} {(r1, c1, r2, c2)} vs {o}")
        boxes.append((r1, c1, r2, c2))
    if not sh.drawing:
        return
    ids = set()
    import re

    for part in sh.drawing.parts:
        for found in re.findall(r'<xdr:cNvPr id="(\d+)"', part):
            if found in ids:
                raise SystemExit(f"dup id {found} {sh.name}")
            ids.add(found)
        for ref in re.findall(r'<a:(?:st|end)Cxn id="(\d+)" idx="(\d+)"', part):
            if ref[0] not in ids and False:
                pass
    # second pass once all ids known
    for part in sh.drawing.parts:
        for ref, idx in re.findall(r'<a:(?:st|end)Cxn id="(\d+)" idx="(\d+)"', part):
            if ref not in ids:
                raise SystemExit(f"missing cxn target {ref} on {sh.name}")
            if int(idx) > 15:
                raise SystemExit(f"idx {idx} {sh.name}")


def build_all():
    styles = prepare_styles()
    howto = build_howto(styles)
    legend = build_legend()
    ov_sheet, ov_prev = build_canvas(
        "02_概要図",
        "02  概要図    サンプルは消して使ってよい    Alt+ドラッグで升目に吸着    線は06    上書きは07    付記は08",
        "1C1C1C",
        100,
        58,
        overview_spec(),
    )
    dt_sheet, dt_prev = build_canvas(
        "03_詳細図",
        "03  詳細図    VPC・現場機器の単位    Alt+ドラッグで吸着    部品は05    上書きの太線は下の線を消さない",
        "1C1C1C",
        132,
        62,
        detail_spec(),
    )
    parts_o = build_parts_overview()
    parts_d = build_parts_detail()
    lines = Sheet("06_線_経路", 110, 20, grid=True, tab="2A4668")
    line_library(lines, overlay=False)
    over = Sheet("07_線_上書き", 110, 20, grid=True, tab="7A5A2C")
    line_library(over, overlay=True)
    comments = build_comments()
    sheets = [howto, legend, ov_sheet, dt_sheet, parts_o, parts_d, lines, over, comments]
    # Ensure grid sheets cover their drawings' anchors.
    for sh in sheets:
        if not sh.drawing:
            check_sheet(sh)
            continue
        for shape in sh.drawing.registry.values():
            sh.cols = max(sh.cols, shape["c2"] + 2)
            sh.rows = max(sh.rows, shape["r2"] + 2)
        check_sheet(sh)
    pack(styles, sheets)
    write_catalog(ov_prev, dt_prev)
    print(f"wrote {OUT_PUBLIC}")
    for sh in sheets:
        n = len(sh.drawing.parts) if sh.drawing else 0
        print(f"  {sh.name:16} shapes={n:4} grid={sh.cols}x{sh.rows}")


def write_catalog(overview, detail):
    payload = {
        "colors": COLORS,
        "colWidth": COL_WIDTH,
        "rowPt": ROW_PT,
        "sheets": [
            {"name": "00_使い方", "text": "手順、升目、7色の約束"},
            {"name": "01_凡例", "text": "図形・本線・上書き線・付記を色別に並べた見本"},
            {"name": "02_概要図", "text": "システム単位。現場、閉域、AWS、SaaSの見取り図"},
            {"name": "03_詳細図", "text": "サブネット、AWSサービス、現場機器"},
            {"name": "04_部品_概要", "text": "大きいノード、領域、図記号。各7色"},
            {"name": "05_部品_詳細", "text": "AWSサービス名つきの小さいノード。各7色"},
            {"name": "06_線_経路", "text": "直線、直角、曲線、破線、双方向"},
            {"name": "07_線_上書き", "text": "半透明の太線。直角、迂回、曲線、S字"},
            {"name": "08_コメント", "text": "付記カード、吹き出し、番号、短ラベル"},
        ],
        "steps": [
            "概要図か詳細図を開く",
            "部品シートから図形をコピーする",
            "Altを押しながら置くと升目に吸着する",
            "経路線の端を、辺16点のどれかに接続する",
            "黄色いハンドルで直角か曲線に曲げる",
            "下の線を残したまま、上書き線で流れを足す",
        ],
        "overview": overview,
        "detail": detail,
    }
    OUT_CATALOG.parent.mkdir(parents=True, exist_ok=True)
    text = "export const catalog = " + json.dumps(payload, ensure_ascii=False, indent=2) + " as const;\n"
    OUT_CATALOG.write_text(text, encoding="utf-8")


def pack(styles: Styles, sheets: list[Sheet]):
    files: dict[str, str] = {}
    overrides = [
        ("/xl/workbook.xml", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"),
        ("/xl/styles.xml", "application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"),
        ("/xl/theme/theme1.xml", "application/vnd.openxmlformats-officedocument.theme+xml"),
        ("/docProps/core.xml", "application/vnd.openxmlformats-package.core-properties+xml"),
        ("/docProps/app.xml", "application/vnd.openxmlformats-officedocument.extended-properties+xml"),
    ]
    wb_sheets = []
    wb_rels = []
    for i, sh in enumerate(sheets, start=1):
        path = f"xl/worksheets/sheet{i}.xml"
        files[path] = sheet_xml(sh, styles)
        overrides.append(
            (f"/{path}", "application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml")
        )
        wb_sheets.append(f'<sheet name="{xe(sh.name)}" sheetId="{i}" r:id="rId{i}"/>')
        wb_rels.append(
            f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>'
        )
        if sh.drawing and sh.drawing.parts:
            dpath = f"xl/drawings/drawing{i}.xml"
            files[dpath] = sh.drawing.xml()
            overrides.append((f"/{dpath}", "application/vnd.openxmlformats-officedocument.drawing+xml"))
            files[f"xl/worksheets/_rels/sheet{i}.xml.rels"] = (
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                f'<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/drawing" Target="../drawings/drawing{i}.xml"/>'
                "</Relationships>"
            )
    files["xl/styles.xml"] = styles.xml()
    files["xl/theme/theme1.xml"] = theme_xml()
    files["xl/workbook.xml"] = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<fileVersion appName="xl" lastEdited="7" lowestEdited="6" rupBuild="22842"/>'
        '<workbookPr defaultThemeVersion="164011"/>'
        '<bookViews><workbookView xWindow="0" yWindow="0" windowWidth="36000" windowHeight="20000" activeTab="2"/></bookViews>'
        f'<sheets>{"".join(wb_sheets)}</sheets>'
        '<calcPr calcId="191029"/>'
        "</workbook>"
    )
    files["xl/_rels/workbook.xml.rels"] = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + "".join(wb_rels)
        + '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        + '<Relationship Id="rIdTheme" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>'
        + "</Relationships>"
    )
    # fix rel ids: I used rIdStyles which is fine as long as unique. Worksheets use rId1..n. styles shouldn't collide.
    # rIdStyles is unique. Good.
    files["docProps/core.xml"] = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        "<dc:title>システム構成図テンプレート</dc:title>"
        "<dc:subject>現場・社内・AWS・外部SaaS</dc:subject>"
        "<dc:description>Meiryo UI。方眼、16接続点、経路7色、上書き用の半透明太線。</dc:description>"
        "<dc:creator>システム構成図テンプレート</dc:creator>"
        "<cp:lastModifiedBy>システム構成図テンプレート</cp:lastModifiedBy>"
        '<dcterms:created xsi:type="dcterms:W3CDTF">2026-10-06T00:00:00Z</dcterms:created>'
        '<dcterms:modified xsi:type="dcterms:W3CDTF">2026-10-06T00:00:00Z</dcterms:modified>'
        "</cp:coreProperties>"
    )
    titles = "".join(f"<vt:lpstr>{xe(sh.name)}</vt:lpstr>" for sh in sheets)
    files["docProps/app.xml"] = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        "<Application>Microsoft Excel</Application>"
        f"<TitlesOfParts><vt:vector size=\"{len(sheets)}\" baseType=\"lpstr\">{titles}</vt:vector></TitlesOfParts>"
        "</Properties>"
    )
    files["_rels/.rels"] = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
        "</Relationships>"
    )
    ct = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
    ]
    for part, ctype in overrides:
        ct.append(f'<Override PartName="{part}" ContentType="{ctype}"/>')
    ct.append("</Types>")
    files["[Content_Types].xml"] = "".join(ct)

    OUT_PUBLIC.parent.mkdir(parents=True, exist_ok=True)
    OUT_ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    for dest in (OUT_PUBLIC, OUT_ARTIFACT):
        with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as z:
            for name, data in files.items():
                z.writestr(name, data.encode("utf-8"))
    # well-formedness
    import xml.etree.ElementTree as ET

    with zipfile.ZipFile(OUT_PUBLIC) as z:
        for info in z.infolist():
            if info.filename.endswith(".xml") or info.filename.endswith(".rels"):
                ET.fromstring(z.read(info.filename))


def theme_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Sumi">
  <a:themeElements>
    <a:clrScheme name="Sumi">
      <a:dk1><a:srgbClr val="1C1C1C"/></a:dk1>
      <a:lt1><a:srgbClr val="F7F6F3"/></a:lt1>
      <a:dk2><a:srgbClr val="3A3A3A"/></a:dk2>
      <a:lt2><a:srgbClr val="E7E6E1"/></a:lt2>
      <a:accent1><a:srgbClr val="2A4668"/></a:accent1>
      <a:accent2><a:srgbClr val="7C3A3A"/></a:accent2>
      <a:accent3><a:srgbClr val="3C5644"/></a:accent3>
      <a:accent4><a:srgbClr val="7A5A2C"/></a:accent4>
      <a:accent5><a:srgbClr val="53425F"/></a:accent5>
      <a:accent6><a:srgbClr val="1F5C58"/></a:accent6>
      <a:hlink><a:srgbClr val="2A4668"/></a:hlink>
      <a:folHlink><a:srgbClr val="7C3A3A"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="Meiryo UI">
      <a:majorFont>
        <a:latin typeface="Meiryo UI"/>
        <a:ea typeface="Meiryo UI"/>
        <a:cs typeface="Meiryo UI"/>
      </a:majorFont>
      <a:minorFont>
        <a:latin typeface="Meiryo UI"/>
        <a:ea typeface="Meiryo UI"/>
        <a:cs typeface="Meiryo UI"/>
      </a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="Office">
      <a:fillStyleLst>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
      </a:fillStyleLst>
      <a:lnStyleLst>
        <a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
        <a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
        <a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
      </a:lnStyleLst>
      <a:effectStyleLst>
        <a:effectStyle><a:effectLst/></a:effectStyle>
        <a:effectStyle><a:effectLst/></a:effectStyle>
        <a:effectStyle><a:effectLst/></a:effectStyle>
      </a:effectStyleLst>
      <a:bgFillStyleLst>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
      </a:bgFillStyleLst>
    </a:fmtScheme>
  </a:themeElements>
</a:theme>
"""


if __name__ == "__main__":
    build_all()
