from setuptools import setup, find_packages

#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 18 february 2023
#--------------------------------------------------------

# using https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html

description="Telegram Bot for system control and runtime notifications"

setup(
    name="hermes",
    py_modules=["hermes"],
    version="2.0",
    description=description,
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/baronefr/hermes",
    author="Francesco Barone",
    license="Open Access",
    python_requires='>=3.5',
    packages=find_packages(),
    install_requires=["pyTelegramBotAPI","termcolor"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Scientists",
        "Programming Language :: Python :: 3",
        "Operating System :: Linux",
    ],
    entry_points={
        "console_scripts": ["hermes=hermes.cli:main", "hermes-setup=hermes.setup:main"],
    },
    scripts=['bin/hermes-start.py'],
)
