python爬虫项目
- 工具:html_util.py
- 依赖:selenium和phantomJS
- 执行方式:
    1. 配置文件:base/config/common_config.py
    2. 创建表,mysql.sql
    3. 执行消费者队列: base/design/mq/action_run.py
    4. 执行爬虫:crawler/mycrawler.py,最好通过定时任务或者线程执行,手动执行要多次执行才行