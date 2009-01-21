#!usr/bin/env python
#
# (C) Legoktm 2008-2009, MIT License
# 
import MySQLdb
db = MySQLdb.connect(db='ltwiktionary_p', host="sql-s3", read_default_file="/home/legoktm/.my.cnf")
cur = db.cursor()
cur.execute("""
Select curdate() as `` from dual
union
(select concat(_utf8'* [[',replace(`a`.`pl_title`,_utf8'_',_utf8' '),_utf8']] (',`a`.`kiekis`,_utf8') ([[:Specialus:Whatlinkshere/',replace(`a`.`pl_title`,_utf8'_',_utf8' '),_utf8'|? nuorodos]])') AS ``
from (select `p`.`pl_title` AS `pl_title`,count(1) AS `kiekis`
from `pagelinks` `p`
where ((not(exists(select 1 AS `1` from `page` `pg`
where ((`p`.`pl_namespace` = `pg`.`page_namespace`) and (`p`.`pl_title` = `pg`.`page_title`)))))
and (`p`.`pl_namespace` = 0))
group by `p`.`pl_namespace`,`p`.`pl_title`) `a`
where (`a`.`kiekis` > 10)
order by `a`.`kiekis` desc);
""")
query = cur.fetchall()
content = ''
for row in query:
	content += row[0]
	content += '\n'
#content = content.decode('utf-8')
file = open('/home/legoktm/public_html/DBQ/22.txt','w')
file.write(content)
file.close()
cur.close()
db.close()