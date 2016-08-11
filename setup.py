from setuptools import setup

setup(
    name='gopay-django-api',
    version='0.3',
    license='MIT',
    description='GoPay implemenation of API for Django',
    author='Jan Papousek',
    author_email='jan.papousek@gmail.com',
    url='https://github.com/papousek/gopay-django-api',
    packages=[
        'gopay_django_api',
        'gopay_django_api.management',
        'gopay_django_api.management.commands',
        'gopay_django_api.migrations',
    ],
    install_requires=['clint', 'gopay']
)
