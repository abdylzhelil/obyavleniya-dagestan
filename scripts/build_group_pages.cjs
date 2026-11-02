/* Build static group pages from the same data/render functions as the browser.
   No browser or npm dependency is needed: node scripts/build_group_pages.cjs */
const fs=require('fs'),path=require('path'),vm=require('vm');
const root=path.resolve(__dirname,'..');
const escape=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
class Node {
 constructor(tag,text){this.tag=tag;this.attrs={};this.children=[];this.value=text||'';}
 set className(v){this.attrs.class=v;} set textContent(v){this.children=[];this.value=String(v);} get textContent(){return this.value+this.children.map(x=>x.textContent).join('');}
 setAttribute(k,v){this.attrs[k]=String(v);} appendChild(n){this.children.push(n);return n;}
 toString(){if(!this.tag)return escape(this.value)+this.children.join('');let s='<'+this.tag+Object.entries(this.attrs).map(([k,v])=>' '+k+'="'+escape(v)+'"').join('')+'>';return s+(['img','br','hr','input'].includes(this.tag)?'':escape(this.value)+this.children.join('')+'</'+this.tag+'>');}
}
const doc={createElement:t=>new Node(t),createTextNode:t=>new Node(null,t),createDocumentFragment:()=>new Node(null),addEventListener:()=>{}};
const context=vm.createContext({document:doc});
const result=vm.runInContext(fs.readFileSync(path.join(root,'script.js'),'utf8')+'\nGROUPS.map(g=>({id:g.id,status:g.status,title:g.name+" — "+PLATFORM_NAMES[g.platform]+" | "+SITE.siteName,description:g.description,url:getAbsoluteUrl(getGroupPageHref(g.id)),html:String(createPromoPage(g))}))',context);
const template=fs.readFileSync(path.join(root,'group.html'),'utf8');
for(const g of result){
 let html=template.replace(/<main id="main">[\s\S]*?<\/main>/,'<main id="main"><section class="promo-section"><div class="wrap" id="group-root" data-static-group="'+g.id+'">'+g.html+'</div></section></main>');
 html=html.replace(/<title>[\s\S]*?<\/title>/,'<title>'+escape(g.title)+'</title>');
 for(const [attr,name,value] of [['name','description',g.description],['property','og:title',g.title],['property','og:description',g.description],['name','twitter:title',g.title],['name','twitter:description',g.description]])html=html.replace(new RegExp('<meta '+attr+'="'+name+'"[^>]*>'),'<meta '+attr+'="'+name+'" content="'+escape(value)+'">');
 html=html.replace(/<!-- Общая картинка[\s\S]*?-->/,'');
 html=html.replace('</head>','<link rel="canonical" href="'+g.url+'">\n<meta property="og:url" content="'+g.url+'">\n<meta name="robots" content="'+(g.status==='open'?'index, follow':'noindex, follow')+'">\n</head>');
 fs.writeFileSync(path.join(root,'group-'+g.id+'.html'),html);console.log('Static group:',g.id);
}
const sitemap=path.join(root,'sitemap.xml');let xml=fs.readFileSync(sitemap,'utf8');
xml=xml.replace(/\s*<url>\s*<loc>[^<]*\/group(?:\.html\?id=[^<]*|-[-a-z0-9]+\.html)<\/loc>\s*<\/url>/g,'');
const urls=result.filter(g=>g.status==='open').map(g=>'  <url>\n    <loc>'+g.url+'</loc>\n  </url>').join('\n');
xml=xml.replace('</urlset>',urls+'\n</urlset>');fs.writeFileSync(sitemap,xml);
