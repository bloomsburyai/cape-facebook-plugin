# Copyright 2018 BLEMUNDSBURY AI LIMITED
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import subprocess
from package_settings import NAME, VERSION, PACKAGES, DESCRIPTION
from setuptools import setup

# TODO is there a better way ? dependencies seem to always require the version
# Calling only at the egg_info step gives us the wanted depth first behavior
if 'egg_info' in sys.argv and os.getenv('CAPE_DEPENDENCIES', 'False').lower() == 'true':
    subprocess.check_call(['pip3', 'install','--no-warn-conflicts','--upgrade', '-r', 'requirements.txt'])

setup(
    name=NAME,
    version=VERSION,
    long_description=DESCRIPTION,
    author='Bloomsbury AI',
    author_email='contact@bloomsbury.ai',
    packages=PACKAGES,
    include_package_data=True,
    package_data={
        '': ['*.*'],
    },
)
