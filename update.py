import re,io
A=[('Пансионат для пожилых в Уфе: как выбрать и проверить', 'pansionat-dlya-pozhilyh-v-ufe', '2026-11-02'), ('Пансионат или сиделка на дому: что выбрать семье', 'pansionat-ili-sidelka', '2026-11-03'), ('Как уговорить пожилого родственника переехать в пансионат', 'kak-ugovorit-pereehat-v-pansionat', '2026-11-05')]
H='https://xn----7sbavm3abdeguerd1d.xn--p1ai'
p="sitemap.xml"; s=open(p,encoding="utf-8").read()
for t,sl,d in A:
    if sl not in s: s=s.replace("</urlset>",'<url><loc>'+H+'/'+sl+'/</loc><lastmod>'+d+'</lastmod><priority>0.8</priority></url>\r\n</urlset>')
open(p,"w",encoding="utf-8",newline="").write(s)
p="index.html"; x=open(p,encoding="utf-8").read()
if "pansionat-ili-sidelka" not in x:
    cards="".join('<a class="card" href="/%s/"><b>%s</b><span>Новый материал справочника.</span></a>\n'%(sl,t) for t,sl,d in A)
    x=x.replace("<h2>Выбор по типу ухода</h2>","<h2>Новые материалы</h2>\n<div class=\"cards\">\n"+cards+"</div>\n\n<h2>Выбор по типу ухода</h2>",1)
    ups="".join("<li><strong>%s:</strong> опубликована статья «%s»</li>\n"%(d,t) for t,sl,d in reversed(A))
    x=x.replace("<h2>Последние обновления</h2>\n<ul>\n","<h2>Последние обновления</h2>\n<ul>\n"+ups,1)
open(p,"w",encoding="utf-8",newline="").write(x)
print("готово")
