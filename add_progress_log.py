import datetime

log_file = "/data/workspace/projects/ai-verktygskistan/PROGRESS_LOG.md"
date_str = datetime.datetime.now().strftime("%Y-%m-%d")

new_entry = f"{date_str} | TILLVÄXT/DATA | Lade till Gamma, ElevenLabs och Suno AI i katalogen | Katalog 38->41, breddar content-skapar intent | nästa: Fånga mer sökintent med ny sida eller verktyg\n"

with open(log_file, "r") as f:
    lines = f.readlines()

with open(log_file, "w") as f:
    f.write(new_entry)
    for line in lines:
        f.write(line)
print("Updated PROGRESS_LOG.md")
