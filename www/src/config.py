# -*- coding: utf-8 -*-


"""
    flask config
"""
# cookie
SECRET_KEY = 'qweasdzxcrty'

"""
    app config
"""
# mongodb
MONGODB_URI = 'mongodb://mongodb:27017/'
MONGODB_STOREDB_NAME = 'scrapy'
MONGODB_SCOREDB_NAME = 'score'
MONGODB_USER = 'flask'
MONGODB_PWD = 'flask'

# grpc
GRPC_HOST = 'spider:50051'

# category
ARTICLE_CATEGORIES = {
        '技术',
        'python',
        '数据库',
        '安全',
        '科技',
        '新闻',
        '漫画',
}
