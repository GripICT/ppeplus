# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
##############################################################################
from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError


class quality_point(models.Model):
    _inherit = 'quality.point'
    
    measure_frequency_unit = fields.Selection([
        ('minutes','Minutes'),
        ('day', 'Days'),
        ('week', 'Weeks'),
        ('month', 'Months')], default="day")
        
    
    def check_execute_now(self):
        self.ensure_one()
        if self.test_type == 'measure':
            if self.measure_frequency_type == 'all':
                return True
            elif self.measure_frequency_type == 'random':
                return (random.random() < self.measure_frequency_value / 100.0)
            elif self.measure_frequency_type == 'periodical':
                delta = False
                if self.measure_frequency_unit == 'minutes':
                    delta = relativedelta(days=self.measure_frequency_unit_value)
                if self.measure_frequency_unit == 'day':
                    delta = relativedelta(days=self.measure_frequency_unit_value)
                elif self.measure_frequency_unit == 'week':
                    delta = relativedelta(weeks=self.measure_frequency_unit_value)
                elif self.measure_frequency_unit == 'month':
                    delta = relativedelta(months=self.measure_frequency_unit_value)
                date_previous = datetime.today() - delta
                checks = self.env['quality.check'].search([
                    ('point_id', '=', self.id),
                    ('create_date', '>=', date_previous.strftime(DEFAULT_SERVER_DATETIME_FORMAT))], limit=1)
                return not(bool(checks))
        return super(quality_point, self).check_execute_now()
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
