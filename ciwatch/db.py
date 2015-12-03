# Copyright (c) 2015 Tintri. All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


from ciwatch.config import Config
from ciwatch import models


config = Config()
engine = create_engine(config.cfg.database.connection, pool_recycle=3600)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
models.Base.metadata.create_all(engine)


def create_projects():
    for name in config.get_projects():
        get_or_create(models.Project,
                      commit_=False,
                      name=name)
    Session().commit()


def update_or_create_comment(commit_=True, **kwargs):
    session = Session()
    comment = session.query(models.Comment).filter_by(
        ci_server_id=kwargs['ci_server_id'],
        patch_set_id=kwargs['patch_set_id']).scalar()
    if comment is not None:
        for key, value in kwargs.iteritems():
            setattr(comment, key, value)
    else:
        session.add(models.Comment(**kwargs))
    if commit_:
        session.commit()


def get_or_create(model, commit_=True, **kwargs):
    session = Session()
    result = session.query(model).filter_by(**kwargs).first()
    if not result:
        result = model(**kwargs)
        session.add(result)
        if commit_:
            session.commit()
    return result


def get_projects():
    return Session().query(models.Project).order_by(models.Project.name).all()


def get_ci_servers():
    return Session().query(models.CiServer).order_by(
        desc(models.CiServer.trusted), models.CiServer.name).all()


def get_patch_sets(project, since):
    return Session().query(models.PatchSet).filter(
        and_(models.PatchSet.project == project,
             models.PatchSet.created >= since)
        ).order_by(models.PatchSet.created.desc()).all()


def get_project(project_name):
    return Session().query(models.Project).filter(
        models.Project.name == project_name).one()
