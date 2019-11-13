from setuptools import setup, find_packages

setup(
    name='coreui-admin',
    version='1.0',
    description='The `coreui-admin` is the core ui command-line utility for administrative tasks',
    url='https://gitlab.com/Luxoft/coreui-admin',
    author='jryannel',
    author_email='jbocklage-ryannel@luxoft.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Code Generators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
    ],
    keywords='qt auto admin',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'colorlog',
        'click',
        'PyYAML',
        'Jinja2',
        'path.py',
        'sh',
        'wget',
    ],
    entry_points={
        'console_scripts': [
            'coreui-admin = coreuiadmin.admin:app'
        ],
    },
)
