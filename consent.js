/* Version changes only when data processing or consent wording changes. */
(function(){
 const VERSION='2026-11-02',KEY='cookie-consent',DETAILS='cookie-consent-details';
 let memory=null;
 function read(){try{const choice=localStorage.getItem(KEY);if(choice==='no')return 'no';const d=JSON.parse(localStorage.getItem(DETAILS)||'null');return choice==='yes'&&d&&d.version===VERSION&&d.choice==='yes'&&Number.isFinite(Date.parse(d.date))?'yes':null;}catch(e){return memory;}}
 function write(choice){if(!['yes','no'].includes(choice))return;memory=choice;try{localStorage.setItem(KEY,choice);localStorage.setItem(DETAILS,JSON.stringify({choice:choice,version:VERSION,date:new Date().toISOString()}));}catch(e){}}
 function clear(){memory=null;try{localStorage.removeItem(KEY);localStorage.removeItem(DETAILS);}catch(e){}}
 window.SiteConsent={read:read,write:write,clear:clear,version:VERSION};window.cookieAccepted=read()==='yes';
})();
