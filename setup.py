from distutils.core import setup

setup(
    name='frozen-pie',
    version='0.4',
    packages=['frozenpie'],
    package_dir={"frozenpie": "frozenpie"},
    package_data={ "frozenpie": ["logging.yml"]},
    url='https://github.com/priyatam/frozen-pie',
    download_url='https://github.com/priyatam/frozen-pie/archive/0.5.tar.gz',
    scripts=["scripts/pie"],
    keywords=["jekyll","static site"],
    license='Apache 2.0 License',
    author='Priyatam Mudivarti',
    author_email='priyatam@gmail.com',
    description='Frozen Pie: a Python single-page static site generator'
)
