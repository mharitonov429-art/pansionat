A=[('Что взять с собой в пансионат: список вещей и документов', 'chto-vzyat-v-pansionat', '2026-12-01'), ('Права проживающих в пансионате и куда жаловаться', 'prava-prozhivayushchih-i-zhaloby', '2026-12-03'), ('Расторжение договора с пансионатом: порядок и возврат денег', 'rastorzhenie-dogovora-s-pansionatom', '2026-12-04'), ('Пансионат для пожилых в Самаре: как выбрать и проверить', 'pansionat-dlya-pozhilyh-v-samare', '2026-12-07'), ('Пансионат для пожилых в Казани: как выбрать и проверить', 'pansionat-dlya-pozhilyh-v-kazani', '2026-12-08'), ('Паллиативный уход: что это и когда нужен', 'palliativnyj-uhod-chto-eto', '2026-12-10'), ('Пансионат после операции: восстановление и уход', 'pansionat-posle-operacii', '2026-12-11'), ('Пансионат для пожилых в Магнитогорске: как выбрать и проверить', 'pansionat-dlya-pozhilyh-v-magnitogorske', '2026-12-14')]
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
    k="<li><strong>30.11.2026"
    x=x.replace(k,ups+k,1) if k in x else x.replace("<h2>Последние обновления</h2>\n<ul>\n","<h2>Последние обновления</h2>\n<ul>\n"+ups,1)
open(p,"w",encoding="utf-8",newline="").write(x)
print("готово")
