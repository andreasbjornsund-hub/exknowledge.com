(function(){
  var b=document.querySelector('.burger'),n=document.querySelector('.nav-links');
  if(b)b.addEventListener('click',function(e){e.stopPropagation();b.classList.toggle('open');n.classList.toggle('open')});
  document.addEventListener('click',function(e){
    if(b&&!b.contains(e.target)&&!n.contains(e.target)){b.classList.remove('open');n.classList.remove('open')}
  });
})();

// Mobile dropdown toggles
document.querySelectorAll('.has-dropdown > a').forEach(function(a) {
  a.addEventListener('click', function(e) {
    if (window.innerWidth <= 900) {
      e.preventDefault();
      var li = a.parentElement;
      document.querySelectorAll('.has-dropdown.open').forEach(function(el) { if (el !== li) el.classList.remove('open'); });
      li.classList.toggle('open');
    }
  });
});

function slideVideos(dir) {
  var track = document.getElementById('sliderTrack');
  var slide = track.querySelector('.slide');
  if (!slide) return;
  var w = slide.offsetWidth + 16; // width + gap
  track.scrollBy({ left: dir * w * 2, behavior: 'smooth' });
}

function playVideo(el, id) {
  var thumb = el.querySelector('.slide-thumb');
  thumb.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position:absolute;top:0;left:0;width:100%;height:100%;border:0"></iframe>';
  el.style.cursor = 'default';
  el.onclick = null;
}