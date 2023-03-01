from setuptools import setup, find_packages

#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 18 february 2023
#--------------------------------------------------------

description="Telegram Bot for system control and runtime notifications."

def read_version(fname="hermes/version.py"):
    exec(compile(open(fname, encoding="utf-8").read(), fname, "exec"))
    return locals()["__version__"]


setup(
    name="hermes",
    py_modules=["hermes"],
    version=read_version(),
    description=description,
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/baronefr/hermes",
    author="Francesco Barone",
    license="CC BY-NC-ND",
    python_requires='>=3.5',
    packages=find_packages(),
    install_requires=["pyTelegramBotAPI","termcolor"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Operating System :: Linux",
    ],
    entry_points={
        "console_scripts": ["hermes=hermes.cli:main", "hermes-setup=hermes.setup:main"],
    },
    scripts=['bin/hermes-start.py'],
)
