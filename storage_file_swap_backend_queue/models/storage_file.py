# Copyright 2026 Camptocamp SA
# @author Simone Orsi <simone.orsi@camptocamp.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models
from odoo.exceptions import UserError


class StorageFile(models.Model):
    _inherit = "storage.file"

    def _swap_backend_job(self, dest_backend_id):
        """Job method: swap files to the given backend.

        :return: text summary for the job result UI.
        :raises UserError: if any file swap failed, so the job is marked failed.
        """
        dest_backend = self.env["storage.backend"].browse(dest_backend_id)
        if not dest_backend.exists():
            raise UserError(
                self.env._(
                    "Destination backend id=%(backend_id)d no longer exists.",
                    backend_id=dest_backend_id,
                )
            )
        existing = self.exists()
        moved = existing._swap_backend(dest_backend)
        lines = []
        if moved:
            lines.append(f"Moved to {dest_backend.name} ({len(moved)}):")
            lines.extend(f"  - {r.name} (ID {r.id})" for r in moved)
        if not lines:
            lines.append("Nothing to swap.")
        return "\n".join(lines)
