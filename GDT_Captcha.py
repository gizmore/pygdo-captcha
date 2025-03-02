from gdo.base.Application import Application
from gdo.base.Util import href
from gdo.core.GDT_Field import GDT_Field
from gdo.core.GDT_Template import GDT_Template
from gdo.core.WithLabel import WithLabel
from gdo.form.GDT_Form import GDT_Form


class GDT_Captcha(GDT_Field):

    def __init__(self, name: str = 'captcha'):
        super().__init__(name)
        self.label('module_captcha')

    ############
    # Validate #
    ############
    def validate(self, val: str | None, value: any) -> bool:
        if Application.is_unit_test():
            return True
        session = Application.get_session()
        correct = session.get('captcha')
        if val is None:
            return self.error_not_null()
        if val.upper() == correct:
            session.set('captcha_solved', correct)
            return True
        return self.error('err_captcha')

    def gdo_form_validated(self, form: GDT_Form):
        Application.get_session().remove('captcha_solved')

    ##########
    # Render #
    ##########
    def render_form(self) -> str:
        old = Application.get_session().get('captcha_solved') or ''
        return GDT_Template.python('captcha', 'captcha_form.html', {
            "href": href('captcha', 'render', '', 'txt'),
            "field": self,
            "old": old,
        })

