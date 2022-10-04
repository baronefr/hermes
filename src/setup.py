from setuptools import setup, find_packages

#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 2 october 2022
#--------------------------------------------------------

description="Telegram Bot for system control and runtime notifications"

setup(
    name="hermes",
    version="0.8",
    description=description,
    url="github.com/baronefr/hermes",
    author="Francesco Barone",
    #author_email="@gmail.com",
    license="Open Access",
    python_requires='>=3',
    packages=find_packages(),
    install_requires=["pyTelegramBotAPI"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Scientists",
        "Programming Language :: Python :: 3",
        "Operating System :: Linux",
    ],
)
