import os
import unittest

from gdo.base.Application import Application
from gdo.base.ModuleLoader import ModuleLoader
from gdo.base.Util import module_enabled
from gdo.core.GDO_Session import GDO_Session
from gdotest.TestUtil import web_plug, reinstall_module, web_gizmore, install_module, GDOTestCase


class CaptchaTest(GDOTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        Application.init(os.path.dirname(__file__ + "/../../../../"))
        Application.init_cli()
        install_module('captcha')
        loader = ModuleLoader.instance()
        loader.load_modules_db()
        loader.init_modules(load_vals=True)
        Application.set_session(GDO_Session.for_user(web_gizmore()))

    async def test_00_install(self):
        reinstall_module('captcha')
        self.assertTrue(module_enabled('captcha'), 'cannot install captcha')

    async def test_01_form_rendering(self):
        out = web_plug('captcha.render.txt').exec()
        self.assertTrue(out.startswith(b'GIF87a'), 'CaptchaTest does not render captcha')


if __name__ == '__main__':
    unittest.main()
