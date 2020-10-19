#!/bin/bash

set -e
set +x

project_dir=$(dirname $(dirname $(readlink -f "$0")))

if [ "$1" != "noclean" ]
then
	rm -rf $project_dir/venv
	python2 -m virtualenv $project_dir/venv

	. $project_dir/venv/bin/activate
	pip install -U pip
	pip install -r $project_dir/truffe2/data/pip-reqs.txt
else
	. $project_dir/venv/bin/activate
fi

rm -rf $project_dir/truffe2/db.sqlite3
cp $project_dir/tools/settingsLocal.py.test $project_dir/truffe2/app/settingsLocal.py

(
	cd $project_dir/truffe2
	python manage.py syncdb
	python manage.py migrate
	if [ "$2" == "demo" ]
	then
		echo 'from main.test_data import initial_data; initial_data()' | python manage.py shell
	fi
)