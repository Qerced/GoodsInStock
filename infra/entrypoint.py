import asyncio
import logging
import os
from argparse import ArgumentParser, ArgumentTypeError

import asyncpg
import uvicorn
from dotenv import load_dotenv

from alembic import command, config

load_dotenv()

DATABASE_URL = 'postgresql://{user}:{password}@{host}:{port}/{db_name}'

WAITING_POSTGRES = 'Waiting for PostgreSQL connection...'
POSTGRES_CONNECTED = 'PostgreSQL is ready'
POSTGRES_NOT_READY = 'PostgreSQL is not ready, retrying in 5 seconds...'
ARGUMENT_ERROR = 'Use required flag --app'

logging.basicConfig(
    level=logging.DEBUG, format='[%(asctime)s] [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


async def waiting_database():
    logger.debug(WAITING_POSTGRES)
    while True:
        try:
            conn = await asyncpg.connect(DATABASE_URL.format(
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                db_name=os.getenv('POSTGRES_DB')
            ))
            logger.debug(POSTGRES_CONNECTED)
            break
        except ConnectionRefusedError:
            logger.warning(POSTGRES_NOT_READY)
            await asyncio.sleep(5)
    await conn.close()


def run_app():
    asyncio.get_event_loop().run_until_complete(waiting_database())
    command.upgrade(config.Config('./alembic.ini'), 'head')
    uvicorn.run(
        'app.main:app', host='0.0.0.0', port=int(os.getenv('APP_PORT'))
    )


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--prod', action='store_true')
    parser.add_argument(
        '--app', dest='func', action='store_const', const=run_app
    )
    args = parser.parse_args()
    if args.prod:
        os.environ['DEBUG'] = 'False'
    if func := args.func:
        func()
    else:
        raise ArgumentTypeError(ARGUMENT_ERROR)
