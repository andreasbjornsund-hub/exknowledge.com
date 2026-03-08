(function(){
  // Sections & content blocks fade in
  document.querySelectorAll(
    '.section, .section-title, .section-subtitle, .content-body > h2, .content-body > h3, .content-body > table, .content-body > .info-box, .content-body > .warning-box, .content-body > .tip-box'
  ).forEach(function(el){ el.classList.add('reveal'); });

  var sectionObs = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(e.isIntersecting){
        e.target.classList.add('visible');
        sectionObs.unobserve(e.target);
      }
    });
  }, { threshold: 0.05 });
  document.querySelectorAll('.reveal').forEach(function(el){ sectionObs.observe(el); });

  // Reveal all sections after short delay to prevent search-hiding bug
  setTimeout(function(){
    document.querySelectorAll('.reveal').forEach(function(el){
      el.classList.add('visible');
    });
    document.querySelectorAll('.topic-card, .blog-card, .bento-item').forEach(function(el){
      el.classList.add('visible');
    });
  }, 1500);

  // Staggered card reveal
  var cardObs = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(e.isIntersecting){
        var siblings = Array.prototype.slice.call(e.target.parentElement.children);
        var idx = siblings.indexOf(e.target);
        e.target.style.transitionDelay = (idx * 0.08) + 's';
        e.target.classList.add('visible');
        cardObs.unobserve(e.target);
      }
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('.topic-card, .blog-card, .bento-item').forEach(function(el){ cardObs.observe(el); });
})();
