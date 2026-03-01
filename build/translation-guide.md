# ExKnowledge Translation Guide

## Source Files
English source: `/tmp/exknowledge/build/content/pages/`
Output: `/tmp/exknowledge/build/content/{LANG}/pages/`

## Pages (12 total)
1. fundamentals.html
2. zone-classification.html
3. gas-groups.html
4. temperature-classes.html
5. protection-methods.html (largest ~17K)
6. epl.html
7. ex-markings.html
8. standards.html
9. certification.html
10. installation-inspection.html
11. cheat-sheet.html
12. faq.html

## Sidebar Labels Per Language
### NO (Norwegian)
Grundleggende, Soner, Gassgrupper, Temperaturklasser, Beskyttelsesmetoder, EPL, Merkinger, Standarder, Sertifisering, Installasjon, Hurtigoversikt

### ES (Spanish)
Fundamentos, Zonas, Grupos de gas, Clases de temperatura, Métodos de protección, EPL, Marcas Ex, Normas, Certificación, Instalación, Guía rápida

### DA (Danish)
Grundlæggende, Zoner, Gasgrupper, Temperaturklasser, Beskyttelsesmetoder, EPL, Mærkninger, Standarder, Certificering, Installation, Hurtigoversigt

### SV (Swedish)
Grunder, Zoner, Gasgrupper, Temperaturklasser, Skyddsmetoder, EPL, Märkningar, Standarder, Certifiering, Installation, Snabböversikt

### FI (Finnish)
Perusteet, Vyöhykkeet, Kaasuryhmät, Lämpötilaluokat, Suojausmenetelmät, EPL, Merkinnät, Standardit, Sertifiointi, Asennus, Pikaohje

### NL (Dutch)
Basiskennis, Zones, Gasgroepen, Temperatuurklassen, Beschermingsmethoden, EPL, Markeringen, Normen, Certificering, Installatie, Snelgids

### PT (Portuguese)
Fundamentos, Zonas, Grupos de gás, Classes de temperatura, Métodos de proteção, EPL, Marcações Ex, Normas, Certificação, Instalação, Guia rápido

### IT (Italian)
Fondamenti, Zone, Gruppi gas, Classi di temperatura, Metodi di protezione, EPL, Marcature Ex, Norme, Certificazione, Installazione, Guida rapida

### AR (Arabic)
الأساسيات, المناطق, مجموعات الغاز, فئات الحرارة, طرق الحماية, EPL, علامات Ex, المعايير, الشهادات, التركيب, مرجع سريع

## Rules
1. Translate ALL body text to the target language
2. Keep ALL HTML structure, IDs, links, image URLs exactly as-is
3. Sidebar must use the translated labels above with `class="current"` on the current page
4. Sidebar h4 should be: "Alle Themen" / "Todos los temas" / etc.
5. Links in sidebar and related sections stay as English filenames (zone-classification.html etc.)
6. Technical terms (Ex d, IEC 60079, ATEX, IECEx, EPL, T1-T6, IIA/IIB/IIC) stay in original
7. Code blocks / pre elements: translate comments/labels only, keep technical content
8. After ALL 12 pages are written, run: cd /tmp/exknowledge && python3 build/build.py && git add -A && git commit -m "{LANG} translation complete" && git push origin main

## Git Auth
Repo: https://github.com/andreasbjornsund-hub/exknowledge.com.git
PAT already configured in git remote.

## Telegram Notification
After push, send status update to Andreas via Telegram (chatId 409006176).
