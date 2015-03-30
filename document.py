import uuid
import hashlib
import mimetypes
import couchdb
import urllib
import os
import base64

class Document(object):
    uuid = uuid.uuid4()

    def __init__(self, path):
        self.path = path
        self.hash = self.buid_hash()
        self.mime = mimetypes.guess_type(urllib.pathname2url(path))[0]
        self.id = hashlib.sha1("%s:%s" % (self.path, self.mime)).hexdigest()
        self.basename = os.path.basename(self.path)


    def buid_hash(self):
        return hashlib.md5(open(self.path, 'rb').read()).hexdigest()


class CouchdbDocument(Document):
    def __init__(self, *args, **kwargs):
        super(CouchdbDocument, self).__init__(*args, **kwargs)
        self.couch = couchdb.Server("http://127.0.0.1:5984/")
        self.db = self.couch['test']

    def upload_file(self):
        name = base64.b64encode(self.basename)
        self.db.put_attachment(self.doc, open(self.path, 'r'), name, self.mime)

    def save(self):
        data = dict(uuid=str(self.uuid), hash=self.hash, raw_path=self.path, path=os.path.split(self.path))
        print self.path

        if self.id in self.db:
            self.doc = self.db[self.id]
        else:
            self.db[self.id] = data
            self.doc = self.db[self.id]

        if self.basename in self.doc.get('_attachments', {}):
            if self.hash != self.doc['hash']:
                self.upload_file()
        else:
            self.upload_file()
