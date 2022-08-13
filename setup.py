import setuptools

#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 26 july 2022
#--------------------------------------------------------

description="Telegram bot for control and notifications."

setuptools.setup(
    name="hermes",
    version="0.5",
    author="Barone F.P.",
    description=description,
    url="github.com/baronefr/",
    packages=setuptools.find_packages(),
    install_requires=['pyTelegramBotAPI'],
    python_requires='>=3',
    license='Open Access',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Scientists",
        "Topic :: Physics :: Dynamical systems",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
