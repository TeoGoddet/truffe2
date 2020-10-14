#!/bin/bash

set -e
set +x

project_dir=$(dirname $(dirname $(readlink -f "$0")))
rm -rf $project_dir/venv

python2 -m virtualenv $project_dir/venv

. $project_dir/venv/bin/activate
pip install -U pip
pip install -r $project_dir/truffe2/data/pip-reqs.txt

rm -rf $project_dir/truffe2/db.sqlite3
cp $project_dir/tools/settingsLocal.py.test $project_dir/truffe2/app/settingsLocal.py

(
	cd $project_dir/truffe2
	python manage.py syncdb
	python manage.py migrate
	echo "update users_truffeuser set is_superuser=1 where id=1;" | sqlite3 truffe2/db.sqlite3
)