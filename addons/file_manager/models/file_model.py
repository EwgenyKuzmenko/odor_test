from odoo import models, fields, api
import base64
import os

class FileModel(models.Model):
    _name = 'file.model'
    _description = 'File Model'

    name = fields.Char(string="File Name", required=True)
    file = fields.Binary(string="File")
    file_path = fields.Char(string="File Path")
    store_in_db = fields.Boolean(string="Store in Database", default=True)

    @api.model
    def create(self, vals):
        if not vals.get('store_in_db') and vals.get('file'):
            file_content = base64.b64decode(vals['file'])
            file_path = f"/var/lib/odoo/{vals['name']}"
            with open(file_path, 'wb') as f:
                f.write(file_content)
            vals['file_path'] = file_path
            vals['file'] = False
        return super(FileModel, self).create(vals)

    def unlink(self):
        for record in self:
            if not record.store_in_db and record.file_path:
                os.remove(record.file_path)
        return super(FileModel, self).unlink()
