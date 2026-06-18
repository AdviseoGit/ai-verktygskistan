"""
AI-Verktygskistan lead magnet — "GDPR-checklista för AI-verktyg".

Deluxe, multi-section PDF (shared design language with the other portfolio
sites). fpdf2 core font = latin-1, which covers å/ä/ö; _s() keeps those and
only strips characters latin-1 cannot represent (em-dash, smart quotes, ...).
"""

BRAND = (5, 150, 105)     # emerald
BRAND_DK = (4, 108, 78)
INK = (28, 28, 30)
MUTED = (110, 110, 116)
LINE = (228, 228, 231)
WASH = (236, 253, 245)
RED = (190, 40, 40)

INTRO = ("AI ger enorm hävstång - men personuppgifter i fel verktyg kan bli dyrt. Den här "
         "checklistan tar er igenom det viktigaste för att använda AI produktivt OCH "
         "GDPR-säkert. Bocka av punkterna innan ni skalar upp.")

DO = [
    ("Innan ni inför ett AI-verktyg", [
        "Kartlägg vilka personuppgifter verktyget hanterar (kund, anställd, känslig data).",
        "Säkerställ rättslig grund (avtal, berättigat intresse, samtycke).",
        "Teckna personuppgiftsbiträdesavtal (DPA) med leverantören.",
        "Välj EU-/EES-lagring eller godkänd överföringsmekanism.",
    ]),
    ("Dokumentera", [
        "För in verktyget i behandlingsregistret med ändamål och rättslig grund.",
        "Beskriv tekniska och organisatoriska skyddsåtgärder.",
    ]),
    ("Riskbedöm", [
        "Gör en konsekvensbedömning (DPIA) vid hög risk - t.ex. profilering, känslig "
        "hälsodata eller automatiserade beslut om individer.",
    ]),
    ("Informera", [
        "Uppdatera integritetspolicyn med hur AI används.",
        "Informera anställda om ev. AI-bevakning (GDPR art. 13-14).",
    ]),
]
AVOID = [
    "Klistra in personnummer eller kunddata i ChatGPT Free / Gemini Basic.",
    "Använda gratisversioner utan DPA - de kan träna på era konversationer.",
    "Låta AI fatta beslut om individer utan mänsklig kontroll.",
]
CLOSING = ("Vill ni jämföra konkreta, GDPR-vänliga verktyg? Hela vår katalog finns på "
           "aiverktygsladan.se - uppdaterad löpande.")


def _s(t):
    t = str(t)
    for a, b in [("—", "-"), ("–", "-"), ("’", "'"), ("‘", "'"),
                 ("“", '"'), ("”", '"'), ("…", "..."), (" ", " ")]:
        t = t.replace(a, b)
    return t.encode("latin-1", "replace").decode("latin-1")


class DeluxeReport:
    MARGIN = 14
    WIDTH = 210 - 2 * 14

    def __init__(self, brand, brand_dk):
        from fpdf import FPDF
        self.brand, self.brand_dk = brand, brand_dk
        self.pdf = FPDF(format="A4")
        self.pdf.set_auto_page_break(auto=True, margin=20)
        self.pdf.set_margins(self.MARGIN, self.MARGIN, self.MARGIN)

    def cover(self, brandname, title, subtitle, intro):
        pdf = self.pdf
        pdf.add_page()
        pdf.set_fill_color(*self.brand)
        pdf.rect(0, 0, 210, 60, "F")
        pdf.set_fill_color(*self.brand_dk)
        pdf.rect(0, 56, 210, 4, "F")
        pdf.set_xy(14, 13)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 25)
        pdf.cell(0, 12, _s(brandname), ln=1)
        pdf.set_x(14)
        pdf.set_font("Helvetica", "", 14)
        pdf.cell(0, 8, _s(title), ln=1)
        pdf.set_x(14)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, _s(subtitle), ln=1)
        pdf.set_y(70)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*MUTED)
        pdf.multi_cell(self.WIDTH, 5, _s(intro))
        pdf.set_text_color(*INK)
        pdf.ln(2)

    def section(self, title, color=None):
        pdf = self.pdf
        if pdf.get_y() > 250:
            pdf.add_page()
        pdf.ln(2)
        y = pdf.get_y()
        pdf.set_fill_color(*(color or self.brand))
        pdf.rect(self.MARGIN, y, self.WIDTH, 9, "F")
        pdf.set_xy(self.MARGIN + 3, y + 1)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(self.WIDTH - 6, 7, _s(title), ln=1)
        pdf.set_text_color(*INK)
        pdf.ln(2)

    def checks(self, items, mark="box"):
        pdf = self.pdf
        for it in items:
            if pdf.get_y() > 262:
                pdf.add_page()
            y = pdf.get_y()
            if mark == "box":
                pdf.set_draw_color(*self.brand)
                pdf.rect(self.MARGIN + 1, y + 1.2, 4, 4)
            else:
                pdf.set_text_color(*RED)
                pdf.set_font("Helvetica", "B", 11)
                pdf.set_xy(self.MARGIN, y)
                pdf.cell(6, 5.5, "X")
                pdf.set_text_color(*INK)
            pdf.set_xy(self.MARGIN + 8, y)
            pdf.set_font("Helvetica", "", 10.5)
            pdf.multi_cell(self.WIDTH - 8, 5.5, _s(it))
            pdf.ln(1)

    def callout(self, text):
        pdf = self.pdf
        import math
        if pdf.get_y() > 250:
            pdf.add_page()
        pdf.ln(2)
        y = pdf.get_y()
        approx = max(1, math.ceil(pdf.get_string_width(_s(text)) / (self.WIDTH - 10)))
        h = approx * 5 + 8
        pdf.set_fill_color(*WASH)
        pdf.set_draw_color(*self.brand)
        pdf.rect(self.MARGIN, y, self.WIDTH, h, "DF")
        pdf.set_xy(self.MARGIN + 4, y + 3)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*INK)
        pdf.multi_cell(self.WIDTH - 8, 5, _s(text))
        pdf.set_y(y + h + 2)


def build_guide_pdf() -> bytes:
    r = DeluxeReport(BRAND, BRAND_DK)
    pdf = r.pdf

    def footer_fn():
        pdf.set_y(-15)
        pdf.set_draw_color(*LINE)
        pdf.line(r.MARGIN, pdf.get_y(), 210 - r.MARGIN, pdf.get_y())
        pdf.set_y(-13)
        pdf.set_font("Helvetica", "I", 7.5)
        pdf.set_text_color(*MUTED)
        pdf.cell(0, 4, _s("AI-Verktygskistan | aiverktygsladan.se | Allmän vägledning, inte "
                          "juridisk rådgivning. Stäm av med ert dataskyddsombud."), align="C")

    pdf.footer = footer_fn
    r.cover("AI-Verktygskistan", "GDPR-checklista för AI-verktyg",
            "Använd AI produktivt OCH säkert i företaget", INTRO)
    for title, items in DO:
        r.section(title)
        r.checks(items)
    r.section("Undvik dessa misstag", color=RED)
    r.checks(AVOID, mark="cross")
    r.callout(CLOSING)
    return bytes(pdf.output())


def user_email_html() -> str:
    return """\
<div style="font-family:Segoe UI,Arial,sans-serif;max-width:560px;margin:auto;color:#1c1c1e">
  <div style="background:#059669;color:#fff;padding:22px 24px;border-radius:12px 12px 0 0">
    <h2 style="margin:0;font-size:20px">Din GDPR-checklista för AI 🤖</h2>
  </div>
  <div style="border:1px solid #ececec;border-top:0;border-radius:0 0 12px 12px;padding:24px">
    <p>Hej, och tack!</p>
    <p>Här kommer din <b>GDPR-checklista för AI-verktyg</b> som <b>PDF i bilagan</b> — det vi
       använder själva för att införa AI produktivt och säkert i en verksamhet.</p>
    <p>Den tar dig igenom rättslig grund, biträdesavtal, behandlingsregister, DPIA och de
       vanligaste misstagen att undvika.</p>
    <p style="margin-top:22px">Lycka till!<br><b>AI-Verktygskistan</b><br>
       <a href="https://aiverktygsladan.se" style="color:#059669">aiverktygsladan.se</a></p>
    <p style="font-size:11px;color:#9a9a9a;margin-top:22px">Du får detta för att du anmälde dig på
       aiverktygsladan.se. Vill du av listan, svara på detta mejl.</p>
  </div>
</div>"""
