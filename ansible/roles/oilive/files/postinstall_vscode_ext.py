#!/usr/bin/env python3

import argparse
import json
import os
from pathlib import Path
from urllib.request import urlretrieve
import zipfile

parser = argparse.ArgumentParser(
    description='Finish the installation of a VS code extension for offline use')
parser.add_argument('extension_name', help='codename of the extension to install')

args = parser.parse_args()
name = args.extension_name
extensions_path = Path.home() / '.vscode' / 'extensions'
basepath = [p for p in extensions_path.iterdir() if name in str(p)][0]
package_file_path = basepath / 'package.json'

with open(package_file_path, 'r', encoding='utf-8') as in_file:
    data = json.load(in_file)
    if 'runtimeDependencies' in data:
        for dep in data['runtimeDependencies']:
            if 'linux' in dep['platforms'] and \
                    ('architectures' not in dep or 'x86_64' in dep['architectures']):
                print(f"Installing {dep['description']}...")
                filename, _ = urlretrieve(dep['url'])
                install_path = basepath
                if 'installPath' in dep:
                    install_path = basepath / dep['installPath']
                    if not install_path.exists():
                        install_path.mkdir()
                zip_ref = zipfile.ZipFile(filename)
                zip_ref.extractall(install_path)
                zip_ref.close()
                os.unlink(filename)
                lock_file = basepath / 'install.lock'
                lock_file.touch()
