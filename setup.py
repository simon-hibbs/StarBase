from distutils.core import setup
import py2exe

setup(name='StarBase',
      version='0.47',
      author='Simon D. Hibbs',
      windows=[{'script' : 'Starbase.pyw'}],
      options={'py2exe' : {'includes' : ['sip'], 'bundle_files' : '1'}},
      scripts=['log.py'],
      data_files=[('', ['projects.ini',
                        'WorldNames.txt']),
                  ('plugins', ['plugins/blank.py',
                               'plugins/blank.yapsy-plugin',
                               'plugins/rikitiki.py',
                               'plugins/rikitiki.yapsy-plugin'])]
      )
