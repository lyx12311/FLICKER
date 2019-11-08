from setuptools import setup

with open("FLICKER/version.py", "r") as f:
    exec(f.read())

setup(name='FLICKER_calc',
      version=__version__,
      description='Calculate Flicker value for lightcurve(s) from one or more observating quarters.',
      url='https://github.com/lyx12311/FLICKER',
      author='Yuxi(Lucy) Lu',
      author_email='lucylulu12311@gmail.com',
      license=' ',
      packages=['FLICKER'],
      install_requires=['numpy', 'pandas'],
      zip_safe=False)
