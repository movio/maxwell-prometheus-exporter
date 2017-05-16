from setuptools import setup, find_packages

setup(
    name='maxwell-prometheus-exporter',
    version='0.3.2',
    description='Maxwell metrics Prometheus exporter',
    url='https://github.com/movio/maxwell-prometheus-exporter',
    author='Nicolas Maquet and Nan Wu',
    author_email='nicolas@movio.co, nan@movio.co',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Monitoring',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='monitoring prometheus exporter maxwell',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'configparser',
      # 'mysql-connector-python',
        'prometheus-client>=0.0.13'
    ],
    entry_points={
        'console_scripts': [
            'maxwell-prometheus-exporter=exporter:main',
        ],
    },
)
