
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
