from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.session import sessionmaker

from app.core.config import settings

if settings.ENVIRONMENT == "PYTEST":
    async_sqlalchemy_database_uri = settings.TEST_SQLALCHEMY_DATABASE_URI
else:
    async_sqlalchemy_database_uri = settings.ASYNC_DEFAULT_SQLALCHEMY_DATABASE_URI

# 异步数据库连接池会话
async_engine = create_async_engine(async_sqlalchemy_database_uri, pool_pre_ping=True)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
