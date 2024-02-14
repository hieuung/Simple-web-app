import json
import os

from contextlib import contextmanager
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.common_utils.exception import APIMessageError

def get_value_by_field(data, filed):
    return data._data[data._fields.index(filed)]

def _get_env_config():
    if 'ENV_CONFIG' not in os.environ:
        raise Exception('Could not find ENV_CONFIG. Ensure "with_env_config: true" is provided in your lambda config')
    
    return json.loads((os.environ['ENV_CONFIG']))


def env_config_fields(*fields):
    def env_config_wrapper(func):
        @wraps(func)
        def _execute(*args, **kwargs):
            config = _get_env_config()

            for field in fields:
                kwargs[field] = config[field]

            return func(*args, **kwargs)

        return _execute

    return env_config_wrapper


@env_config_fields('SQL_URI')
def _get_session_class(SQL_URI):
    engine = create_engine(SQL_URI)
    return sessionmaker(
        bind=engine,
        # Disable this allow to access to object after session is close
        expire_on_commit=False
    )


@contextmanager
def session():
    """Provide a transactional scope around a series of operations."""
    session_class = _get_session_class()
    _session = session_class()
    try:
        yield _session
    finally:
        _session.close()


def with_session(func):
    @wraps(func)
    def with_session_func_wrapper(*args, **kwargs):
        if 'session' in kwargs:
            return func(*args, **kwargs)

        with session() as sess:
            return func(*args, session=sess, **kwargs)

    return with_session_func_wrapper


@contextmanager
def transaction():
    """Provide a transactional scope around a series of operations."""
    session_class = _get_session_class()
    _session = session_class()
    try:
        yield _session
        _session.commit()
    except:
        _session.rollback()
        raise
    finally:
        _session.close()


def with_transaction(func):
    @wraps(func)
    def transaction_func_wrapper(*args, **kwargs):
        if 'session' in kwargs:
            return func(*args, **kwargs)

        with transaction() as sess:
            return func(*args, session=sess, **kwargs)

    return transaction_func_wrapper