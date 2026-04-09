# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

from odoo.tools.sql import column_exists

_logger = logging.getLogger(__name__)


def pre_init_hook(env):
    """Pre init hook."""
    # add columns for computed fields to avoid useless computation by the ORM
    # when installing the module
    cr = env.cr
    if not column_exists(cr, "ir_attachment", "fs_storage_id"):
        _logger.info("Add columns for computed fields on ir_attachment")
        cr.execute(
            """
            ALTER TABLE ir_attachment
            ADD COLUMN fs_storage_id INTEGER;
            ALTER TABLE ir_attachment
            ADD FOREIGN KEY (fs_storage_id) REFERENCES fs_storage(id);
            """
        )
        cr.execute(
            """
            ALTER TABLE ir_attachment
            ADD COLUMN fs_url VARCHAR;
            """
        )
        cr.execute(
            """
            ALTER TABLE ir_attachment
            ADD COLUMN fs_storage_code VARCHAR;
            """
        )
        _logger.info("Columns added on ir_attachment")
    # Always ensure base_url_for_files exists on fs_storage
    if not column_exists(cr, "fs_storage", "base_url_for_files"):
        _logger.info("Add column for computed field on fs_storage")
        cr.execute(
            """
            ALTER TABLE fs_storage
            ADD COLUMN base_url_for_files VARCHAR;
            """
        )
        _logger.info("Column added on fs_storage")
