#!/usr/bin/env python
import os
from . import celery, init_app

app = init_app('config.ProdConfig')
app.app_context().push()