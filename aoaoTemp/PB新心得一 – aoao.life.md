---
title: "PB新心得一 – aoao.life"
date: 2019-10-23 19:54:31
---

困扰了一周的问题，终于得到解决。

在调用含有“insert into”、“drop”之类字样的存储过程（Procedures）时，需要先将auto commit设置成true，调用后再将之设回来。并且需要注意的是，在修改的过程中，不能直接给它赋值true，而是要将true先赋给一个变量。
具体实现代码如下。

```
boolean bb=true
if sqlca.autocommit<>bb then
sqlca.autocommit=bb
disconnect using sqlca;
connect using sqlca;
end if

DECLARE select_xq2 PROCEDURE FOR p_SGTJ_XQ2
@int_year=:li_year,
@int_month=:li_month,
@char_HSJBH=:gs_company
using sqlca;
EXECUTE select_xq2  ;

if sqlca.sqlcode=-1 then
messagebox("","调用存储过程失败!~r~n"+sqlca.sqlerrtext)
disconnect using sqlca;
sqlca.autocommit=false
connect using sqlca;
return -1
end if

CLOSE select_xq2;
disconnect using sqlca;
sqlca.autocommit=not(bb)
connect using sqlca;
```