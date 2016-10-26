from setuptools import setup, find_packages

version = '0.1.3'

setup(
    name='multiqc-alascca',
    version=version,
    author='Daniel Klevebring',
    author_email='daniel.klevebring@ki.se',
    description="QC for the ALASCCA study",
    long_description=__doc__,
    keywords='bioinformatics',
    #    url = 'http://multiqc.info',
    #    download_url = 'https://github.com/ewels/MultiQC/releases',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'jinja2',
        'simplejson',
        'pyyaml',
        'click', 'multiqc', 'pyvcf'
    ],
    entry_points={
        'multiqc.modules.v1': [
            'alasccaqc = alasccaqc.modules.alasccacov:MultiqcModule',
            'hzconcordance = alasccaqc.modules.hzconcordance:MultiqcModule',
            'somaticvariants = alasccaqc.modules.somaticvariants:MultiqcModule',
        ],
        'multiqc.hooks.v1': [
            'after_modules = alasccaqc.hooks:set_sample_status',
        ]

    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: JavaScript',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)
