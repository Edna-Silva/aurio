const el=()=>new Proxy(function(){},{get:(t,k)=>k==='classList'?{add(){},toggle(){}}:k==='style'?{}:k==='forEach'?()=>{}:el(),set:()=>true,apply:()=>el()});
global.document={getElementById:()=>el(),querySelectorAll:()=>[],addEventListener(){}, body:{style:{}}};
global.IntersectionObserver=class{observe(){}};global.Audio=class{play(){return Promise.resolve()}};global.window={innerWidth:1300};
require('./chk.js');
