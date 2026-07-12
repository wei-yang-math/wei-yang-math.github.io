from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "wei-yang-cv.pdf"
PUBLIC_COPY = ROOT / "public" / "cv" / "wei-yang-cv.pdf"

PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT = 50
RIGHT = PAGE_WIDTH - 50
TEXT = HexColor("#202020")
MUTED = HexColor("#5f5b55")
ACCENT = HexColor("#365f55")
LINE = HexColor("#d8d2c8")


def register_fonts() -> None:
    font_dir = Path("C:/Windows/Fonts")
    pdfmetrics.registerFont(TTFont("TimesNewRoman", font_dir / "times.ttf"))
    pdfmetrics.registerFont(TTFont("TimesNewRoman-Bold", font_dir / "timesbd.ttf"))
    pdfmetrics.registerFont(TTFont("TimesNewRoman-Italic", font_dir / "timesi.ttf"))
    pdfmetrics.registerFont(TTFont("Arial", font_dir / "arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", font_dir / "arialbd.ttf"))


def draw_section(c: canvas.Canvas, title: str, y: float) -> float:
    c.setFillColor(ACCENT)
    c.setFont("Arial-Bold", 9.2)
    c.drawString(LEFT, y, title.upper())
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(LEFT + 96, y + 2.5, RIGHT, y + 2.5)
    return y - 21


def draw_entry_header(
    c: canvas.Canvas, left_text: str, right_text: str, y: float
) -> float:
    c.setFillColor(TEXT)
    c.setFont("TimesNewRoman-Bold", 10.7)
    c.drawString(LEFT, y, left_text)
    c.setFont("Arial", 8.8)
    c.setFillColor(MUTED)
    c.drawRightString(RIGHT, y + 0.5, right_text)
    return y - 15


def draw_wrapped(
    c: canvas.Canvas,
    text: str,
    y: float,
    *,
    font: str = "TimesNewRoman",
    size: float = 10.2,
    leading: float = 13.6,
    left: float = LEFT,
    max_width: float | None = None,
    color=TEXT,
) -> float:
    width = max_width if max_width is not None else RIGHT - left
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if pdfmetrics.stringWidth(candidate, font, size) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)

    c.setFillColor(color)
    c.setFont(font, size)
    for line in lines:
        c.drawString(left, y, line)
        y -= leading
    return y


def draw_note(
    c: canvas.Canvas, number: str, title: str, date: str, url: str, y: float
) -> float:
    c.setFillColor(MUTED)
    c.setFont("Arial", 8.8)
    c.drawString(LEFT, y, number)
    title_left = LEFT + 18
    y = draw_wrapped(
        c,
        title,
        y,
        font="TimesNewRoman-Italic",
        size=10.1,
        leading=13.4,
        left=title_left,
        max_width=RIGHT - title_left - 70,
    )
    c.setFillColor(MUTED)
    c.setFont("Arial", 8.6)
    c.drawRightString(RIGHT, y + 13.4, date)
    c.linkURL(url, (title_left, y + 10, RIGHT - 72, y + 24), relative=0)
    return y - 4


def build_cv() -> None:
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_COPY.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(OUTPUT), pagesize=A4)
    c.setTitle("Curriculum Vitae - Wei Yang")
    c.setAuthor("Wei Yang")
    c.setSubject("Academic curriculum vitae")

    y = PAGE_HEIGHT - 52
    c.setFillColor(TEXT)
    c.setFont("TimesNewRoman-Bold", 24)
    c.drawString(LEFT, y, "Wei Yang")

    c.setFillColor(MUTED)
    c.setFont("Arial", 9.2)
    c.drawRightString(RIGHT, y + 6, "Curriculum Vitae")
    y -= 20

    c.setStrokeColor(ACCENT)
    c.setLineWidth(1.2)
    c.line(LEFT, y, RIGHT, y)
    y -= 17

    c.setFillColor(MUTED)
    c.setFont("Arial", 8.8)
    c.drawString(LEFT, y, "School of Mathematical Sciences, Peking University")
    c.drawRightString(
        RIGHT, y, "2301110030 [at] stu [dot] pku [dot] edu [dot] cn"
    )
    y -= 14
    website = "https://wei-yang-math.github.io"
    c.setFillColor(ACCENT)
    c.drawRightString(RIGHT, y, website)
    website_width = pdfmetrics.stringWidth(website, "Arial", 8.8)
    c.linkURL(website, (RIGHT - website_width, y - 2, RIGHT, y + 9), relative=0)
    y -= 26

    y = draw_section(c, "Education", y)
    y = draw_entry_header(c, "Peking University", "Beijing, China | 2023-present", y)
    y = draw_wrapped(
        c,
        "Ph.D. student in Mathematics, School of Mathematical Sciences",
        y,
        size=10,
        color=MUTED,
    )
    y = draw_wrapped(
        c,
        "Advisor: Professor Ruochuan Liu",
        y + 1,
        font="TimesNewRoman-Italic",
        size=9.7,
        color=MUTED,
    )
    y -= 7

    y = draw_entry_header(
        c,
        "University of Science and Technology of China",
        "Hefei, China | 2019-2023",
        y,
    )
    y = draw_wrapped(
        c,
        "B.S. in Mathematics, School of the Gifted Young",
        y,
        size=10,
        color=MUTED,
    )
    y = draw_wrapped(
        c,
        "Undergraduate advisor: Professor Lei Zhang",
        y + 1,
        font="TimesNewRoman-Italic",
        size=9.7,
        color=MUTED,
    )
    y -= 14

    y = draw_section(c, "Research Interests", y)
    y = draw_wrapped(
        c,
        "Homotopy theory and arithmetic geometry, with particular interest in using techniques from arithmetic geometry to study problems in homotopy theory.",
        y,
        size=10.2,
        leading=14,
    )
    y -= 12

    y = draw_section(c, "Research Notes", y)
    y = draw_note(
        c,
        "1.",
        "Syntomic Tate Twists over p-adic Local Fields and the Cyclotomic Torsion Groups",
        "June 2026",
        "https://wei-yang-math.github.io/notes/syntomic-complexes-ok/syntomic-tate-twists-over-p-adic-local-fields/",
        y,
    )
    y = draw_note(
        c,
        "2.",
        "Semiorthogonal Decompositions of Perfect Complexes on Split Smooth Projective Toric Schemes over Z",
        "June 2026",
        "https://wei-yang-math.github.io/notes/toric-semiorthogonal-decompositions-over-z/",
        y,
    )
    y -= 10

    y = draw_section(c, "Teaching Experience", y)
    y = draw_entry_header(
        c, "Peking University", "Fall 2025 and Spring 2026", y
    )
    y = draw_wrapped(
        c,
        "Exercise Session Teaching Assistant, Advanced Algebra (Experimental Class)",
        y,
        size=10,
        color=MUTED,
    )

    c.setFillColor(MUTED)
    c.setFont("Arial", 7.8)
    c.drawString(LEFT, 31, "Updated July 2026")
    c.drawRightString(RIGHT, 31, "Wei Yang - Curriculum Vitae")

    c.save()
    PUBLIC_COPY.write_bytes(OUTPUT.read_bytes())


if __name__ == "__main__":
    build_cv()
