import setuptools

with open('requirements.txt') as f:
    requirements = f.readlines()

setuptools.setup(
    name='stratus-api-storage',
    version="0.0.1",
    author="DOT",
    author_email="dot@adara.com",
    description="An API framework for simplified development",
    long_description="Sample",
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/dot-at-adara/storage",
    setup_requires=['pytest-runner'],
    test_requires=[requirements],
    packages=setuptools.find_namespace_packages(include=['stratus_api.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[requirements]
)
