A=[('Пансионат для пожилых в Стерлитамаке: как выбрать и проверить', 'pansionat-dlya-pozhilyh-v-sterlitamake', '2026-12-15'), ('Пансионат при диабете у пожилых: на что обратить внимание', 'pansionat-pri-diabete', '2026-12-17'), ('Выгорание ухаживающего: что делать, если семья не справляется', 'vygoranie-uhazhivayushchego', '2026-12-18'), ('Пансионат для пожилых в Ижевске: как выбрать и проверить', 'pansionat-dlya-pozhilyh-v-izhevske', '2026-12-21'), ('Уход за лежачим больным дома: что нужно знать до решения о пансионате', 'uhod-za-lezhachim-doma', '2026-12-22'), ('Новый год с близким в пансионате: как организовать праздник', 'novyj-god-v-pansionate', '2026-12-24'), ('Как поддерживать связь с родителем в пансионате: посещения, звонки, видеосвязь', 'svyaz-s-roditelem-v-pansionate', '2026-12-25'), ('Пансионат для пожилых на северо-востоке Башкирии: Месягутово и соседние районы', 'pansionat-severo-vostok-bashkirii', '2026-12-28'), ('Пансионат для пожилых в Кургане: как выбрать и проверить', 'pansionat-dlya-pozhilyh-v-kurgane', '2026-12-29'), ('Как нанять сиделку: договор, проверка, оплата', 'kak-nanyat-sidelku', '2026-12-30'), ('Путеводитель по справочнику: все материалы по выбору пансионата', 'putevoditel-po-spravochniku', '2026-12-31')]
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
    k="<li><strong>14.12.2026"
    x=x.replace(k,ups+k,1) if k in x else x.replace("<h2>Последние обновления</h2>\n<ul>\n","<h2>Последние обновления</h2>\n<ul>\n"+ups,1)
open(p,"w",encoding="utf-8",newline="").write(x)
print("готово")
