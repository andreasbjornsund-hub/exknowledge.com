#!/usr/bin/env python3
"""Build the English monthly blog posts (blog/*.html).

The page chrome (security policy, analytics, favicons, stylesheets, nav,
footer and scripts) is copied from the live blog index at build time, so
generated posts always match the current site. See DESIGN.md.
Run from the repo root: python3 build_blog.py
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(ROOT, "blog")
CHROME_SOURCE = os.path.join(BLOG_DIR, "index.html")


def site_chrome():
    """Extract shared head tags, nav, footer and trailing scripts from a live page."""
    s = open(CHROME_SOURCE, encoding="utf-8").read()
    head = s.split("</head>")[0]
    keep = []
    for pat in (r'<meta http-equiv="Content-Security-Policy"[^>]*>', r'<meta name="referrer"[^>]*>',
                r'<script src="https://hazardousareaguide\.com/consent-banner\.js"></script>',
                r'<link rel="(?:icon|apple-touch-icon)"[^>]*>', r'<link rel="stylesheet"[^>]*>',
                r'<script async src="https://www\.googletagmanager\.com/gtag/js[^"]*"></script>',
                r'<script>window\.dataLayer=.*?</script>'):
        keep += re.findall(pat, head, re.S)
    nav = re.search(r'<nav class="nav">.*?</nav>', s, re.S).group(0)
    nav = nav.replace(' aria-current="page" class="active"', '')
    footer = re.search(r'<footer class="footer">.*?</footer>', s, re.S).group(0)
    scripts = "\n".join(sorted(set(re.findall(r'<script src="/js/[a-z]+\.js"></script>', s)) | {'<script src="/js/forms.js"></script>'},
                               key=lambda t: ["nav", "reveal", "search", "forms", "toast"].index(re.search(r"/js/([a-z]+)", t).group(1))))
    return "\n  ".join(keep), nav, footer, scripts


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
  {site_head}
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
{site_nav}

<section class="content-page">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="/">Home</a> <span aria-hidden="true">/</span> <a href="/blog/">Blog</a> <span aria-hidden="true">/</span> <span>{date_label}</span>
    </nav>
    <div class="content-layout">
      <article class="content-body">
        <img class="content-hero" src="{hero_img}" alt="{h1}" loading="lazy" width="820" height="240">
        <p class="post-date">{date_label}</p>
        <h1>{h1}</h1>
        {content}
        <aside class="news-cta" aria-labelledby="newsCtaTitle">
          <h2 class="news-cta-title" id="newsCtaTitle">Get the monthly Ex industry update</h2>
          <p>Standards changes, incidents worth learning from and new guides, once a month. No spam.</p>
          <form class="news-cta-form" action="#" method="POST" data-exk-form data-subject="ExKnowledge newsletter signup (blog)" data-success="Thanks for subscribing. The next update is on its way.">
            <input type="hidden" name="_subject" value="ExKnowledge newsletter signup (blog)">
            <label class="field-label" for="newsEmail">Work email</label>
            <div class="news-cta-row">
              <input class="field" type="email" id="newsEmail" name="email" autocomplete="email" placeholder="name@company.com" required>
              <button type="submit" class="btn btn--primary">Subscribe</button>
            </div>
          </form>
        </aside>
      </article>
      <aside class="content-sidebar" aria-label="More posts">
        <div class="sidebar-card">
          <h4><i class="ph ph-archive" aria-hidden="true"></i> All issues</h4>
          {sidebar_links}
        </div>
      </aside>
    </div>
  </div>
</section>

{site_footer}

{site_scripts}
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
        "hero_img": "https://images.unsplash.com/photo-1690508313456-bf8c851e8319?w=1000&q=80",
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
        "hero_img": "https://images.unsplash.com/photo-1611273426858-450d8e3c9fce?w=1000&q=80",
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
        "hero_img": "https://images.unsplash.com/photo-1566221857770-508d35ee6220?w=1000&q=80",
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

# July and September 2026 issues (researched 2026-09-29; every item sourced in its month)
POSTS += [{'filename': '2026-07.html', 'seo_title': 'Ex Industry Monthly: July 2026 — IEC 60079-0, NFPA 660', 'meta_desc': 'July 2026 Ex news: IEC 60079-0 Edition 8 changes, Wessex Water charged over Avonmouth, NTSB hot-work finding, NFPA 660 and certified inspection robots.', 'h1': 'IEC 60079-0 Edition 8, Wessex Water Charges, and a Hot-Work Explosion on a Sludge Vessel', 'date_label': 'July 2026', 'iso_date': '2026-07-30', 'hero_img': 'https://images.unsplash.com/photo-1611273426858-450d8e3c9fce?w=1000&q=80', 'content': '\n<h2 id="iec-60079-0-2026">IEC 60079-0:2026: Edition 8 of the General Requirements</h2>\n<p>The IEC published the eighth edition of IEC 60079-0, the general requirements document that every other Ex protection standard builds on, on June 16, 2026. It replaces the 2017 seventh edition. In July SGS published a summary of the changes for manufacturers. Most are minor for existing certified products, but several are not.</p>\n<p>On marking and documentation, the ambient temperature range must now always be marked, even when it is the standard −20 °C to +40 °C, and the temperature range of an Ex component must appear in its schedule of limitations. IP marking is clarified, and there are new requirements for alternative marking using digital technology. Other changes cover electrostatic bonding of dissipative non-metallic enclosures, modified surface resistance testing, temperature sensors and shutdown for rotating machines with auxiliary cooling fans, instructions for converter-driven type "e" motors, factory wiring between enclosures, IP retention for plugs and sockets, and cable glands with multi-hole seals. Sodium nickel chloride is added to the permitted secondary cells.</p>\n<p>For users, the most visible effect will be on nameplates, where the ambient range will always be shown, so there is less need to assume the default. For manufacturers, the practical question is timing. When new certificates must be issued to the 2026 edition depends on IECEx transition decisions and, in the EU, on when the EN version is cited in the Official Journal (see <a href="../pages/standards.html">Ex standards</a>, <a href="../pages/ex-markings.html">Ex markings</a> and <a href="../pages/how-to-read-atex-nameplate.html">reading an ATEX nameplate</a>).</p>\n<p><em>Source: <a href="https://www.sgs.com/en-gb/news/2026/07/iec-60079-0-2026-significant-technical-changes" target="_blank" rel="noopener">SGS, Jul 17 2026</a></em></p>\n\n<h2 id="wessex-water">Wessex Water to Face Charges Over the 2020 Avonmouth Explosion</h2>\n<p>On July 15 the UK Health and Safety Executive confirmed it had authorized criminal charges against Wessex Water under the Health and Safety at Work etc. Act 1974. The charges relate to the explosion at its Avonmouth wastewater treatment site in Bristol on December 3, 2020, which killed four people, including a 16-year-old apprentice. The explosion happened in a silo containing biosolids. Avon and Somerset Police had dropped a manslaughter investigation in July 2024.</p>\n<p>HSE has not published a cause, and the case now goes to court. Nothing should be read into it about fault until then. For Ex practice, the relevance is the type of plant. Wastewater and biosolids sites handle material that can give off flammable gas and, once dried, can form combustible dust. That puts them squarely under <a href="../pages/dsear-regulations-uk.html">DSEAR</a>: a risk assessment, <a href="../pages/zone-classification.html">zone classification</a> wherever an explosive atmosphere can form (including inside and above storage vessels), and control of ignition sources for any work carried out there (see also <a href="../pages/dust-explosion-protection.html">dust explosion protection</a>).</p>\n<p><em>Source: <a href="https://www.itv.com/news/westcountry/2026-07-15/water-firm-faces-criminal-charges-over-blast-that-killed-four" target="_blank" rel="noopener">ITV News, Jul 15 2026</a></em></p>\n\n<h2 id="hunts-point">NTSB: Torch Used on Deck Ignited Gas From a Sludge Tank</h2>\n<p>The NTSB published its report on the May 24, 2025 explosion aboard the New York City sludge vessel <em>Hunts Point</em>, moored at the North River Wastewater Treatment Plant. Sludge gives off flammable gases, including methane. The crew needed to loosen sludge in the cargo tanks, but the pipe plugs on the cleaning hatch covers had seized, so the flanges were removed from the hatches. When some flange bolts broke, the chief engineer used a heating torch to free them. Gas coming out of the tank ignited, the tank over-pressurized, and the chief engineer was killed. Three other crew were injured, and the vessel suffered about $10 million in damage.</p>\n<p>NTSB noted that once the flanges were off, nothing prevented an ignition source from reaching the gas leaving the tanks. The employer\'s policy treated torch use on deck as hot work requiring a permit, placards warned against open lights, and the master had warned the chief engineer twice. The training record showed no hot-work training, and the 2024 annual safety training did not cover hot work procedures or the gases produced by sludge.</p>\n<p>The general lesson: opening a closed vessel creates a new source of release, so the hazardous area around the opening changes for as long as it is open. Hot-work permits, gas testing and isolation are the controls for that temporary condition (see <a href="../pages/installation-inspection.html#activities-requiring-special-attention">maintenance activities requiring special attention</a> and <a href="../pages/zone-classification.html#zone-extent">zone extent</a>).</p>\n<p><em>Source: <a href="https://www.workboat.com/coastal-inland-waterways/ntsb-hot-work-triggered-deadly-new-york-sludge-tanker-explosion" target="_blank" rel="noopener">WorkBoat, Jul 31 2026</a></em></p>\n\n<h2 id="nfpa-660">NFPA 660: What the Consolidated Dust Standard Changed</h2>\n<p>A Safety+Health column by a Fike explosion safety consultant set out what NFPA 660 means in practice. NFPA 660, <em>Standard for Combustible Dusts and Particulate Solids</em>, took effect on December 6, 2024. It merged six documents (NFPA 61, 484, 652, 654, 655 and 664) into one. Chapters 1–10 are fundamentals that apply to every facility: hazard identification, the dust hazard analysis, management systems, prevention and mitigation, and a new chapter on emergency planning and response. Commodity chapters follow: 21 for agricultural and food, 22 for metals, 23 for sulfur, 24 for wood, and 25 for other dusts.</p>\n<p>According to the article, the core requirements are largely unchanged, but they are renumbered and reorganized. "Management of change" is now defined, and a new operational readiness review (8.12) calls for a pre-startup review for new processes and for restarts after shutdowns. The next edition is expected in 2028. The first draft report is scheduled for October 28, and second draft public comments run until January 6.</p>\n<p>NFPA 660 covers the dust hazard analysis, housekeeping and process protection. Electrical area classification for dust in the US still follows the NEC, with NFPA 499 as the recommended practice (see <a href="../pages/dust-explosion-protection.html">dust explosion protection</a> and <a href="../pages/nec-500-vs-atex-iec.html">NEC 500 vs ATEX/IEC</a>).</p>\n<p><em>Source: <a href="https://www.safetyandhealthmagazine.com/consolidated-combustible-dust-standard/" target="_blank" rel="noopener">Safety+Health, Jul 27 2026</a></em></p>\n\n<h2 id="robots">Certified Inspection Robots and Fixed Acoustic Monitoring</h2>\n<p>In late June, UL Solutions issued the first certification under UL 6260, the Outline of Investigation for Remotely-Operated Inspection and Maintenance Equipment for Hazardous (Classified) Locations, to the ExRobotics ExR-2.5 inspection robot. In July its North American distributor, MicroWatt, launched the robot there. The North American rating given is Class I, Division 2, Groups C and D, T4. According to UL, the evaluation covered batteries, electrical systems and mechanical components under normal and fault conditions. The manufacturer separately states ATEX/IECEx Zone 1 certification for the platform.</p>\n<p>In the same month, Sorama launched the L642Ex, a fixed acoustic monitor for Zone 1 areas certified by DEKRA on April 3, 2026. It is designed to detect and locate gas leaks, mechanical anomalies and partial discharge, and can be mounted on assets or carried on a robotic platform.</p>\n<p>A practical point for users is that the Division 2 and Zone 1 ratings are different claims. A robot marked Class I, Division 2, Groups C and D is not suitable for Division 1 areas, or for Group B (hydrogen) areas, under the NEC. Check the marking against the classification of each area it will patrol (see <a href="../pages/nec-500-vs-atex-iec.html">NEC 500 vs ATEX/IEC</a>, <a href="../pages/gas-groups.html">gas groups</a> and <a href="../pages/epl.html">EPL</a>).</p>\n<p><em>Source: <a href="https://energynow.ca/2026/07/microwatt-launches-north-americas-first-ul-certified-inspection-robot-for-hazardous-locations/" target="_blank" rel="noopener">EnergyNow, Jul 15 2026</a>; <a href="https://hydrocarbonprocessing.com/news/2026/07/sorama-launches-world-s-first-fixed-acoustic-monitor-certified-for-atexiecex-zone-1-areas/" target="_blank" rel="noopener">Hydrocarbon Processing, Jul 7 2026</a></em></p>\n\n<h2 id="analyzers">Flameproof Analyzer Enclosures as an Alternative to Purge</h2>\n<p>AMETEK Process Instruments added flameproof (Ex d) enclosures to its 993X and 9933 UV gas analyzers. They are certified to ATEX and IECEx for Zone 1 and rated IP66/NEMA 4X. The analyzers measure sulfur compounds such as H₂S, carbonyl sulfide and methyl mercaptan in natural gas and biomethane, and sulfur species in sulfur recovery units. The stated purpose is to allow Zone 1 installation where purge gas is unavailable or impractical.</p>\n<p>This is a common trade-off in analyzer design. <a href="../pages/protection-methods.html#ex-p--pressurization-iec-60079-2">Pressurization (Ex p)</a> depends on a continuous supply of protective gas, plus monitoring and interlocks that act when pressure is lost. <a href="../pages/protection-methods.html#ex-d--flameproof-enclosure-iec-60079-1">Flameproof enclosures (Ex d)</a> need no utility, but the enclosure must contain an internal explosion. That means flame paths, fasteners and cable entries have to stay intact through every opening and <a href="../pages/installation-inspection.html#inspection-iec-60079-17">inspection</a>.</p>\n<p><em>Source: <a href="https://www.hydrocarbonprocessing.com/news/2026/07/ametek-process-instruments-introduces-explosion-proof-993x-series-of-gas-analyzers-for-zone-1-applications/" target="_blank" rel="noopener">Hydrocarbon Processing, Jul 7 2026</a></em></p>\n\n<h2 id="events">Events &amp; Milestones</h2>\n<ul>\n<li><strong>IEC 60079-11:2023 Interpretation Sheet 6</strong> (intrinsic safety) published July 23. The IEC lists Amendment 1 to the 2023 edition as under development, with forecast publication in October 2027</li>\n<li><strong>Liushenyu coal mine, China</strong>: authorities widened the investigation into the May 22 gas explosion that killed 82 workers, and a senior provincial mine safety official was placed under investigation (Hazardex, Jul 23)</li>\n</ul>\n'}, {'filename': '2026-09.html', 'seo_title': 'Ex Industry Monthly: September 2026 — Shell CSB, Vapes', 'meta_desc': 'September 2026 Ex news: CSB report on Shell Monaca, vapes in Queensland coal mines, ISO/IEC 80079-38 Edition 2, Yenkin plea and California battery fires.', 'h1': 'Shell Monaca CSB Report, Vapes in Coal Mines, and New Mining and Assembly Standards', 'date_label': 'September 2026', 'iso_date': '2026-09-29', 'hero_img': 'https://images.unsplash.com/photo-1566221857770-508d35ee6220?w=1000&q=80', 'content': '\n<h2 id="shell-monaca">CSB: Backflow Into a Lit Furnace Caused the Shell Monaca Explosion</h2>\n<p>On September 16 the US Chemical Safety Board released its final report on the June 4, 2025 explosion at the Shell Polymers Monaca ethane cracker in Pennsylvania. Flammable cracked gas flowed back from the downstream quench tower into the firebox of Furnace 5, where it reached lit pilots and ignited about six minutes later. The explosion ruptured the firebox wall and was followed by a fire. Fifteen employees were evacuated, and no one was killed or seriously injured. Shell estimated property damage at about $95 million, and an estimated 5,100 pounds of ethylene and combustion products were released.</p>\n<p>According to the CSB, a process control engineer who had never done the task before opened both motor-operated valves that isolated the furnace at the same time. Shell relied on 11 administrative controls to prevent backflow. The furnace licensor had provided engineered controls that could prevent it, but they were not configured for the step of removing double isolation. The control screen showed three nearly identical valves whose tags differed mainly in the last digit. The CSB recommended engineered controls to prevent backflow in all modes of operation.</p>\n<p>Fired heaters are permanent ignition sources inside process units, and <a href="../pages/zone-classification.html">area classification</a> does not protect against flammable gas routed into a firebox. That has to be prevented by the process design and its safeguards. The case also shows how start-up and shutdown steps can defeat protections designed around normal operation (see <a href="../pages/fundamentals.html">explosion fundamentals</a>).</p>\n<p><em>Source: <a href="https://www.csb.gov/us-chemical-safety-board-releases-final-investigation-report-on-2025-explosion-and-fire-at-shell-polymers-monaca-facility-in-pennsylvania/" target="_blank" rel="noopener">U.S. Chemical Safety Board, Sep 16 2026</a></em></p>\n\n<h2 id="vapes-coal-mines">Queensland Regulator Warns Over Vapes in Underground Coal Mines</h2>\n<p>Resources Safety &amp; Health Queensland (RSHQ) issued a safety alert after six reports of contraband in mines over five months, including vapes, mobile phones, watches and smoking materials. Two of the alleged incidents involved vapes being used underground. RSHQ had never received a report of a vape in a mine before this year, and had had no reports of contraband in underground coal mines since 2012.</p>\n<p>Testing by RSHQ\'s Safety in Mines Testing and Research Station (Simtars) found that vape heating elements can exceed 250 °C in use. It also found the devices can generate more than 100 times the energy needed to ignite gas in an underground coal mine. The regulator\'s message: no vapes, no lighters, no contraband underground.</p>\n<p>Equipment taken into a gassy underground coal mine is Group I and certified to <a href="../pages/epl.html#mining">EPL Ma or Mb</a>. A personal device with a lithium cell and a heating element has no such protection, and methane and coal dust together make it a credible ignition source (see <a href="../pages/gas-groups.html">gas groups</a>). The same logic applies to personal electronics in any classified area above ground.</p>\n<p><em>Source: <a href="https://www.abc.net.au/news/2026-09-11/contraband-vape-warning-for-coal-mines/107142456" target="_blank" rel="noopener">ABC News, Sep 10 2026</a></em></p>\n\n<h2 id="standards">Standards: ISO/IEC 80079-38 Edition 2 and IEC 60079-46 at FDIS</h2>\n<p>ISO/IEC 80079-38:2026, the second edition of the standard for Group I Ex equipment and assemblies forming mining machinery, was published on September 25. It replaces the 2016 first edition as a technical revision. It covers construction, testing and marking for equipment at EPL Ma and Mb. The IEC refers readers to the foreword for the list of technical changes.</p>\n<p>Separately, IEC 60079-46 (equipment assemblies) went to its final draft (FDIS) vote, which runs from September 18 to October 30. Its forecast publication date is January 8, 2027, and it will replace the 2017 Technical Specification with an International Standard. It covers assemblies built from individually certified items and addresses new ignition hazards that the assembly creates beyond those individual certificates. It excludes pressurized or ventilated rooms (IEC 60079-13), analyzer houses (IEC TR 60079-16), installation on site, and Group I.</p>\n<p>For skid builders and package vendors, 60079-46 is the document that will define how an assembly of certified parts is assessed as a whole (see <a href="../pages/standards.html">Ex standards</a> and <a href="../pages/certification.html">certification</a>).</p>\n<p><em>Source: <a href="https://webstore.iec.ch/en/publication/79914" target="_blank" rel="noopener">IEC Webstore, Sep 25 2026</a>; <a href="https://webstore.iec.ch/en/publication/117098" target="_blank" rel="noopener">IEC Webstore, Sep 18 2026</a></em></p>\n\n<h2 id="yenkin-majestic">Yenkin-Majestic Pleads Guilty Over 2021 Resin Plant Explosion</h2>\n<p>Yenkin Majestic Paint Corporation pleaded guilty in federal court in the Southern District of Ohio to a charge of negligent endangerment. The charge relates to the April 8, 2021 explosion at its Columbus resin plant, which killed one employee and injured several others. According to the Justice Department, a new manway fitted to a resin kettle in December 2020 was never pressure tested and leaked from the start. The company kept using it with a thicker gasket that it believed was PTFE but was actually silicone.</p>\n<p>On the night of the explosion, the kettle agitator had stopped, likely because of electrical work, and restarting it caused the contents to vaporize. Hot resin and flammable solvent vapor escaped through the manway. Flammable gas detectors registered rising concentrations but were not configured to sound an audible alarm. The vapor found an ignition source at 12:04 a.m.</p>\n<p>Gas detection only reduces risk if it leads to action. Where detection is part of the basis of safety, for example to raise an alarm, trip non-Ex equipment or start ventilation, its setpoints and alarm outputs belong in the same inspection and change-control regime as the Ex equipment itself (see <a href="../pages/installation-inspection.html">installation and inspection</a>).</p>\n<p><em>Source: <a href="https://www.justice.gov/opa/pr/ohio-company-pleads-guilty-worker-death-case-0" target="_blank" rel="noopener">U.S. Department of Justice, Sep 4 2026</a></em></p>\n\n<h2 id="duluth">Out-of-Service Gasoline Tank Explodes in Duluth</h2>\n<p>On September 14 a mostly empty 17,000-gallon gasoline tank exploded at a Superior Fuel transfer facility in Duluth, Minnesota, while two workers were removing the last of the fuel. One worker was injured and later released from hospital. The tank had already been taken out of service and disconnected ahead of a move to another site.</p>\n<p>According to the company, residual gasoline vapor from the tank had entered the containment area, and it ignited when a worker plugged in an extension cord. The Duluth Fire Marshal\'s Office has not confirmed that account and is still investigating.</p>\n<p>A tank taken out of service remains a source of release until it has been cleaned and gas-freed. Gasoline vapor is heavier than air and collects in bunds, pits and containment. Temporary power, meaning extension cords, portable lights and plug connections, is among the most common non-Ex ignition sources brought into those spaces during maintenance (see <a href="../pages/zone-classification.html#zone-extent">zone extent</a> and <a href="../pages/installation-inspection.html#activities-requiring-special-attention">maintenance activities requiring special attention</a>).</p>\n<p><em>Source: <a href="https://www.northernnewsnow.com/2026/09/14/update-one-injured-roads-closed-after-fuel-tank-explosion-leads-fire-duluth/" target="_blank" rel="noopener">Northern News Now, Sep 14 2026</a></em></p>\n\n<h2 id="bess">Two California Battery Storage Incidents in One Week</h2>\n<p>On September 22 a "minor explosion" and fire in one of two battery energy storage systems at the Metropolitan Water District\'s facility in La Verne, California, led to evacuation orders. The next day about 200 homes were still evacuated. One civilian was injured at the start of the incident. Four days earlier, on September 18, fire broke out again at the Moss Landing battery plant, in a building damaged in the January 2025 fire. Batteries there were still charged, and officials said about 1,500 fully energized batteries were against the north wall. No cause had been given for either incident.</p>\n<p>The explosion hazard in lithium-ion storage is mainly a gas problem. Cells in thermal runaway vent flammable gases, including hydrogen, that can build up inside a container or room and then ignite. In the US, NFPA 855 requires explosion control for energy storage installations, either deflagration venting to NFPA 68 or explosion prevention (typically gas detection with mechanical ventilation) to NFPA 69. The requirements have been revised between editions, so check which edition the local authority has adopted (see <a href="../pages/hydrogen-explosion-protection.html">hydrogen explosion protection</a>).</p>\n<p><em>Source: <a href="https://www.latimes.com/california/story/2026-09-22/lithium-ion-battery-fire-in-la-verne-spurs-neighborhood-school-evacuations" target="_blank" rel="noopener">Los Angeles Times, Sep 22 2026</a>; <a href="https://www.latimes.com/california/story/2026-09-18/another-battery-fire-erupts-at-moss-landing-where-some-batteries-are-still-charged" target="_blank" rel="noopener">Los Angeles Times, Sep 18 2026</a></em></p>\n\n<h2 id="mol-tiszaujvaros">Hungary Fines MOL After Fatal Olefin Unit Restart Explosion</h2>\n<p>Hungarian authorities fined MOL Petrochemicals 38 million forints after investigating the May 22 explosion at its Tiszaújváros plant, which killed one worker and injured 11. The explosion happened during the restart of the Olefin-1 unit after a maintenance shutdown that began on April 27. During that shutdown, equipment was drained, residual hydrocarbons were removed and the system was purged with nitrogen. During commissioning, personnel noticed icing on a pipeline, and the explosion happened while that condition was being checked.</p>\n<p>The occupational safety authority found that safety equipment in parts of the plant could not detect and signal hazardous process conditions in time, or allow the process to be safely interrupted. MOL was ordered to review its technological and safety systems, improve risk assessments and worker information, and introduce scheduled maintenance for specified pipelines and fittings.</p>\n<p>Restart after maintenance is when a plant is least like its normal-operation design basis. An unexpected physical sign during start-up is a reason to treat the area as a possible source of release before sending people in to look (see <a href="../pages/zone-classification.html">zone classification</a> and <a href="../pages/installation-inspection.html">installation and inspection</a>).</p>\n<p><em>Source: <a href="https://www.hazardexonthenet.net/article/224146/Hungary-fines-MOL-after-fatal-Tisza%C3%BAjv%C3%A1ros-petrochemical-explosion.aspx" target="_blank" rel="noopener">Hazardex, Sep 22 2026</a></em></p>\n\n<h2 id="events">Events &amp; Milestones</h2>\n<ul>\n<li><strong>IECEx Annual Meetings</strong> (Sep 14–18, Beijing): ExMC, ExTAG and ExPCC meetings, assessor training and an industrial symposium</li>\n<li><strong>Gastech 2026</strong> (Sep 14–17, Bangkok): Vaisala launched the DMP370, an intrinsically safe dew point instrument for hydrogen, biomethane and natural gas service</li>\n<li><strong>BARTEC</strong> launched a modular Ex de energy distribution panel series certified to ATEX and IECEx for Zones 1/21 and 2/22, rated up to 690 V and 1,000 A (Sep 3)</li>\n<li><strong>Hazardex in the Regions</strong> (Sep 23, Ellesmere Port, UK): engineering judgement, competence and the threat from AI</li>\n</ul>\n'}]

ALL_ISSUES = [("2026-09.html", "September 2026"), ("2026-07.html", "July 2026"), ("2026-03.html", "March 2026"), ("2026-02.html", "February 2026"), ("2026-01.html", "January 2026"),
              ("2025-12.html", "December 2025"), ("2025-11.html", "November 2025")]

if __name__ == "__main__":
    site_head, site_nav, site_footer, site_scripts = site_chrome()
    import sys
    only = set(sys.argv[1:])   # e.g. python3 build_blog.py 2026-07.html: rebuild only these (older posts were post-processed by scripts/build_*.py)
    for post in POSTS:
        if only and post["filename"] not in only:
            continue
        post["sidebar_links"] = "\n          ".join(
            f'<a href="{f}"{" class=\"current\" aria-current=\"page\"" if f == post["filename"] else ""}>{l}</a>' for f, l in ALL_ISSUES)
        html = BLOG_TEMPLATE.format(site_head=site_head, site_nav=site_nav, site_footer=site_footer,
                                    site_scripts=site_scripts, **post)
        path = os.path.join(BLOG_DIR, post["filename"])
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Built: {post['filename']} ({len(html)} bytes)")
    print(f"\nDone! {len(POSTS)} blog posts built.")
