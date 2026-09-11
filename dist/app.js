(() => {
 'use strict';
 const dictionaries=window.KOTOBAIA_TRANSLATIONS||{en:{}};
 const labels={en:'EN',ja:'日本語',ko:'한국어','zh-Hans':'简中','zh-Hant':'繁中',es:'ES',fr:'FR',de:'DE','pt-BR':'PT',it:'IT',ru:'RU',ar:'العربية'};
 const supported=new Set(Object.keys(dictionaries));
 const originalTitle=document.title;
 const dialog=document.querySelector('#language-dialog');
 const menu=document.querySelector('.menu-toggle');
 let activeLocale='en';
 const translate=source=>dictionaries[activeLocale]?.[source]||source;
 function normalizeLocale(value){
  if(!value)return null;
  if(supported.has(value))return value;
  const normalized=value.toLowerCase().replaceAll('_','-');
  if(normalized.startsWith('zh'))return /hant|tw|hk|mo/.test(normalized)?'zh-Hant':'zh-Hans';
  if(normalized.startsWith('pt'))return 'pt-BR';
  const base=normalized.split('-')[0];return supported.has(base)?base:null;
 }
 function closeMenu(){
  document.body.classList.remove('menu-open');
  menu?.setAttribute('aria-expanded','false');
  menu?.setAttribute('aria-label',translate('Open navigation'));
 }
 function setLocale(locale,persist=true){
  if(!supported.has(locale))return;
  activeLocale=locale;
  document.documentElement.lang=locale;
  document.documentElement.dir=locale==='ar'?'rtl':'ltr';
  document.documentElement.dataset.script=/^(zh|ja|ko)/.test(locale)?'cjk':'latin';
  document.querySelectorAll('[data-en]').forEach(el=>{el.textContent=translate(el.dataset.en);});
  document.querySelectorAll('[data-i18n-aria]').forEach(el=>el.setAttribute('aria-label',translate(el.dataset.i18nAria)));
  document.querySelectorAll('[data-i18n-alt]').forEach(el=>el.setAttribute('alt',translate(el.dataset.i18nAlt)));
  document.querySelectorAll('[data-language]').forEach(el=>el.setAttribute('aria-pressed',String(el.dataset.language===locale)));
  document.querySelectorAll('.language-current').forEach(el=>{el.textContent=labels[locale];});
  const heading=document.querySelector('h1');
  document.title=dictionaries[locale][originalTitle]||(locale==='en'?originalTitle:(heading?.textContent.trim()||originalTitle)+' — Kotobaia');
  if(persist){try{localStorage.setItem('kotobaia.language',locale);}catch{}}
  const currentURL=new URL(location.href);currentURL.searchParams.set('lang',locale);
  history.replaceState(null,'',currentURL);
  document.querySelectorAll('a[href]').forEach(link=>{
   const target=new URL(link.getAttribute('href'),location.href);
   if(!['http:','https:'].includes(target.protocol))return;
   if(target.origin!==location.origin&&!['kotobaia.com','sunimori.com'].includes(target.hostname))return;
   target.searchParams.set('lang',locale);link.href=target.href;
  });
 }
 let stored;try{stored=localStorage.getItem('kotobaia.language');}catch{}
 const locale=normalizeLocale(new URLSearchParams(location.search).get('lang'))||normalizeLocale(stored)||(navigator.languages||[navigator.language]).map(normalizeLocale).find(Boolean)||'en';
 setLocale(locale,false);
 document.querySelectorAll('.language-open').forEach(button=>button.addEventListener('click',()=>{
  closeMenu();dialog?.showModal();dialog?.querySelector('[data-language="'+activeLocale+'"]')?.focus();
 }));
 document.querySelectorAll('[data-language]').forEach(button=>button.addEventListener('click',()=>{setLocale(button.dataset.language);dialog?.close();}));
 document.querySelector('.dialog-close')?.addEventListener('click',()=>dialog?.close());
 dialog?.addEventListener('click',event=>{
  if(event.target!==dialog)return;
  const bounds=dialog.getBoundingClientRect();
  if(event.clientX<bounds.left||event.clientX>bounds.right||event.clientY<bounds.top||event.clientY>bounds.bottom)dialog.close();
 });
 menu?.addEventListener('click',()=>{
  const open=document.body.classList.toggle('menu-open');menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',translate(open?'Close navigation':'Open navigation'));
 });
 document.querySelectorAll('#site-nav a').forEach(link=>link.addEventListener('click',closeMenu));
 document.addEventListener('keydown',event=>{if(event.key==='Escape'){if(document.body.classList.contains('menu-open'))menu?.focus();closeMenu();}});
 document.addEventListener('click',event=>{if(document.body.classList.contains('menu-open')&&!event.target.closest('.site-header'))closeMenu();});
 matchMedia('(min-width:761px)').addEventListener('change',event=>{if(event.matches)closeMenu();});
 const updateHeader=()=>document.body.classList.toggle('scrolled',scrollY>24);
 window.addEventListener('scroll',updateHeader,{passive:true});updateHeader();
 const tabs=[...document.querySelectorAll('[data-experience]')];
 function selectExperience(tab){
  tabs.forEach(button=>{
   const selected=button===tab;button.setAttribute('aria-selected',String(selected));button.tabIndex=selected?0:-1;
   const panel=document.getElementById(button.getAttribute('aria-controls'));if(panel)panel.hidden=!selected;
  });
  document.querySelector('.experience-panels')?.setAttribute('data-active',tab.dataset.experience);
 }
 tabs.forEach((tab,index)=>{
  tab.addEventListener('click',()=>selectExperience(tab));
  tab.addEventListener('keydown',event=>{
   let next;const rtl=document.documentElement.dir==='rtl';
   if(event.key==='ArrowRight')next=(index+(rtl?-1:1)+tabs.length)%tabs.length;
   if(event.key==='ArrowLeft')next=(index+(rtl?1:-1)+tabs.length)%tabs.length;
   if(event.key==='Home')next=0;if(event.key==='End')next=tabs.length-1;
   if(next===undefined)return;event.preventDefault();selectExperience(tabs[next]);tabs[next].focus();
  });
 });
})();
