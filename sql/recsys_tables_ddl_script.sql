/*
 Navicat MySQL Data Transfer

 Source Server         : xg
 Source Server Version : 80013
 Source Host           : 47.244.123.248
 Source Database       : recsys

 Target Server Version : 80013
 File Encoding         : utf-8

 Date: 01/08/2019 21:33:59 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `__comment_test`
-- ----------------------------
DROP TABLE IF EXISTS `__comment_test`;
CREATE TABLE `__comment_test` (
  `ID` varchar(255) NOT NULL,
  `TIME` varchar(255) DEFAULT NULL,
  `MOVIEID` varchar(255) DEFAULT NULL,
  `RATING` varchar(255) DEFAULT NULL,
  `CONTENT` text,
  `CREATOR` varchar(255) DEFAULT NULL,
  `ADD_TIME` varchar(255) DEFAULT NULL,
  `NEWDATA` varchar(5) DEFAULT '0',
  `USERID` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `time_index` (`TIME`),
  KEY `movie_id_index` (`MOVIEID`),
  KEY `rat_index` (`RATING`),
  KEY `new_data_index` (`NEWDATA`),
  KEY `user_id_index` (`USERID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `__ibmovie_2019_1_1_bak`
-- ----------------------------
DROP TABLE IF EXISTS `__ibmovie_2019_1_1_bak`;
CREATE TABLE `__ibmovie_2019_1_1_bak` (
  `id` varchar(50) NOT NULL,
  `movieid` varchar(50) NOT NULL,
  `recmovieid` varchar(50) NOT NULL,
  `recmovierat` varchar(50) NOT NULL,
  `simrat` varchar(50) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `enable` varchar(5) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `movie_id_index` (`movieid`),
  KEY `recmovieid_index` (`recmovieid`),
  KEY `recmovierat_index` (`recmovierat`),
  KEY `simrat_index` (`simrat`),
  KEY `time_index` (`time`),
  KEY `enable_index` (`enable`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `__movie_2018_12_31_bak`
-- ----------------------------
DROP TABLE IF EXISTS `__movie_2018_12_31_bak`;
CREATE TABLE `__movie_2018_12_31_bak` (
  `id` varchar(255) NOT NULL,
  `name` text,
  `ADD_TIME` varchar(255) DEFAULT NULL,
  `type` varchar(500) DEFAULT NULL,
  `actors` varchar(500) DEFAULT NULL,
  `region` varchar(255) DEFAULT NULL,
  `director` varchar(255) DEFAULT NULL,
  `trait` varchar(500) DEFAULT NULL,
  `rat` varchar(50) DEFAULT NULL,
  `enable` varchar(4) DEFAULT '1',
  `description` text NOT NULL,
  `img` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `region_index` (`region`),
  KEY `trait_index` (`trait`) USING BTREE,
  KEY `dir_index` (`director`),
  KEY `rat_index` (`rat`),
  KEY `enable_index` (`enable`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `__movie_2018_12_31_bak_1`
-- ----------------------------
DROP TABLE IF EXISTS `__movie_2018_12_31_bak_1`;
CREATE TABLE `__movie_2018_12_31_bak_1` (
  `id` varchar(255) NOT NULL,
  `name` text,
  `ADD_TIME` varchar(255) DEFAULT NULL,
  `type` varchar(500) DEFAULT NULL,
  `actors` varchar(500) DEFAULT NULL,
  `region` varchar(255) DEFAULT NULL,
  `director` varchar(255) DEFAULT NULL,
  `trait` varchar(500) DEFAULT NULL,
  `rat` varchar(50) DEFAULT NULL,
  `enable` varchar(4) DEFAULT '1',
  `description` text NOT NULL,
  `img` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `region_index` (`region`),
  KEY `trait_index` (`trait`) USING BTREE,
  KEY `dir_index` (`director`),
  KEY `rat_index` (`rat`),
  KEY `enable_index` (`enable`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `__moviedetail`
-- ----------------------------
DROP TABLE IF EXISTS `__moviedetail`;
CREATE TABLE `__moviedetail` (
  `id` varchar(50) DEFAULT NULL,
  `movieid` varchar(50) DEFAULT NULL,
  `description` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `__recmoviedefault`
-- ----------------------------
DROP TABLE IF EXISTS `__recmoviedefault`;
CREATE TABLE `__recmoviedefault` (
  `id` varchar(50) NOT NULL,
  `movieid` varchar(255) DEFAULT NULL,
  `rectime` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `recinfo` varchar(500) DEFAULT '根据Top10%评分',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `comment_new`
-- ----------------------------
DROP TABLE IF EXISTS `comment_new`;
CREATE TABLE `comment_new` (
  `ID` varchar(255) NOT NULL,
  `TIME` varchar(255) DEFAULT NULL,
  `MOVIEID` varchar(255) DEFAULT NULL,
  `RATING` varchar(255) DEFAULT NULL,
  `CONTENT` text,
  `CREATOR` varchar(255) DEFAULT NULL,
  `ADD_TIME` varchar(255) DEFAULT NULL,
  `NEWDATA` varchar(5) DEFAULT '0',
  `USERID` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `time_index` (`TIME`),
  KEY `movie_id_index` (`MOVIEID`),
  KEY `rat_index` (`RATING`),
  KEY `new_data_index` (`NEWDATA`),
  KEY `user_id_index` (`USERID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `config`
-- ----------------------------
DROP TABLE IF EXISTS `config`;
CREATE TABLE `config` (
  `id` varchar(50) NOT NULL,
  `type` varchar(50) NOT NULL,
  `content` text NOT NULL,
  `time` timestamp NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `ibmovie`
-- ----------------------------
DROP TABLE IF EXISTS `ibmovie`;
CREATE TABLE `ibmovie` (
  `id` varchar(50) NOT NULL,
  `movieid` varchar(50) NOT NULL,
  `recmovieid` varchar(50) NOT NULL,
  `recmovierat` varchar(50) NOT NULL,
  `simrat` varchar(50) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `enable` varchar(5) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `movie_id_index` (`movieid`),
  KEY `recmovieid_index` (`recmovieid`),
  KEY `recmovierat_index` (`recmovierat`),
  KEY `simrat_index` (`simrat`),
  KEY `time_index` (`time`),
  KEY `enable_index` (`enable`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `movie`
-- ----------------------------
DROP TABLE IF EXISTS `movie`;
CREATE TABLE `movie` (
  `id` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` text,
  `ADD_TIME` varchar(255) DEFAULT NULL,
  `type` varchar(500) DEFAULT NULL,
  `actors` varchar(500) DEFAULT NULL,
  `region` varchar(255) DEFAULT NULL,
  `director` varchar(255) DEFAULT NULL,
  `trait` varchar(500) DEFAULT NULL,
  `rat` varchar(50) DEFAULT NULL,
  `enable` varchar(4) DEFAULT '1',
  `description` text NOT NULL,
  `img` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `region_index` (`region`),
  KEY `rat_index` (`rat`),
  KEY `enable_index` (`enable`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `mqlog`
-- ----------------------------
DROP TABLE IF EXISTS `mqlog`;
CREATE TABLE `mqlog` (
  `id` varchar(50) NOT NULL,
  `logtype` varchar(50) NOT NULL COMMENT 'm: movie change; u: user action change; c: comment changes',
  `content` text NOT NULL COMMENT 'json detail',
  `time` timestamp NOT NULL,
  `extension` varchar(255) DEFAULT NULL,
  `pulled` varchar(5) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `recmovie`
-- ----------------------------
DROP TABLE IF EXISTS `recmovie`;
CREATE TABLE `recmovie` (
  `id` varchar(50) DEFAULT NULL,
  `userid` varchar(50) DEFAULT NULL,
  `movieid` varchar(255) DEFAULT NULL,
  `rectime` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `lrrat` varchar(255) NOT NULL DEFAULT '0',
  `fmrat` varchar(255) NOT NULL DEFAULT '0',
  `srcmovieid` varchar(255) DEFAULT NULL,
  KEY `userid_index` (`userid`),
  KEY `movie_id_index` (`movieid`),
  KEY `rectime_index` (`rectime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `system_operation_log`
-- ----------------------------
DROP TABLE IF EXISTS `system_operation_log`;
CREATE TABLE `system_operation_log` (
  `id` varchar(50) NOT NULL COMMENT '主键',
  `user_id` varchar(50) NOT NULL COMMENT '用户主键',
  `operation_time` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT '操作时间',
  `client_ip` varchar(50) NOT NULL COMMENT '客户端IP',
  `module` varchar(100) NOT NULL COMMENT '功能模块',
  `operation_type` varchar(100) NOT NULL COMMENT '操作类型',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='系统操作日志';

-- ----------------------------
--  Table structure for `system_operation_param`
-- ----------------------------
DROP TABLE IF EXISTS `system_operation_param`;
CREATE TABLE `system_operation_param` (
  `id` varchar(50) NOT NULL COMMENT '主键',
  `log_id` varchar(50) NOT NULL COMMENT '日志主键',
  `request_param` text COMMENT '请求参数',
  `response_param` text COMMENT '响应结果',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='系统操作参数记录';

-- ----------------------------
--  Table structure for `system_user`
-- ----------------------------
DROP TABLE IF EXISTS `system_user`;
CREATE TABLE `system_user` (
  `id` varchar(50) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `school` varchar(255) DEFAULT NULL,
  `age` varchar(50) DEFAULT NULL,
  `sex` varchar(50) DEFAULT 'male',
  `occupation` varchar(255) DEFAULT NULL,
  `preference` text,
  `region` varchar(255) DEFAULT NULL,
  `is_disabled` tinyint(4) DEFAULT NULL,
  `last_modification_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `userproex_new`
-- ----------------------------
DROP TABLE IF EXISTS `userproex_new`;
CREATE TABLE `userproex_new` (
  `userid` varchar(255) NOT NULL,
  `rmax` double(11,5) NOT NULL,
  `rmin` double(11,5) NOT NULL,
  `ravg` double(11,5) NOT NULL,
  `rcount` double(11,5) NOT NULL,
  `rsum` double(11,5) NOT NULL,
  `rmedian` double(11,5) NOT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
