A=[('Отзывы о пансионатах: как отличить заказные от настоящих', 'otzyvy-o-pansionatah', '2026-11-18'), ('Компенсации и налоговый вычет за пансионат: что известно', 'kompensacii-i-vychet-za-pansionat', '2026-11-20'), ('Пансионат для пожилых в Оренбурге: как выбрать и проверить', 'pansionat-dlya-pozhilyh-v-orenburge', '2026-11-21')]
H='https://xn----7sbavm3abdeguerd1d.xn--p1ai'
p="sitemap.xml"; s=open(p,encoding="utf-8").read()
for t,sl,d in A:
    if "/"+sl+"/" not in s: s=s.replace("</urlset>",'<url><loc>'+H+'/'+sl+'/</loc><lastmod>'+d+'</lastmod><priority>0.8</priority></url>\r\n</urlset>')
open(p,"w",encoding="utf-8",newline="").write(s)
p="index.html"; x=open(p,encoding="utf-8").read()
m='<h2>Новые материалы</h2>\n<div class="cards">\n'
if A[0][1] not in x and m in x:
    cards="".join('<a class="card" href="/%s/"><b>%s</b><span>Новый материал справочника.</span></a>\n'%(sl,t) for t,sl,d in A)
    x=x.replace(m,m+cards,1)
    ups="".join("<li><strong>%s:</strong> опубликована статья «%s»</li>\n"%(d[8:]+"."+d[5:7]+"."+d[:4],t) for t,sl,d in reversed(A))
    k="<li><strong>19.11.2026"
    x=x.replace(k,ups+k,1) if k in x else x.replace("<h2>Последние обновления</h2>\n<ul>\n","<h2>Последние обновления</h2>\n<ul>\n"+ups,1)
open(p,"w",encoding="utf-8",newline="").write(x)
print("готово")
