/* Pause decorative motion offscreen, in hidden tabs, or at the user's request. */
(function(){
 const reduce=window.matchMedia('(prefers-reduced-motion: reduce)');
 const demos=[...document.querySelectorAll('[data-motion-demo]')].map(function(node){
  return {node:node,button:document.querySelector('[data-motion-for="'+node.id+'"]'),visible:false,paused:false};
 });
 function update(d){d.node.classList.toggle('demo-motion-paused',!d.visible||d.paused||document.hidden||reduce.matches);if(d.button){d.button.hidden=reduce.matches;d.button.setAttribute('aria-pressed',String(d.paused));d.button.setAttribute('aria-label',d.paused?'Продолжить анимацию':'Приостановить анимацию');d.button.textContent=d.button.hasAttribute('data-motion-compact')?(d.paused?'Продолжить':'Пауза'):(d.paused?'Продолжить анимацию':'Приостановить анимацию');}}
 const io='IntersectionObserver' in window?new IntersectionObserver(function(entries){entries.forEach(function(e){const d=demos.find(x=>x.node===e.target);d.visible=e.isIntersecting;update(d);});},{threshold:.1}):null;
 demos.forEach(function(d){if(d.button)d.button.addEventListener('click',function(){d.paused=!d.paused;update(d);});if(io)io.observe(d.node);else d.visible=true;update(d);});
 document.addEventListener('visibilitychange',function(){demos.forEach(update);});
 if(reduce.addEventListener)reduce.addEventListener('change',function(){demos.forEach(update);});
})();
