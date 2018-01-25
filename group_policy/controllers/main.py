from odoo import http, _
from odoo.addons.website.models.website import slug
from odoo.http import request
import json
from odoo.addons.website_hr_recruitment.controllers.main import WebsiteHrRecruitment
from odoo.addons.website_form.controllers.main import WebsiteForm

class Submit(WebsiteHrRecruitment):


    @http.route('/jobs/apply/<model("hr.job"):job>', type='http', auth="public", website=True)
    def jobs_apply(self, job, **kwargs):

        res = super(Submit, self).jobs_apply(job)
        print '))))))))))))))'
        user_id = request.env.user
        print user_id
        return res


class Submitbutton(WebsiteForm):

    @http.route('/website_form/<string:model_name>', type='http', auth="public", methods=['POST'], website=True)
    def website_form(self, model_name, **kwargs):
        user_id = request.env.user
        print ')))))', user_id
        if user_id.has_group('group_policy.group_hr_applicant'):
            print 'User have not rights to apply'
            return json.dumps({'id':False})
        return super(Submitbutton, self).website_form(model_name)

    
        