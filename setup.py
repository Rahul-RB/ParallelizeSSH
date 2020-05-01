import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="ParallelizeSSH",
    version="0.0.2",
    author="Rahul R Bharadwaj",
    description="Simple Parallel SSH based on Paramiko backend.",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/Rahul-RB/paramiko-parallel-ssh",
    package_dir={'':'src'},
    packages=setuptools.find_packages("src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
