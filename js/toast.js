(function(){
  var p=new URLSearchParams(window.location.search);
  var msg=null;
  if(p.get("subscribed")==="1") msg="Thanks for subscribing! We’ll keep you updated.";
  if(p.get("thanks")==="1") msg="Thanks for reaching out! We’ll get back to you soon.";
  if(msg){
    var t=document.createElement("div");t.className="form-toast";
    t.innerHTML="<i class=\"ph ph-check-circle\"></i> "+msg;
    document.body.appendChild(t);
    setTimeout(function(){t.classList.add("visible")},100);
    setTimeout(function(){t.classList.remove("visible");setTimeout(function(){t.remove()},500)},5000);
    history.replaceState(null,"",window.location.pathname);
  }
})();