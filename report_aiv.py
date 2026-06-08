"""
AI-Verktygskistan lead magnet — "GDPR-checklista for AI-verktyg".
Matches the site's AI-tools + GDPR-compliance content. Static PDF + email body.
fpdf2 core font = latin-1 (a/a/o ok; avoid em-dash/smart quotes -> _s()).
"""

GREEN = (5, 150, 105)
INK = (28, 28, 30)
MUTED = (110, 110, 116)
RED = (190, 40, 40)

DO = [
    ("Innan ni infor ett AI-verktyg", [
        "Kartlagg vilka personuppgifter verktyget hanterar (kund, anstalld, kanslig data).",
        "Sakerstall rattslig grund (avtal, berattigat intresse, samtycke).",
        "Teckna personuppgiftsbitradesavtal (DPA) med leverantoren.",
        "Valj EU-/EES-lagring eller godkand overforingsmekanism.",
    ]),
    ("Dokumentera", [
        "For in verktyget i behandlingsregistret med andamal och rattslig grund.",
        "Beskriv tekniska och organisatoriska skyddsatgarder.",
    ]),
    ("Riskbedom", [
        "Gor en konsekvensbedomning (DPIA) vid hog risk - t.ex. profilering, "
        "kanslig halsodata eller automatiserade beslut om individer.",
    ]),
    ("Informera", [
        "Uppdatera integritetspolicyn med hur AI anvands.",
        "Informera anstallda om ev. AI-bevakning (GDPR art. 13-14).",
    ]),
]
AVOID = [
    "Klistra in personnummer eller kunddata i ChatGPT Free / Gemini Basic.",
    "Anvanda gratisversioner utan DPA - de kan trana pa era konversationer.",
    "Lata AI fatta beslut om individer utan mansklig kontroll.",
]


def _s(t):
    t = str(t)
    for a, b in [("—", "-"), ("–", "-"), ("’", "'"), ("‘", "'"),
                 ("“", '"'), ("”", '"'), ("…", "..."), (" ", " ")]:
        t = t.replace(a, b)
    return t.encode("latin-1", "replace").decode("latin-1")


def build_guide_pdf() -> bytes:
    from fpdf import FPDF
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.add_page()

    pdf.set_fill_color(*GREEN)
    pdf.rect(0, 0, 210, 30, "F")
    pdf.set_xy(14, 9)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "AI-Verktygskistan", ln=1)
    pdf.set_xy(14, 19)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, _s("GDPR-checklista for AI-verktyg i foretag"), ln=1)

    pdf.set_xy(14, 38)
    pdf.set_text_color(*MUTED)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(182, 5, _s(
        "AI ger enorm havstang - men personuppgifter i fel verktyg kan bli dyrt. "
        "Den har checklistan tar er igenom det viktigaste for att anvanda AI "
        "produktivt OCH GDPR-sakert. Bocka av punkterna innan ni skalar upp."))
    pdf.ln(2)

    for title, items in DO:
        pdf.set_text_color(*GREEN)
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 9, _s(title), ln=1)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(*INK)
        for it in items:
            y = pdf.get_y()
            pdf.set_draw_color(*MUTED)
            pdf.rect(15, y + 1.2, 3.5, 3.5)
            pdf.set_x(22)
            pdf.multi_cell(173, 6, _s(it))
        pdf.ln(2)

    pdf.set_text_color(*RED)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 9, _s("Undvik dessa misstag"), ln=1)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(*INK)
    for it in AVOID:
        y = pdf.get_y()
        pdf.set_text_color(*RED)
        pdf.set_xy(15, y)
        pdf.cell(5, 6, "X")
        pdf.set_text_color(*INK)
        pdf.set_x(22)
        pdf.multi_cell(173, 6, _s(it))
    pdf.ln(2)

    pdf.set_y(-18)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(182, 4, _s("AI-Verktygskistan | aiverktygsladan.se | Allman vagledning, "
                              "inte juridisk radgivning. Stam av med ert dataskyddsombud."))
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
