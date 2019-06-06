from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="modeltranslation-lokalise",
    version="0.1.2",
    description="Integrate django-modeltranslation with lokalise.co",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chisvi/modeltranslation-lokalise",
    download_url="https://github.com/chisvi/modeltranslation-lokalise/archive/0.1.1.tar.gz",
    keywords=['Django', 'django-modeltranslation', 'translation', 'lokalise'],
    author="Sergi Chisvert",
    author_email="chisvi@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Development Status :: 3 - Alpha",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["django", "django-modeltranslation",
                      "djangorestframework", "requests"],
)
