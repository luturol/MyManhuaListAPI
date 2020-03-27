import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mymanhualist-luturol", 
    version="0.0.1",
    author="Rafael Ahrons",
    author_email="rafael.ahrons@gmail.com",
    description="A my anime list clone that allows you add whatever you want to track",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luturol/MyManhuaListAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)