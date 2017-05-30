Query #1:
select * FROM t1 LEFT JOIN t2 ON t1.a = t2.a WHERE t1.b > 1 AND t2.c = 5;


Recommendation #1:
create index index_t1_ab on t1(a, b);
create index index_t2_c on t2(c);

Recommendation #2:
create index index_t1_b on t1(b);
create index index_t2_ac on t2(a, c);
-----------------------

Query #2:
select * FROM t1 LEFT JOIN t2 ON t1.a = t2.a WHERE t1.b = 5000 AND t1.c > 3 ORDER BY t2.c , t2.d;


Recommendation #1:
create index index_t1_bc on t1(b, c);
create index index_t2_a on t2(a);
-----------------------

Query #3:
select * FROM t1 LEFT JOIN t2 ON t1.a = t2.a WHERE t2.b = 5000 AND t2.c > 3 ORDER BY t2.c, t2.d;


Recommendation #1:
create index index_t1_a on t1(a);
create index index_t2_bcd on t2(b, c, d);
-----------------------

Query #4:
select * FROM t1 LEFT JOIN t2 ON t2.a = t1.a ORDER BY t2.b;


Recommendation #1:

create index index_t2_a on t2(a);
-----------------------

Query #5:
select * FROM t1 INNER JOIN t2 ON t1.a = t2.a WHERE t1.b = 5 ORDER BY t1.c;


Recommendation #1:
create index index_t1_bc on t1(b, c);
create index index_t2_a on t2(a);
-----------------------

Query #6:
select * from t where a = 5 and b > 1;

create index index_t_ab on t(a, b);
-----------------------

Query #7:
select * from t where a = 5 and c = 5;

create index index_t_ac on t(a, c);
-----------------------

Query #8:
select * from t where a = 5 and c > 3 and b = 5000;

create index index_t_abc on t(a, b, c);
-----------------------

Query #9:
select * from t where a = 5;

create index index_t_a on t(a);
-----------------------

Query #10:
select * from t where b = 5 and a = 5 and c > 3 order by c, d;
create index index_t_bacd on t(b, a, c, d);
-----------------------

