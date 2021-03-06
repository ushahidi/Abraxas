import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons import config
from pylons.controllers.util import abort, redirect

from sqlalchemy import and_, desc, func, or_, select, types

from abraxas.lib.base import BaseController, render
from abraxas.model import Entry
from abraxas.model import Tag
from abraxas.model.meta import Session

log = logging.getLogger(__name__)
entry_table = Entry.table
tag_table = Tag.table

class EntryController(BaseController):

    def index(self, format='html', page=0, tag=None):
        cols = entry_table.c
        query = select([
            cols.id,
            cols.title,
            cols.url,
            cols.tags,
            cols.pubtime,
            cols.host,
            cols.feed_title
        ])
        order_by = cols.pubtime.desc()
        query = query.limit(c.pagesize).offset(c.slicestart)
        query = query.order_by(order_by)
        c.links = Session.execute(query).fetchall()
        c.view = 'latest'
        return render('/links_960.mako')

    def tag(self, keyword, format='html', page=0):
        j = tag_table.join(entry_table, tag_table.c.entry_id==entry_table.c.id)
        cols = entry_table.c
        query = select([
            cols.id,
            cols.title,
            cols.url,
            cols.tags,
            cols.pubtime,
            cols.host,
            cols.feed_title
        ], from_obj=j)
        query = query.where(tag_table.c.lower==keyword.lower())
        query = query.limit(c.pagesize)
        query = query.offset(c.slicestart)
        query = query.order_by(cols.pubtime.desc())
        c.links = Session.execute(query).fetchall()
        c.view = 'tag/%s' % keyword
        return render('/links_960.mako')

