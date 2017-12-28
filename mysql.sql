
drop TABLE IF EXISTS action_queue;
CREATE TABLE `action_queue` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `action_status` tinyint(4) DEFAULT '1' COMMENT '{1:未执行,0:执行失败,2:执行成功}',
  `fail_num` tinyint(4) DEFAULT '0' COMMENT '总的失败次数',
  `try_num` tinyint(4) DEFAULT '0' COMMENT '失败重试次数',
  `action_str` varchar(500) DEFAULT NULL COMMENT 'action',
  `params` varchar(500) DEFAULT NULL COMMENT '参数',
  `ip` varchar(255) DEFAULT NULL COMMENT '执行任务ip',
  `create_time` datetime DEFAULT NULL COMMENT '任务创建时间',
  `finish_time` datetime DEFAULT NULL COMMENT '任务执行结束时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS web_url_table;
CREATE TABLE `web_url_table` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `url` varchar(255) DEFAULT NULL COMMENT 'url链接',
  `title` VARCHAR(255) DEFAULT NULL COMMENT '当前url的title',
  `content_type` VARCHAR(255) DEFAULT NULL COMMENT '当前url的content_type',
  `referer` VARCHAR(255) DEFAULT NULL COMMENT 'url网站来源',
  `hostname` varchar(50) DEFAULT NULL COMMENT 'url的host',
  `params` varchar(500) DEFAULT NULL COMMENT '参数',
  `md5` varchar(50) NOT NULL UNIQUE COMMENT 'url md5值',
  `url_type` tinyint(4) DEFAULT '0' COMMENT '{0:inter,1:outer}',
  `used` tinyint(4) DEFAULT '0' COMMENT '{0:未使用,1:已使用}',
  `file_path` VARCHAR(255) DEFAULT NULL COMMENT '爬取数据存储的文件路径',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  KEY `md5` (`md5`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
