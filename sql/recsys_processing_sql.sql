-- 根据rectime排序从最近开始，给定用户ID，即查询用户推荐的电影； 其中recmovie表中是推荐的电影列表
select * from recmovie inner JOIN movie on recmovie.movieid = movie.id and recmovie.userid=1 and movie.enable = 1 ORDER BY rectime DESC, rat DESC limit 0, 30
-- delete from recmovie where movieid not in (select id from movie)
select * from comment_new limit 0, 100
select *,MD5(creator) as userid from comment limit 0,100
-- 更新userid语句
-- update comment_new,comment set comment_new.userid=md5(comment.creator) from comment where comment_new.id=comment.id
select count(*) from comment_new
-- 查看是否重复ID
select count(DISTINCT id) from comment
-- 处理userid
update comment_new s set userid = (select md5(creator) from comment where id = s.id);
-- 检查异常数据
select count(*) from comment where creator='' or creator is null
-- 检查数据处理的正确性
select count(*),MD5(creator) as userid_c,userid, MOVIEID, creator from comment_new where creator='windyxp' group by userid_c
select count(*),MD5(creator) as userid_c,userid, MOVIEID, creator from comment_new where creator='windyxp'
select MD5(creator) as userid_c,userid, MOVIEID, creator from comment_new where creator='windyxp' 
-- 查看评分的幅度
select max(rating) from comment
-- 处理comment抓取的数据
select count(*) from comment where comment.MOVIEID in (select id from movie)
select count(*) from movie
-- 删除无用数据
-- delete  from comment where comment.MOVIEID not in (select id from movie)
select count(*) as cnt,creator from comment where creator not like '%已注销%' group by creator order by cnt desc limit 0,100
select * from comment_new limit 0, 100
select * from movie limit 0, 100
select * from movie where id = 1294829
select count(*) from comment_new where creator='妖怪dodo' 
select * from comment_new where creator='妖怪dodo' 
select * from comment_new where creator='妖怪dodo'  order by time
select * from comment_new where creator='妖怪dodo'  group by content, movieid order by time
select * from comment_new where creator='米粒'  order by time
select * from comment_new where creator='米粒'  group by content, movieid order by time
select * from comment_new where creator='麦克阿瑟'  group by content, movieid order by time
select * from comment_new where creator='麦克阿瑟'  order by time
select sum(rating)/count(rating) from comment_new where creator='妖怪dodo'
select * from comment_new group by content, movieid limit 500,100
-- select avg(rating) from comment where creator = '麦克阿瑟'
-- 中位数，平均数，最大评分，最小评分
select count(DISTINCT userid) from comment_new
select * from movie limit 0,100
select count(*) from userproex where userid='12'
select DISTINCT userid from comment_new where userid is not null
select rating from comment_new where userid='0a87619cd22313468311d7077dd8a35c'
select max(rating) as rmax, min(rating) as rmin, avg(rating) as ravg, count(rating) as rcount, sum(rating) as rsum from comment_new where userid='0a87619cd22313468311d7077dd8a35c' 
select count(*) from userproex
-- 统计特征
-- delete from userproex_new
-- INSERT INTO userproex_new (userid, rmax, rmin, ravg, rcount, rsum) (select userid, max(rating) as rmax, min(rating) as rmin, avg(rating) as ravg, count(rating) as rcount, sum(rating) as rsum from comment_new group by userid having userid is not null)
select * from userproex_new limit 0,100
select * from userproex where userid='00000bc601790de1bafd1914e2cd9abb'
select count(*) from userproex_new where rmedian>0
select userid from userproex_new where rmedian=0
select * from comment_new where movieid='10533913' and rating=3 limit 0,100
select count(*) from comment_new where rating = 3
select * from ibmovie order by movieid LIMIT 0,1000
select * from movie where id='1794438'
select cnt,movieid from (select count(*) as cnt,movieid from ibmovie group by movieid) as t where cnt < 200
select * from ibmovie   order by time desc limit 0,1
insert into ibmovie (id, movieid, recmovieid, recmovierat, simrat, time, enable) values ('c29197ff-e469-4d7e-90cf-af5991ab87b2','1795628','1296049','7.7','0.466998209110974','2018-12-21 05:26:02.907768','1')
select id from movie
select count(*) from ibmovie
select * from comment_new limit 0, 100
select count(*) from comment_new
-- **************** 开发测试使用 ****************
select * from movie limit 0, 100
-- 查询一个电影的相似电影
select * from ibmovie left join movie on ibmovie.recmovieid = movie.id where ibmovie.movieid = '10521893'
select count(*) from ibmovie
select * from movie left join moviedetail on movie.id=moviedetail.id 
select * from moviedetail
select max(cnt) from (select count(*) as cnt from comment_new group by movieid) t
select * from system_user
select * from comment_test where USERID='1'
select * from comment_new limit 0, 10
select * from comment_new left join movie on comment_new.MOVIEID = movie.id where userid='cf2349f9c01f9a5cd4050aebd30ab74f'
select * from movie where id = '10428476'
select id from system_user
select * from userproex_new where userid = 'cf2349f9c01f9a5cd4050aebd30ab74f'
select * from movie where id in (select DISTINCT movieid from recmovie where userid='cf2349f9c01f9a5cd4050aebd30ab74f')
select * from comment_new limit 0,1 
select * from recmovie left join movie on movie.id=recmovie.movieid left join userproex_new on userproex_new.userid=recmovie.userid 
where recmovie.userid = 'cf2349f9c01f9a5cd4050aebd30ab74f'
update recmovie set recmovie.fmrat = 0.1 where id = 1
select id from recmovie where userid='cf2349f9c01f9a5cd4050aebd30ab74f' and movieid='10430817'
select * from recmovie
select count(*) from recmovie
select * from recmovie left join movie on movie.id=recmovie.movieid left join userproex_new on userproex_new.userid=recmovie.userid 
select * from comment_new where newdata = 1 
select DISTINCT recmovieid from ibmovie where movieid = '10746430'
select * from system_user
select * from comment_new where userid = 'cf2349f9c01f9a5cd4050aebd30ab74f' 
-- insert into comment_new (ID, TIME, MOVIEID, RATING, CONTENT, CREATOR, ADD_TIME, NEWDATA, USERID)
-- VALUES ('300004', '2018-12-29 13:09:21', '1296384', 4, '中等', 'wuenda', '2018-12-29 13:09:21', '1', 'cf2349f9c01f9a5cd4050aebd30ab74f')
-- update comment_new set newdata = 0 where id = '300001'
-- update comment_new set newdata = 2 where id = '300004'
-- insert into recmovie (id, userid, movieid, rectime) values ('7', 'cf2349f9c01f9a5cd4050aebd30ab74f', '10430817', '2018-12-27 21:09:21')
select count(*) from movie where description is null or description = ''
select * from movie limit 0,1000
select count(*) from movie
select * from system_user
select * from __comment_test limit 0, 1
select * from comment_new limit 0, 1
select * from mqlog where pulled = 0
-- select * from mqlog where logtype = 'u' and pulled = 0
-- update mqlog set pulled = 0 where pulled = 1 and logtype='u'
select * from userproex_new where userid = '7c561cbe-f463-4185-844c-a317bc02788a'
select * from userproex_new where userid = '1'
select count(*) from movie
select escape(description) from movie limit 0,1
select * from mqlog where logtype = 'm' and pulled = 0
update mqlog set pulled = 0 where logtype = 'm'
select * from movie where name like '%Aquaman%'
select * from comment_new where userid is null or userid = ''
select * from movie where  id = '4301274'
select * from mqlog
select * from recmovie
select count(*) from ibmovie
select convert(simrat, DECIMAL(5,5)) from ibmovie limit 0, 1
select id,simrat,convert(simrat , DECIMAL(5,5)) as simrat_5 from ibmovie where movieid = '10746430' order by convert(simrat , DECIMAL(5,5)) desc limit 0,10
select * from ibmovie where simrat like '%e-%'
select * from movie where id = 'ce2ab2e8-4ee6-4b92-bdfe-3d40b6622b77'
select * from movie where id = '0849b8cb-a9e2-4c81-b1f3-04f699f002db'
select * from ibmovie where movieid = '0849b8cb-a9e2-4c81-b1f3-04f699f002db'
select max(convert(simrat, DECIMAL(5,5))) from ibmovie
select * from comment_new where id = 'add4da0e-86a1-411c-9411-7ac605a615c0'
select * from mqlog where logtype = 'c' and pulled = 0
select * from comment_new where newdata = 1
select * from comment_new where id in ('add4da0e-86a1-411c-9411-7ac605a615c0','9c9d2ffc-22a9-40ce-83ac-33400ead121d','b3f815c3-5d5f-4369-90db-590f06014ee0','4bcc19dc-2b9e-4e80-9748-665022db2508','dfce4112-cb1e-4ee6-9441-9211ee385e87')
('add4da0e-86a1-411c-9411-7ac605a615c0','9c9d2ffc-22a9-40ce-83ac-33400ead121d','b3f815c3-5d5f-4369-90db-590f06014ee0','4bcc19dc-2b9e-4e80-9748-665022db2508','dfce4112-cb1e-4ee6-9441-9211ee385e87')
select * from comment_new where id in ('add4da0e-86a1-411c-9411-7ac605a615c0','9c9d2ffc-22a9-40ce-83ac-33400ead121d','b3f815c3-5d5f-4369-90db-590f06014ee0','4bcc19dc-2b9e-4e80-9748-665022db2508','dfce4112-cb1e-4ee6-9441-9211ee385e87')
select * from config where type = 'csv_last_url'

-- delete from recmovie 
select count(*) from recmovie where userid='7c561cbe-f463-4185-844c-a317bc02788a'
select * from recmovie inner JOIN movie on recmovie.movieid = movie.id and recmovie.userid=1 and movie.enable = 1 ORDER BY fmrat DESC, lrrat DESC,rectime DESC, rat DESC limit 48, 12
select count(*) from (select DISTINCT userid from comment_new)
select * from comment_new limit 1, 10
update recmovie set recmovie.fmrat = 1,rectime='2019-01-03 11:31:07.410736' where id = 1
update recmovie set recmovie.fmrat = 1 where id = '1'
select * from mqlog where pulled = 0
select * from comment_new where userid = 'cf2349f9c01f9a5cd4050aebd30ab74f'
select * from movie where id = '1293345'
select * from movie where id = '22939161'
select * from system_user
select * from movie where id = '46c1406a-fcc3-4746-8d7b-343abfa7fb48'
select * from mqlog where pulled = 0
select * from comment_new left join movie on comment_new.movieid = movie.id where userid='7c561cbe-f463-4185-844c-a317bc02788a' -- group by comment_new.movieid
update recmovie set recmovie.fmrat = 2.5249200000000003,rectime='2019-01-05 10:42:07' where id = '032d13e1-8bc6-440f-8e1f-accfa2fd13b1'
select * from comment_new where userid= 'b1580ce1-f9a3-4bfe-a50b-4a0c1fa752e7'
select DISTINCT userid from comment_new
select DISTINCT username from recmovie left join system_user on recmovie.userid=system_user.id where userid = '1'
select * from movie where id = '26344688'
select * from movie left join comment_new on comment_new.movieid = movie.id where comment_new.userid=1
select * from comment_new where userid=1
select * from system_user
