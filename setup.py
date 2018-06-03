from setuptools import setup

setup(
    name="pagarme-conciliator",
    version="0.1",
    description="Pagar.me Conciliator",
    author="Gabriel Salla",
    author_email="gabriel.c.salla@gmail.com",
    packages=["src"],
    install_requires=[
        "peewee",
        "peewee-async",
        "aiopg",
        "aiohttp",
        "pytz",
        "inquirer"
    ]
)
