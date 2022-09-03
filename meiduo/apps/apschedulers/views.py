from apscheduler.schedulers.background import BackgroundScheduler
from django.shortcuts import render

from django_apscheduler.jobstores import DjangoJobStore
import logging
from collections import OrderedDict
from django.conf import settings
import os
import time
from django.template import loader
from django_apscheduler.jobstores import register_job

from meiduo.apps.contents.models import ContentCategory

from ..goods.models import GoodsChannel
from ..goods.utils import get_categories

logger = logging.getLogger("django")
scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
scheduler.add_jobstore(DjangoJobStore(), 'default')


@register_job(scheduler, "interval", id="generate_html_task", seconds=60*60,  replace_existing=True)
def generate_static_index_html():
    """
    生成静态的主页html文件
    """
    logger.info('%s: generate_static_index_html》》》》调用生成静态html文件' % time.ctime())
    # 商品频道及分类菜单
    # 使用有序字典保存类别的顺序
    # categories = {
    #     1: { # 组1
    #         'channels': [{'id':, 'name':, 'url':},{}, {}...],
    #         'sub_cats': [{'id':, 'name':, 'sub_cats':[{},{}]}, {}, {}, ..]
    #     },
    #     2: { # 组2
    #
    #     }
    # }
    categories = get_categories()

    # 广告内容
    contents = {}
    content_categories = ContentCategory.objects.all()
    for cat in content_categories:
        contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')
    # 渲染模板
    context = {
        'categories': categories,  # 商品频道数据
        'contents': contents  # 广告数据
    }
    logging.info("《-----加载模版数据完毕 %s" % context)
    # 加载模板文件
    template = loader.get_template('index.html')
    # 渲染模板
    logging.info("《《《------重新渲染模版")
    html_text = template.render(context)
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'index.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_text)
    logging.info("'%s: generate_static_index_html' % time.ctime()》》》》生成静态html成功")


scheduler.start()
