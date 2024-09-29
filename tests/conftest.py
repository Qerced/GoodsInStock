from pathlib import Path

import pytest
import pytest_asyncio
from mixer.backend.sqlalchemy import Mixer as _mixer
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

try:
    from app.main import app  # noqa
except (NameError, ImportError):
    raise AssertionError('Не обнаружен объект приложения `app`.')

try:
    from app.core.db import Base, get_async_session  # noqa
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружены объекты `Base, get_async_session`. '
    )

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

pytest_plugins = ['fixtures.data',]

TEST_DB = BASE_DIR / 'test.db'
SQLALCHEMY_DATABASE_URL = f'sqlite+aiosqlite:///{str(TEST_DB)}'
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(class_=AsyncSession, bind=engine)


async def override_db():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def mixer():
    mixer_engine = create_engine(f'sqlite:///{str(TEST_DB)}')
    session = sessionmaker(bind=mixer_engine)
    return _mixer(session=session(), commit=True)
