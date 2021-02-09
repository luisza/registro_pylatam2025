#!/bin/bash

coverage run src/manage.py test
coverage html
