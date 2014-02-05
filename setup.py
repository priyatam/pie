from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='frozen-pie',
    version='0.4',
    packages=['pie'],
    package_dir={"pie": "pie"},
    package_data={ "pie": ["logging.yml", "controller.js"]},
    url='https://github.com/priyatam/frozen-pie',
    download_url='https://github.com/priyatam/frozen-pie/archive/0.5.tar.gz',
    keywords=["jekyll","static site"],
    license='Apache 2.0 License',
    entry_points={
            'console_scripts': [
                'pie = pie.pie:main',
            ]
    },
    author='Priyatam Mudivarti',
    author_email='priyatam@gmail.com',
    description='Frozen Pie: a Python single-page static site generator',
    install_requires=required,
    classifiers=[
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache License',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Unix',
            'Operating System :: POSIX',
            'Programming Language :: Python',
            'Topic :: Software Development',
            'Topic :: Software Development :: Build Tools',
            'Topic :: Software Development :: Code Generators',
            'Topic :: Internet',
            'Topic :: Internet :: WWW/HTTP :: Site Management',
      ],
)
