Query #1:
SELECT * FROM t1 INNER JOIN t2 ON t1.a = t2.a;


Recommendation #1:
create index index_t1_a on t1(a);


Recommendation #2:

create index index_t2_a on t2(a);
-----------------------

Query #2:
SELECT * FROM t1 INNER JOIN t2 ON t1.a = t2.a WHERE t1.b = 5 ORDER BY t1.c;


Recommendation #1:
create index index_t1_bc on t1(b, c);
create index index_t2_a on t2(a);
-----------------------

Query #3:
SELECT * FROM t1 INNER JOIN t2 ON t1.a = t2.a WHERE t2.b = 5 ORDER BY t2.c;


Recommendation #1:
create index index_t1_a on t1(a);
create index index_t2_bc on t2(b, c);
-----------------------

Query #4:
SELECT * FROM t1 INNER JOIN t2 ON t1.a = t2.a WHERE t1.b > 5;


Recommendation #1:
create index index_t1_ab on t1(a, b);


Recommendation #2:
create index index_t1_b on t1(b);
create index index_t2_a on t2(a);
-----------------------

Query #5:
SELECT * FROM t1 LEFT JOIN t2 ON t1.a = t2.a WHERE t2.b > 5 ORDER BY t1.c;


Recommendation #1:
create index index_t1_c on t1(c);
create index index_t2_ab on t2(a, b);
-----------------------

Query #6:
SELECT * FROM t1 LEFT JOIN t2 ON t1.a = t2.a ORDER BY t2.c;


Recommendation #1:

create index index_t2_a on t2(a);
-----------------------

Query #7:
SELECT * FROM t1 LEFT JOIN t2 ON t1.a = t2.a WHERE t1.b = 5;


Recommendation #1:
create index index_t1_b on t1(b);
create index index_t2_a on t2(a);
-----------------------

Query #8:
SELECT * FROM t1 LEFT JOIN t2 ON t1.a = t2.a WHERE t2.b = 5 ORDER BY t1.c;


Recommendation #1:
create index index_t1_c on t1(c);
create index index_t2_ab on t2(a, b);
-----------------------

Query #9:
SELECT * FROM t1 LEFT JOIN t2 ON t1.a = t2.a WHERE t1.b > 5 ORDER BY t2.c;


Recommendation #1:
create index index_t1_b on t1(b);
create index index_t2_a on t2(a);
-----------------------

Query #10:
SELECT * FROM t1 LEFT JOIN t2 ON t1.a = t2.a WHERE t2.b > 5;


Recommendation #1:
create index index_t1_a on t1(a);
create index index_t2_b on t2(b);

Recommendation #2:

create index index_t2_ab on t2(a, b);
-----------------------

Query #11:
SELECT * FROM t1 RIGHT JOIN t2 ON t1.a = t2.a ORDER BY t1.с;


Recommendation #1:
create index index_t1_a on t1(a);

-----------------------

Query #12:
SELECT * FROM t1 RIGHT JOIN t2 ON t1.a = t2.a WHERE t1.b = 5 ORDER BY t2.c;


Recommendation #1:
create index index_t1_ab on t1(a, b);
create index index_t2_c on t2(c);
-----------------------

Query #13:
SELECT * FROM t1 RIGHT JOIN t2 ON t1.a = t2.a WHERE t2.b = 5;


Recommendation #1:
create index index_t1_a on t1(a);
create index index_t2_b on t2(b);
-----------------------

Query #14:
SELECT * FROM t1 RIGHT JOIN t2 ON t1.a = t2.a WHERE t1.b > 5 ORDER BY t1.c;


Recommendation #1:
create index index_t1_cb on t1(c, b);
create index index_t2_a on t2(a);
-----------------------

Query #15:
SELECT * FROM t1 RIGHT JOIN t2 ON t1.a = t2.a WHERE t2.b > 5 ORDER BY t2.c;

Recommendation #1:
create index index_t1_a on t1(a);
create index index_t2_cb on t2(c, b);
-----------------------

