# executer ce scripts dans un environnement virtuel activer pour mettre ces packages
# installez aussi setuptools via pip
# creer un fichier python et mettez le scripts suivant assurez vous que le fichier soit au meme niveau que manage.py

import pkg_resources
import subprocess

packages = [dist.project_name for dist in pkg_resources.working_set]
subprocess.check_call(["pip","install","--upgrade"] + packages)