/* Deterministic behavior tests without a browser. Run: node scripts/check-interactions.cjs */
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const source = fs.readFileSync('assets/js/site.js', 'utf8');
function setup({reduced=false, observer=true, hash=''}={}) {
  const callbacks={}, observed=[], classes=new Set(), root=new Set();
  const button={hidden:true, expanded:'false', span:{textContent:'+'}, focused:false,
    setAttribute(k,v){this.expanded=v;},getAttribute(){return this.expanded;},
    querySelector(){return this.span;},addEventListener(k,fn){callbacks['button:'+k]=fn;},focus(){this.focused=true;}};
  const navigation={classList:{remove(k){classes.delete(k);},toggle(k,v){v?classes.add(k):classes.delete(k);}},addEventListener(k,fn){callbacks['nav:'+k]=fn;}};
  const details={open:false}, target={closest(){return details;}};
  let observerCallback;
  const window={matchMedia(query){return {matches:reduced,addEventListener(k,fn){callbacks['media:'+query]=fn;}};},addEventListener(k,fn){callbacks[k]=fn;}};
  function IntersectionObserver(fn){observerCallback=fn;this.observe=e=>observed.push(e);this.unobserve=e=>observed.splice(observed.indexOf(e),1);}
  if(observer)window.IntersectionObserver=IntersectionObserver;
  const element={classList:{add(k){this.added=k;}}};
  const document={documentElement:{classList:{add(k){root.add(k);}}},querySelector(){return button;},getElementById(id){return id==='navigation'?navigation:id==='privacy-details'?target:null;},addEventListener(k,fn){callbacks[k]=fn;},querySelectorAll(){return [element];}};
  const location={hash};
  vm.runInNewContext(source,{document,window,location,IntersectionObserver});
  return {callbacks,button,classes,details,location,observed,element,reveal:()=>observerCallback([{isIntersecting:true,target:element}])};
}
for(let i=0;i<3;i++){
  const t=setup();assert.equal(t.button.hidden,false);
  t.callbacks['button:click']();assert.equal(t.button.expanded,'true');assert(t.classes.has('is-open'));
  t.callbacks['button:click']();assert.equal(t.button.expanded,'false');assert(!t.classes.has('is-open'));
  t.callbacks['button:click']();t.callbacks.keydown({key:'Escape'});assert(t.button.focused);assert.equal(t.button.expanded,'false');
  t.callbacks['button:click']();t.callbacks['nav:click']({target:{closest:()=>({})}});assert.equal(t.button.expanded,'false');
  t.location.hash='#privacy-details';t.callbacks.hashchange();assert(t.details.open);
  t.details.open=false;t.callbacks.hashchange();assert(t.details.open);
  t.details.open=false;t.callbacks.click({target:{closest:()=>({getAttribute:()=> '#privacy-details'})}});assert(t.details.open);
  t.callbacks['button:click']();t.callbacks['media:(min-width: 761px)']();assert.equal(t.button.expanded,'false');
  t.location.hash='#%broken';assert.doesNotThrow(()=>t.callbacks.hashchange());
  assert.equal(t.observed.length,1);t.reveal();assert.equal(t.observed.length,0);assert.equal(t.element.classList.added,'reveal-in');
}
assert.equal(setup({reduced:true}).observed.length,0);
assert.equal(setup({observer:false}).observed.length,0);
assert(setup({hash:'#privacy-details'}).details.open);
console.log('PASS: repeated mobile menu, Escape/focus, navigation close, linked FAQ, malformed hash, one-time reveal, reduced motion and missing-observer fallback. These are unit tests, not browser rendering tests.');
