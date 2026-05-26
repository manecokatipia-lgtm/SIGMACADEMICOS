from peewee import *
db=SqliteDatabase('escola.db',  timeout=10,  pragmas=[
        ('journal_mode', 'wal'),
        ('cache_size', -1024 * 64),   # exemplo: otimizar cache
        ('foreign_keys', 1),          # garantir integridade referencial
        ('ignore_check_constraints', 0)
    ],check_same_thread=False)