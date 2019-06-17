from setuptools import setup, find_packages

setup(
    name='lr1',
    version='0.1.0',
    description='LR1 huffman code encoder/decoder',
    author='McWladkoE',
    author_email='svevladislav@gmail.com',
    url='',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[],
    entry_points="""\
        [console_scripts]
        lr1 = samotoy.main:main
    """,
)
