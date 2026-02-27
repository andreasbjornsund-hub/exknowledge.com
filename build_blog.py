#!/usr/bin/env python3
"""Build blog HTML pages."""
import os

BLOG_DIR = "/tmp/exknowledge/blog"

BLOG_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{seo_title}</title>
  <meta name="description" content="{meta_desc}">
  <link rel="canonical" href="https://exknowledge.com/blog/{filename}">
  <meta property="og:title" content="{seo_title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:url" content="https://exknowledge.com/blog/{filename}">
  <meta property="og:type" content="article">
  <meta property="og:image" content="{hero_img}">
  <meta property="article:published_time" content="{iso_date}">
  <link rel="stylesheet" href="../css/style.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚡</text></svg>">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{h1}",
    "description": "{meta_desc}",
    "url": "https://exknowledge.com/blog/{filename}",
    "datePublished": "{iso_date}",
    "image": "{hero_img}",
    "author": {{ "@type": "Organization", "name": "ExKnowledge" }},
    "publisher": {{ "@type": "Organization", "name": "ExKnowledge", "url": "https://exknowledge.com" }}
  }}
  </script>
</head>
<body>

<nav class="nav">
  <div class="container">
    <a href="../" class="nav-logo">Ex<span>Knowledge</span></a>
    <button class="nav-toggle" aria-label="Menu" onclick="this.classList.toggle('open');document.querySelector('.nav-links').classList.toggle('open')">
      <span></span><span></span><span></span>
    </button>
    <ul class="nav-links">
      <li><a href="../">Home</a></li>
      <li><a href="../pages/fundamentals.html">Fundamentals</a></li>
      <li><a href="../pages/protection-methods.html">Protection</a></li>
      <li><a href="index.html" class="active">Blog</a></li>
    </ul>
  </div>
</nav>

<section class="content-page">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../">Home</a> <span>/</span> <a href="index.html">Blog</a> <span>/</span> <span>{date_label}</span>
    </nav>
    <div class="content-layout">
      <article class="content-body">
        <img class="content-hero" src="{hero_img}" alt="{h1}" loading="lazy" width="820" height="240">
        <p style="font-size:13px;color:var(--accent);font-weight:600;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">{date_label}</p>
        <h1>{h1}</h1>
        {content}
      </article>
      <aside class="content-sidebar" aria-label="More posts">
        <div class="sidebar-card">
          <h4>All Issues</h4>
          {sidebar_links}
        </div>
      </aside>
    </div>
  </div>
</section>

<footer class="footer">
  <div class="container">
    <p>ExKnowledge — Built from field experience.</p>
    <p style="margin-top:8px">© 2026 ExKnowledge.com</p>
  </div>
</footer>

<script>
document.querySelectorAll('.nav-links a').forEach(a => a.addEventListener('click', () => {{
  document.querySelector('.nav-toggle')?.classList.remove('open');
  document.querySelector('.nav-links')?.classList.remove('open');
}}));
</script>
</body>
</html>"""

POSTS = [
    {
        "filename": "2025-11.html",
        "seo_title": "Ex Industry Monthly: November 2025 — Robotics, Dust Hazards, UK Standards",
        "meta_desc": "November 2025 Ex industry news: explosion-proof robotics, Imperial Sugar dust explosion lessons, UK ATEX standards update, AI cameras in hazardous areas.",
        "h1": "Explosion-Proof Robotics, Food Industry Dust Hazards, and UK Standards Update",
        "date_label": "November 2025",
        "iso_date": "2025-11-28",
        "hero_img": "https://images.unsplash.com/photo-1513828583688-c52646db42da?w=1000&q=80",
        "content": """
<h2 id="robotics">ATEX-Certified Robotics Are Getting Real</h2>
<p>The push for automation in hazardous areas took a meaningful step forward in November. Several manufacturers are now testing robotic inspection platforms that carry ATEX Zone 1 or IECEx ratings, aimed at refineries and offshore platforms where sending people into confined spaces is both expensive and dangerous.</p>
<p>The challenge remains certification. Getting a robot through ATEX testing means every motor, sensor, battery, and communication module needs to meet <a href="../pages/protection-methods.html">Ex protection requirements</a> individually. Most current designs rely on <a href="../pages/protection-methods.html#ex-i--intrinsic-safety-iec-60079-11">Ex i</a> for sensors and <a href="../pages/protection-methods.html#ex-d--flameproof-enclosure-iec-60079-1">Ex d</a> for drive motors, which adds weight and limits battery life.</p>
<p><em>Source: <a href="https://newsgab.com/advancements-in-explosion-proof-robotics-for-atex-iecex-environments/" target="_blank" rel="noopener">Newsgab, Nov 15 2025</a></em></p>

<h2 id="dust">Imperial Sugar Revisited: Dust Explosions in Food Processing</h2>
<p>Cobic B.V. published a detailed analysis of how the 2008 Imperial Sugar dust explosion — which killed 14 workers in Port Wentworth, Georgia — remains relevant today. The root cause was straightforward: sugar dust accumulation, poor housekeeping, and inadequate <a href="../pages/zone-classification.html">zone classification</a> for combustible dust areas.</p>
<p>What makes the article worth reading is the emphasis on how many food processing facilities still don't classify their dust zones correctly. <a href="../pages/fundamentals.html">Dust explosions</a> require particles under 500 μm to stay airborne, and sugar, flour, and grain all qualify. The article argues that ATEX Zone 20/21/22 classification is often skipped entirely in older food plants.</p>
<p><em>Source: <a href="https://foodindustryexecutive.com/2025/11/explosion-safety-in-food-processing-why-a-preventable-disaster-remains-relevant/" target="_blank" rel="noopener">Food Industry Executive, Nov 1 2025</a></em></p>

<h2 id="uk-standards">UK Government Updates Designated ATEX Standards List</h2>
<p>The UK's Department for Business and Trade published an updated consolidated list of designated standards for equipment intended for use in explosive atmospheres. Post-Brexit, the UK maintains its own list (separate from the EU's harmonised standards) under the Supply of Machinery (Safety) Regulations.</p>
<p>For manufacturers selling into both markets, the practical impact is ongoing dual compliance. Most IEC 60079 standards are listed by both the EU and UK, but the administrative overhead of maintaining both UKCA and CE marking continues to frustrate smaller Ex equipment makers.</p>
<p><em>Source: <a href="https://www.gov.uk/government/publications/designated-standards-atex" target="_blank" rel="noopener">GOV.UK, Nov 18 2025</a></em></p>

<h2 id="market">Ex Equipment Market: $12.5 Billion and Growing</h2>
<p>Market analysts project the intelligent explosion-proof communication equipment segment alone will reach $12.5 billion by 2033, growing at 7.8% CAGR. The broader explosion-proof equipment market continues to be driven by LNG expansion in the Middle East, hydrogen projects in Europe, and ongoing petrochemical investment in Asia.</p>
<p>Key players named across multiple reports: ABB, Siemens, Eaton, Emerson, Pepperl+Fuchs, BARTEC, R. Stahl, Honeywell, Schneider Electric, and Hubbell.</p>
<p><em>Source: <a href="https://www.openpr.com/news/4282542/explosion-proof-equipment-market-size-trends-2032-by-key" target="_blank" rel="noopener">OpenPR, Nov 21 2025</a></em></p>

<h2 id="ai-cameras">AI Cameras Enter ATEX-Certified Environments</h2>
<p>Machine learning-enabled surveillance cameras are being certified for ATEX and IECEx environments. The use case is predictive maintenance and safety monitoring — detecting gas leaks visually, tracking worker positions in confined spaces, and identifying equipment anomalies before they become incidents.</p>
<p>The cameras themselves typically carry <a href="../pages/protection-methods.html#ex-d--flameproof-enclosure-iec-60079-1">Ex d</a> or <a href="../pages/protection-methods.html#ex-e--increased-safety-iec-60079-7">Ex e</a> housings, with edge computing done outside the hazardous zone. The interesting part is what happens when the AI processing needs to happen on-device, inside the zone, which pushes the boundaries of what <a href="../pages/epl.html">EPL Gb</a> rated equipment can do with limited power budgets.</p>

<h2 id="events">Events This Month</h2>
<ul>
<li><strong>Pepperl+Fuchs</strong> announced as sponsor for NAMUR-Hauptsitzung 2026, the annual meeting of Germany's process industry user association</li>
<li><strong>EPIT Group</strong> launched new Ex awareness training courses aimed at electrical and mechanical personnel in hazardous areas</li>
</ul>
"""
    },
    {
        "filename": "2025-12.html",
        "seo_title": "Ex Industry Monthly: December 2025 — BARTEC Acquisition, SPS, Market Forecasts",
        "meta_desc": "December 2025 Ex industry news: One Equity Partners acquires BARTEC, R. Stahl at SPS Nuremberg with Ethernet-APL, flameproof market hits $15B, BARTEC SP9EX1.",
        "h1": "BARTEC Acquired by One Equity Partners, SPS 2025, and Market Growth",
        "date_label": "December 2025",
        "iso_date": "2025-12-28",
        "hero_img": "https://images.unsplash.com/photo-1545259741-2ea3ebf61fa3?w=1000&q=80",
        "content": """
<h2 id="bartec">One Equity Partners Acquires BARTEC</h2>
<p>The biggest company news this quarter: One Equity Partners (OEP) completed its acquisition of BARTEC from Bridgepoint Credit and Alcentra. BARTEC, based in Bad Mergentheim, Germany, is one of the world's leading manufacturers of Ex equipment — from intrinsically safe smartphones and tablets to complete automation solutions for hazardous areas.</p>
<p>The acquisition signals continued private equity interest in the explosion protection sector. BARTEC had been through several ownership changes in recent years, and OEP's track record suggests they'll focus on operational efficiency and bolt-on acquisitions. For customers, the practical question is whether this leads to more R&D investment or more cost-cutting.</p>
<p><em>Source: <a href="https://tracxn.com/d/acquisitions/acquisitions-by-one-equity-partners/__qwQlfNp80LUWUkhXKvQ3mojSelzQFD6NnLnvYfnxFIM" target="_blank" rel="noopener">Tracxn, Aug 29 2025</a></em></p>

<h2 id="bartec-sp9">BARTEC Launches SP9EX1: 5G in Zone 1</h2>
<p>On the product side, BARTEC released the SP9EX1 — billed as the world's most compact 5G smartphone certified for Zone 1/21 and Division 1 hazardous areas. It runs Android 15, has a 6.1" AMOLED display, and packs a 48 MP camera. The certification covers <a href="../pages/gas-groups.html">gas group IIC</a> and <a href="../pages/temperature-classes.html">temperature class T4</a>.</p>
<p>5G connectivity in Zone 1 is a genuine step forward. Previous ATEX smartphones were stuck on 4G, which limited their usefulness for real-time video streaming, remote expert assistance, and IoT data collection in the field.</p>
<p><em>Source: <a href="https://intrinsicallysafestore.com/product/bartec-sp9ex1-explosion-proof-5g-smartphone/" target="_blank" rel="noopener">Intrinsically Safe Store, Dec 5 2025</a></em></p>

<h2 id="sps">R. Stahl at SPS 2025: Ethernet-APL in Hazardous Areas</h2>
<p>SPS 2025 in Nuremberg — Europe's main industrial automation trade fair — saw R. Stahl push hard on Ethernet-APL (Advanced Physical Layer). Their pitch: a single Ethernet cable delivering both power and data to field devices in <a href="../pages/zone-classification.html">Zone 1</a> and even Zone 0, replacing the tangle of 4-20 mA analog loops and HART protocols that have dominated process plants for decades.</p>
<p>The Ethernet-APL field switch is the key piece. It converts standard Ethernet to the 2-wire, intrinsically safe connection that can reach instruments in hazardous areas. R. Stahl's selling point is that their switch is the "safest bet" — purpose-built for Ex, not adapted from a general industrial product.</p>
<p><em>Source: <a href="https://www.youtube.com/watch?v=KRb9OW0Ag8k" target="_blank" rel="noopener">R. Stahl YouTube, Dec 11 2025</a></em></p>

<h2 id="market">Flameproof Equipment Market: $15 Billion by 2034</h2>
<p>The global flameproof equipment market — the <a href="../pages/protection-methods.html#ex-d--flameproof-enclosure-iec-60079-1">Ex d</a> segment specifically — is projected to exceed $15 billion by 2034. Growth drivers: LNG terminal construction in the Middle East, hydrogen infrastructure in Europe, and tightening safety standards in Southeast Asia.</p>
<p>Saudi Arabia alone is expected to grow at 7.5% CAGR through 2033, driven by Vision 2030 petrochemical expansions and NEOM-related hydrogen projects.</p>
<p><em>Source: <a href="https://www.openpr.com/news/4315412/flameproof-equipment-market-projected-to-exceed-usd-15-billion" target="_blank" rel="noopener">OpenPR, Dec 15 2025</a></em></p>

<h2 id="events">Events & Milestones</h2>
<ul>
<li><strong>SPS 2025</strong> (Nov 25-27, Nuremberg): Major Ex equipment suppliers present including R. Stahl, Pepperl+Fuchs, Eaton, Turck</li>
<li><strong>Hazardous Area Equipment Market Report</strong> published by SkyQuest, naming 12 major players across the $8.2B global market</li>
<li><strong>UK ATEX designated standards</strong> list updated for Q4 2025 — no significant additions but confirms ongoing dual EU/UK compliance requirements</li>
</ul>
"""
    },
    {
        "filename": "2026-01.html",
        "seo_title": "Ex Industry Monthly: January 2026 — R. Stahl 150 Years, Hydrogen ATEX Gaps, Chemical Outlook",
        "meta_desc": "January 2026 Ex industry news: R. Stahl celebrates 150 years, hydrogen exposes ATEX concept gaps, 2026 chemical sector outlook, Zone 1 LED lighting projects.",
        "h1": "R. Stahl Turns 150, Hydrogen ATEX Gaps, and the Chemical Sector Outlook",
        "date_label": "January 2026",
        "iso_date": "2026-01-28",
        "hero_img": "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=1000&q=80",
        "content": """
<h2 id="rstahl-150">R. Stahl Celebrates 150 Years</h2>
<p>2026 marks 150 years for R. Stahl, making it one of the oldest companies in the explosion protection industry. Founded in 1876 in Künzelsau, Germany, the company has been through the entire arc of the industry — from early mining lamp safety to today's Ethernet-APL field switches and <a href="../pages/protection-methods.html#ex-i--intrinsic-safety-iec-60079-11">intrinsically safe</a> remote I/O systems.</p>
<p>The anniversary comes at an interesting time. R. Stahl's recent financials show weak demand in 2025, and the company is balancing tradition with a need to modernize. But 150 years of continuous operation in a niche where mistakes kill people is worth acknowledging.</p>
<p><em>Source: <a href="https://de.linkedin.com/in/marco-suleder-623a891a8/en" target="_blank" rel="noopener">R. Stahl LinkedIn, Jan 27 2026</a></em></p>

<h2 id="hydrogen-atex">Hydrogen Exposes Gaps in Existing ATEX Concepts</h2>
<p>ATEXshop.de published a technical article that deserves wide readership: existing ATEX protection concepts designed for methane or propane often fall short when applied to hydrogen. The reason is physics.</p>
<p>Hydrogen has a minimum ignition energy of just 0.017 mJ (versus 0.28 mJ for methane), an explosive range of <a href="../pages/fundamentals.html">4-77% by volume</a>, and falls into <a href="../pages/gas-groups.html">gas group IIC</a> — the highest risk category. Flame paths in <a href="../pages/protection-methods.html#ex-d--flameproof-enclosure-iec-60079-1">Ex d enclosures</a> need to be tighter, <a href="../pages/protection-methods.html#ex-i--intrinsic-safety-iec-60079-11">Ex i circuits</a> need lower energy limits, and <a href="../pages/zone-classification.html">zone extents</a> are larger because hydrogen disperses faster and further than heavier gases.</p>
<p>As green hydrogen projects multiply across Europe, this is becoming a pressing practical problem. Facilities designed for natural gas cannot simply swap in hydrogen without re-evaluating every piece of Ex equipment installed.</p>
<p><em>Source: <a href="https://www.atex-shop.de/en/blog/news-7/explosion-protection-in-hydrogen-systems-why-existing-atex-concepts-are-often-insufficient-100" target="_blank" rel="noopener">ATEXshop.de, Feb 2026</a></em></p>

<h2 id="chemical-outlook">2026 Chemical Sector Outlook</h2>
<p>ALL4, a US environmental consulting firm, published their annual chemical sector lookahead for 2026. Key regulatory items affecting hazardous areas:</p>
<ul>
<li><strong>EPA Risk Management Program (RMP)</strong> updates requiring newer prevention technology and backup safety measures</li>
<li><strong>OSHA Process Safety Management (PSM)</strong> expected updates on contractor safety and management of change</li>
<li><strong>Clean Water Act</strong> changes affecting chemical storage facilities near waterways</li>
</ul>
<p>For Ex equipment manufacturers and installers, the takeaway is that US chemical plants will face more regulatory pressure in 2026, which typically drives equipment upgrades and re-certification.</p>
<p><em>Source: <a href="https://www.all4inc.com/4-the-record-articles/2026-chemical-sector-lookahead/" target="_blank" rel="noopener">ALL4, Jan 2026</a></em></p>

<h2 id="lighting">Zone 1 LED Lighting: Field Experience</h2>
<p>SEEKINGLED published practical engineering notes from hazardous area lighting installations using their HB21 Series ATEX LED high bays. The article is useful because it covers real-world installation problems rather than catalogue specs: cable gland selection, thermal management at ambient temperatures above 40°C, and how <a href="../pages/temperature-classes.html">temperature class</a> derating works in practice.</p>
<p>LED replacements for old sodium or mercury vapour Ex d luminaires continue to be one of the easiest wins in hazardous area upgrades — lower power, longer life, and often better <a href="../pages/temperature-classes.html">T-class</a> ratings due to less heat generation.</p>
<p><em>Source: <a href="https://seekingled.com/atex-explosion-proof-lighting-practical-experience-from-hazardous-area-installations" target="_blank" rel="noopener">SEEKINGLED, Jan 23 2026</a></em></p>

<h2 id="events">Events & Milestones</h2>
<ul>
<li><strong>R. Stahl 150th anniversary</strong> — celebrations planned throughout 2026</li>
<li><strong>Pepperl+Fuchs confirmed as NAMUR 2026 sponsor</strong> — will shape the technical programme for Germany's largest process industry user group</li>
<li><strong>IECEx annual meeting</strong> preparations underway for Q2 2026</li>
</ul>
"""
    },
    {
        "filename": "2026-02.html",
        "seo_title": "Ex Industry Monthly: February 2026 — Hydrogen Incidents, US Regulatory Rollback, R. Stahl Results",
        "meta_desc": "February 2026 Ex industry news: fatal hydrogen truck explosion, Trump guts chemical safety rules, R. Stahl weak demand, OSHA cites US Steel, Dow blast report.",
        "h1": "Hydrogen Incidents, US Regulatory Rollback, and R. Stahl's Restructuring",
        "date_label": "February 2026",
        "iso_date": "2026-02-27",
        "hero_img": "https://images.unsplash.com/photo-1611348586804-61bf6c080437?w=1000&q=80",
        "content": """
<h2 id="hydrogen-explosion">Fatal Hydrogen Truck Explosion in California</h2>
<p>On February 24, a hydrogen transport truck exploded in Colton, San Bernardino County, killing one person and injuring another. The Colton Fire Department responded to the blast, which sent debris across a wide area and triggered a large hazmat response.</p>
<p>Hydrogen transport and storage incidents are increasingly in the news as the hydrogen economy scales up. The physics are unforgiving: <a href="../pages/gas-groups.html">gas group IIC</a>, minimum ignition energy of 0.017 mJ, and an explosive range of <a href="../pages/fundamentals.html">4-77% by volume</a>. Transport vehicles carrying compressed or liquefied hydrogen present risks that differ from traditional hydrocarbon fuels, and the emergency response playbook is still being written.</p>
<p><em>Source: <a href="https://ktla.com/news/inland-empire/one-person-killed-another-injured-in-san-bernardino-county-hydrogen-truck-explosion/" target="_blank" rel="noopener">KTLA, Feb 24 2026</a></em></p>

<h2 id="epa-rollback">Trump Administration Moves to Gut Chemical Safety Regulations</h2>
<p>The Guardian reported on February 27 that Trump administration officials are moving to dismantle the EPA's chemical disaster prevention system. The rules being targeted require hazardous facilities to use newer prevention technology, implement backup safety measures, and consider replacing dangerous chemicals with safer alternatives.</p>
<p>For the Ex industry, this is significant. The US Risk Management Program (RMP) rules directly affect how chemical plants design and maintain their hazardous area protections. Weakening these requirements doesn't change the physics — it just changes who bears the consequences when something goes wrong.</p>
<p><em>Source: <a href="https://www.theguardian.com/environment/2026/feb/27/trump-fire-chemical-safety-system-epa" target="_blank" rel="noopener">The Guardian, Feb 27 2026</a></em></p>

<h2 id="rstahl">R. Stahl Reports Weak 2025, Launches Restructuring</h2>
<p>R. Stahl AG published preliminary 2025 results showing a challenging year. Group sales came in at €313 million with order intake dropping to €306.5 million (down from €327.6 million the year before). The company exceeded its EBITDA forecast, but attributed that to "temporary effects" rather than underlying improvement.</p>
<p>More telling: R. Stahl launched a "development program for the future" and withdrew from the employer association, with membership ending July 31, 2026. Translation: restructuring is coming, likely including headcount reduction and operational streamlining. The 150-year-old explosion protection specialist is adapting to a market where demand has softened and competition from Asian manufacturers is intensifying.</p>
<p><em>Source: <a href="https://www.tradingview.com/news/eqs:46bbc7943094b:0-weak-demand-in-financial-year-2025-reflected-in-r-stahl-s-figures/" target="_blank" rel="noopener">TradingView / EQS, Feb 24 2026</a></em></p>

<h2 id="dow-blast">Dow Plant Explosion Traced to Forgotten Work Lights</h2>
<p>The CSB (Chemical Safety and Hazard Investigation Board) released its report on the 2023 Dow Chemical plant explosions in Plaquemine, Louisiana. The cause: portable work lights were left inside a large processing drum for nearly two months. When the drum was put back into service, the non-Ex-rated lights provided the ignition source for a series of explosions.</p>
<p>This is a textbook example of why <a href="../pages/installation-inspection.html">inspection and maintenance</a> procedures exist. Certified Ex equipment, proper <a href="../pages/zone-classification.html">zone classification</a>, and rigorous hot work / equipment control procedures — none of it matters if someone leaves a consumer-grade work light inside a vessel.</p>
<p><em>Source: <a href="https://www.wbrz.com/news/dow-plant-explosion-in-plaquemine-caused-by-portable-work-lights-left-in-drum-investigators-say" target="_blank" rel="noopener">WBRZ, Feb 26 2026</a></em></p>

<h2 id="osha-ussteel">OSHA Cites US Steel Over Explosion That "Exposed" Workers</h2>
<p>OSHA issued citations against US Steel following a valve rupture and explosion at one of its plants. Investigators found that safety shortcomings "exposed" employees to explosion hazards — a finding that carries both regulatory penalties and the weight of knowing it could have been worse.</p>
<p><em>Source: <a href="https://www.insurancejournal.com/news/east/2026/02/17/858214.htm" target="_blank" rel="noopener">Insurance Journal, Feb 17 2026</a></em></p>

<h2 id="deer-park">Deer Park Refinery: Labeling Failures Behind Fatal H₂S Release</h2>
<p>A new report on the 2024 fatal hydrogen sulfide release at the Deer Park refinery near Houston found that operators failed to clearly label equipment and didn't follow written procedures. H₂S is both toxic and flammable, falling under <a href="../pages/gas-groups.html">gas group IIB</a> with an auto-ignition temperature of 260°C (<a href="../pages/temperature-classes.html">T3</a>).</p>
<p>The incident reinforces a pattern seen across decades of incident reports: the equipment and the rules were there, but the procedures weren't followed.</p>
<p><em>Source: <a href="https://www.houstonpublicmedia.org/articles/news/energy-environment/2026/02/23/544206/report-finds-2024-fatal-deer-park-hydrogen-sulfide-release-caused-by-labeling-protocol-issues/" target="_blank" rel="noopener">Houston Public Media, Feb 23 2026</a></em></p>

<h2 id="canby">Manufacturing Facility Explosion in Oregon</h2>
<p>A presumed gas explosion at a manufacturing facility in Canby, Oregon on February 4 injured one person and sent metal debris flying, prompting a Level 3 evacuation order. The blast was powerful enough to require hazmat response from Clackamas County emergency services.</p>
<p><em>Source: <a href="https://www.kptv.com/2026/02/04/presumed-gas-explosion-reported-canby/" target="_blank" rel="noopener">KPTV Portland, Feb 4 2026</a></em></p>
"""
    },
]

ALL_ISSUES = [("2026-02.html","February 2026"),("2026-01.html","January 2026"),("2025-12.html","December 2025"),("2025-11.html","November 2025")]

for post in POSTS:
    sb = "\n".join(f'<a href="{f}" {"class=current" if f==post["filename"] else ""}>{l}</a>' for f,l in ALL_ISSUES)
    post["sidebar_links"] = sb
    html = BLOG_TEMPLATE.format(**post)
    path = os.path.join(BLOG_DIR, post["filename"])
    with open(path, 'w') as f:
        f.write(html)
    print(f"Built: {post['filename']} ({len(html)} bytes)")

print(f"\nDone! {len(POSTS)} blog posts built.")
