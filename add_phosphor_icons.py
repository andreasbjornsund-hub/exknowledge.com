#!/usr/bin/env python3
"""Add Phosphor Icons across all ExKnowledge HTML pages."""
import os
import re
import glob

BASE = '/tmp/exknowledge'

PHOSPHOR_CSS = '''  <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/regular/style.css">
  <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/bold/style.css">'''

# Find all HTML files
html_files = glob.glob(os.path.join(BASE, '**/*.html'), recursive=True)
# Exclude build/ and exscanner/
html_files = [f for f in html_files if '/build/' not in f and '/exscanner/' not in f]

print(f"Found {len(html_files)} HTML files")

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. Add Phosphor CSS links (after the style.css link, if not already present)
    if 'phosphor-icons' not in content:
        # Find the main stylesheet link
        content = re.sub(
            r'(<link rel="stylesheet" href="[^"]*style\.css">)',
            r'\1\n' + PHOSPHOR_CSS,
            content,
            count=1
        )
    
    # 2. Navigation icons - add before link text
    # Home variants
    for home_word in ['Home', 'Hjem', 'Startseite', 'Inicio', 'Hem', 'Accueil', 'Startpagina', 
                       'Início', 'Pagina iniziale', 'الرئيسية', 'Etusivu', 'Forside', 'Hjem']:
        content = content.replace(
            f'>{home_word}</a>',
            f'><i class="ph ph-house"></i> {home_word}</a>'
        )
    
    # Fundamentals variants
    for word in ['Fundamentals', 'Grunnleggende', 'Grundlagen', 'Fundamentos', 'Grunder',
                 'Fondamentaux', 'Basisprincipes', 'Fundamentos', 'Fondamenti', 'الأساسيات',
                 'Perusteet', 'Grundlæggende']:
        content = content.replace(
            f'>{word}</a>',
            f'><i class="ph ph-fire"></i> {word}</a>'
        )
    
    # Protection variants
    for word in ['Protection', 'Beskyttelse', 'Schutz', 'Protección', 'Skydd',
                 'Protection', 'Bescherming', 'Proteção', 'Protezione', 'الحماية',
                 'Suojaus', 'Beskyttelse']:
        content = content.replace(
            f'>{word}</a>',
            f'><i class="ph ph-shield-check"></i> {word}</a>'
        )
    
    # Blog variants 
    for word in ['Blog', 'Blogg', 'Blog', 'Blog']:
        content = content.replace(
            f'>{word}</a>',
            f'><i class="ph ph-newspaper"></i> {word}</a>'
        )
    
    # Standards variants
    for word in ['Standards', 'Standarder', 'Normen', 'Normas', 'Standarder',
                 'Normes', 'Normen', 'Normas', 'Standard', 'المعايير',
                 'Standardit', 'Standarder']:
        content = content.replace(
            f'>{word}</a>',
            f'><i class="ph ph-book-open"></i> {word}</a>'
        )
    
    # Zones variants  
    for word in ['Zones', 'Soner', 'Zonen', 'Zonas', 'Zoner',
                 'Zones', 'Zones', 'Zonas', 'Zone', 'المناطق',
                 'Vyöhykkeet', 'Zoner']:
        content = content.replace(
            f'>{word}</a>',
            f'><i class="ph ph-map-trifold"></i> {word}</a>'
        )
    
    # Cheat Sheet variants
    for word in ['Cheat Sheet', 'Jukseark', 'Spickzettel', 'Hoja de referencia', 'Fuskark',
                 'Aide-mémoire', 'Spiekbrief', 'Folha de referência', 'Foglio informativo',
                 'ورقة مرجعية', 'Lunttilappu', 'Snyderi']:
        content = content.replace(
            f'>{word}</a>',
            f'><i class="ph ph-lightning"></i> {word}</a>'
        )
    
    # 3. Hamburger menu - replace burger div lines with icon
    # Pattern 1: div-based burger
    content = re.sub(
        r'<div class="burger" aria-label="Menu">\s*'
        r'<div class="line1"></div>\s*'
        r'<div class="line2"></div>\s*'
        r'<div class="line3"></div>\s*'
        r'</div>',
        '<div class="burger" aria-label="Menu">\n      <i class="ph-bold ph-list"></i>\n    </div>',
        content
    )
    # Pattern 2: button-based nav-toggle with spans
    content = re.sub(
        r'<button class="nav-toggle" aria-label="Menu"([^>]*)>\s*'
        r'<span></span><span></span><span></span>\s*'
        r'</button>',
        r'<button class="nav-toggle" aria-label="Menu"\1>\n      <i class="ph-bold ph-list"></i>\n    </button>',
        content
    )
    
    # 4. Search button - replace emoji
    content = content.replace(
        '<button class="hero-search-btn" aria-label="Search">🔍</button>',
        '<button class="hero-search-btn" aria-label="Search"><i class="ph ph-magnifying-glass"></i></button>'
    )
    
    # 5. Breadcrumb separators - replace <span>/</span> within breadcrumb
    # Only replace / spans that are inside breadcrumb nav
    def replace_breadcrumb_separators(match):
        bc = match.group(0)
        bc = bc.replace('<span>/</span>', '<i class="ph ph-caret-right" style="font-size:12px;opacity:0.5"></i>')
        return bc
    
    content = re.sub(
        r'<nav class="breadcrumb"[^>]*>.*?</nav>',
        replace_breadcrumb_separators,
        content,
        flags=re.DOTALL
    )
    
    # 6. Sidebar headings
    content = content.replace(
        '<h4>All Issues</h4>',
        '<h4><i class="ph ph-archive"></i> All Issues</h4>'
    )
    content = content.replace(
        '<h4>All Topics</h4>',
        '<h4><i class="ph ph-list-bullets"></i> All Topics</h4>'
    )
    # Translated sidebar headings
    sidebar_issues = {
        'Alle utgaver': 'archive', 'Alle Ausgaben': 'archive', 'Todos los números': 'archive',
        'Alla nummer': 'archive', 'Tous les numéros': 'archive', 'Alle uitgaven': 'archive',
        'Todas as edições': 'archive', 'Tutti i numeri': 'archive', 'جميع الأعداد': 'archive',
        'Kaikki numerot': 'archive', 'Alle numre': 'archive',
    }
    sidebar_topics = {
        'Alle emner': 'list-bullets', 'Alle Themen': 'list-bullets', 'Todos los temas': 'list-bullets',
        'Alla ämnen': 'list-bullets', 'Tous les sujets': 'list-bullets', 'Alle onderwerpen': 'list-bullets',
        'Todos os temas': 'list-bullets', 'Tutti gli argomenti': 'list-bullets', 'جميع المواضيع': 'list-bullets',
        'Kaikki aiheet': 'list-bullets', 'Alle emner': 'list-bullets',
    }
    for text, icon in {**sidebar_issues, **sidebar_topics}.items():
        content = content.replace(
            f'<h4>{text}</h4>',
            f'<h4><i class="ph ph-{icon}"></i> {text}</h4>'
        )
    
    # 7. Footer - add icon before ExKnowledge in footer
    # Various footer patterns
    content = content.replace(
        '<p>ExKnowledge — Built from field experience.</p>',
        '<p><i class="ph ph-lightning" style="color:var(--accent)"></i> ExKnowledge — Built from field experience.</p>'
    )
    content = re.sub(
        r'(<footer class="footer">.*?<p>)(Built for engineers)',
        r'\1<i class="ph ph-lightning" style="color:var(--accent)"></i> Built for engineers',
        content,
        flags=re.DOTALL
    )
    # Translated footer patterns
    footer_patterns = [
        'ExKnowledge — Bygget fra felterfaring.',
        'ExKnowledge — Aus Felderfahrung gebaut.',
        'ExKnowledge — Construido desde experiencia de campo.',
        'ExKnowledge — Byggt från fälterfarenhet.',
        'ExKnowledge — Construit à partir de l\'expérience de terrain.',
        'ExKnowledge — Gebouwd vanuit veldervaring.',
        'ExKnowledge — Construído a partir de experiência de campo.',
        'ExKnowledge — Costruito dall\'esperienza sul campo.',
        'ExKnowledge — مبني من تجربة ميدانية.',
        'ExKnowledge — Rakennettu kenttäkokemuksesta.',
        'ExKnowledge — Bygget ud fra felterfaring.',
    ]
    for fp in footer_patterns:
        content = content.replace(
            f'<p>{fp}</p>',
            f'<p><i class="ph ph-lightning" style="color:var(--accent)"></i> {fp}</p>'
        )
    
    # 8. Topic cards - add icons to topic cards on homepage
    # Map topic h3 text to icons (English + translations)
    topic_icon_map = {
        # English
        'Fundamentals': 'fire', 'Zone Classification': 'map-trifold', 'Gas Groups': 'flask',
        'Temperature Classes': 'thermometer-hot', 'Protection Methods': 'shield-check',
        'Equipment Protection Levels': 'gauge', 'Reading Ex Markings': 'tag',
        'Standards': 'book-open', 'Certification': 'certificate',
        'Installation & Inspection': 'wrench', 'Cheat Sheet': 'lightning',
        # Norwegian
        'Grunnleggende': 'fire', 'Soneklassifisering': 'map-trifold', 'Gassgrupper': 'flask',
        'Temperaturklasser': 'thermometer-hot', 'Beskyttelsesmetoder': 'shield-check',
        'Utstyrsbeskyttelsesnivåer': 'gauge', 'Leser eks-merker': 'tag', 'Lese Ex-merkinger': 'tag',
        'Standarder': 'book-open', 'Sertifisering': 'certificate',
        'Installasjon og inspeksjon': 'wrench', 'Jukseark': 'lightning',
        # German
        'Grundlagen': 'fire', 'Zonenklassifizierung': 'map-trifold', 'Gasgruppen': 'flask',
        'Temperaturklassen': 'thermometer-hot', 'Schutzarten': 'shield-check',
        'Geräteschutzniveaus': 'gauge', 'Ex-Kennzeichnung lesen': 'tag',
        'Normen': 'book-open', 'Zertifizierung': 'certificate',
        'Installation und Inspektion': 'wrench', 'Spickzettel': 'lightning',
        # Spanish
        'Fundamentos': 'fire', 'Clasificación de zonas': 'map-trifold', 'Grupos de gas': 'flask',
        'Clases de temperatura': 'thermometer-hot', 'Métodos de protección': 'shield-check',
        'Niveles de protección de equipos': 'gauge', 'Lectura de marcas Ex': 'tag',
        'Normas': 'book-open', 'Certificación': 'certificate',
        'Instalación e inspección': 'wrench', 'Hoja de referencia': 'lightning',
        # Swedish
        'Grunder': 'fire', 'Zonklassificering': 'map-trifold', 'Gasgrupper': 'flask',
        'Temperaturklasser': 'thermometer-hot', 'Skyddsmetoder': 'shield-check',
        'Utrustningsskyddsnivåer': 'gauge', 'Läsa Ex-märkningar': 'tag',
        'Standarder': 'book-open', 'Certifiering': 'certificate',
        'Installation och inspektion': 'wrench', 'Fuskark': 'lightning',
        # Danish
        'Grundlæggende': 'fire', 'Zoneklassificering': 'map-trifold', 'Gasgrupper': 'flask',
        'Temperaturklasser': 'thermometer-hot', 'Beskyttelsesmetoder': 'shield-check',
        'Udstyrsbeskyttelsesniveauer': 'gauge', 'Læsning af Ex-mærkninger': 'tag',
        'Standarder': 'book-open', 'Certificering': 'certificate',
        'Installation og inspektion': 'wrench', 'Snyderi': 'lightning',
        # Finnish
        'Perusteet': 'fire', 'Vyöhykeluokitus': 'map-trifold', 'Kaasuryhmät': 'flask',
        'Lämpötilaluokat': 'thermometer-hot', 'Suojausmenetelmät': 'shield-check',
        'Laitteiden suojaustasot': 'gauge', 'Ex-merkintöjen lukeminen': 'tag',
        'Standardit': 'book-open', 'Sertifiointi': 'certificate',
        'Asennus ja tarkastus': 'wrench', 'Lunttilappu': 'lightning',
        # Dutch
        'Basisprincipes': 'fire', 'Zoneclassificatie': 'map-trifold', 'Gasgroepen': 'flask',
        'Temperatuurklassen': 'thermometer-hot', 'Beschermingsmethoden': 'shield-check',
        'Beschermingsniveaus voor apparatuur': 'gauge', 'Ex-markeringen lezen': 'tag',
        'Normen': 'book-open', 'Certificering': 'certificate',
        'Installatie en inspectie': 'wrench', 'Spiekbrief': 'lightning',
        # Portuguese
        'Fundamentos': 'fire', 'Classificação de zonas': 'map-trifold', 'Grupos de gás': 'flask',
        'Classes de temperatura': 'thermometer-hot', 'Métodos de proteção': 'shield-check',
        'Níveis de proteção de equipamentos': 'gauge', 'Leitura de marcações Ex': 'tag',
        'Normas': 'book-open', 'Certificação': 'certificate',
        'Instalação e inspeção': 'wrench', 'Folha de referência': 'lightning',
        # Italian
        'Fondamenti': 'fire', 'Classificazione delle zone': 'map-trifold', 'Gruppi di gas': 'flask',
        'Classi di temperatura': 'thermometer-hot', 'Metodi di protezione': 'shield-check',
        'Livelli di protezione delle apparecchiature': 'gauge', 'Leggere le marcature Ex': 'tag',
        'Standard': 'book-open', 'Certificazione': 'certificate',
        'Installazione e ispezione': 'wrench', 'Foglio informativo': 'lightning',
        # Arabic
        'الأساسيات': 'fire', 'تصنيف المناطق': 'map-trifold', 'مجموعات الغاز': 'flask',
        'فئات درجة الحرارة': 'thermometer-hot', 'طرق الحماية': 'shield-check',
        'مستويات حماية المعدات': 'gauge', 'قراءة علامات Ex': 'tag',
        'المعايير': 'book-open', 'الشهادة': 'certificate',
        'التركيب والفحص': 'wrench', 'ورقة مرجعية': 'lightning',
    }
    
    # Only add icons to topic cards (within topic-card links)
    for title, icon in topic_icon_map.items():
        # Match topic card h3 without existing icon
        old = f'<h3>{title}</h3>'
        new = f'<i class="ph ph-{icon}"></i>\n        <h3>{title}</h3>'
        # Only replace within topic-card context (check if topic-card appears before)
        content = content.replace(old, new)
    
    # Prevent double icons (if run twice)
    content = re.sub(r'(<i class="ph ph-[^"]+"></i>\s*){2,}(<h3>)', r'\1\2', content)
    content = re.sub(r'(<i class="ph ph-[^"]+"></i> ){2,}', r'\1', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Updated: {filepath}")

print("\nDone! Updated all HTML files.")
