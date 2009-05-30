#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Bernardo Heynemann <heynemann@gmail.com>
# Copyright (C) 2009 Gabriel Falcão <gabriel@nacaolivre.org>
#
# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.opensource.org/licenses/osl-3.0.php
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pmock import *

from pyccuracy import Page
from pyccuracy.common import Settings
from pyccuracy.actions.core.page_actions import *

class FakeContext(object):
    settings = Settings(cur_dir='/')
    browser_driver = Mock()

def test_page_go_to_action_calls_the_right_browser_driver_methods():

    context = FakeContext()
    context.browser_driver.expects(once()) \
                          .page_open(eq("some_url"))

    context.browser_driver.expects(once()) \
                          .wait_for_page()

    action = PageGoToAction()

    action.execute(context, url="some_url")
    context.browser_driver.verify()

def test_page_go_to_action_sets_context_current_url():
    context = FakeContext()

    context.browser_driver.expects(once()) \
                          .page_open(eq("some_url"))
    context.browser_driver.expects(once()) \
                          .wait_for_page()

    action = PageGoToAction()

    action.execute(context, url="some_url")
    context.browser_driver.verify()

    assert context.url == "some_url"

def test_page_go_to_action_sets_page_if_page_is_supplied():
    class SomePage(Page):
        url = "some"

    context = FakeContext()

    context.browser_driver.expects(once()) \
                          .page_open(eq("some"))
    context.browser_driver.expects(once()) \
                          .wait_for_page()

    action = PageGoToAction()

    action.execute(context, url="Some Page")
    context.browser_driver.verify()

    assert isinstance(context.current_page, SomePage)

def test_page_am_in_action_calls_the_right_browser_driver_methods():
    class SomePage(Page):
        url = "some"

    context = FakeContext()

    context.browser_driver.expects(once()) \
                          .page_open(eq("some"))
    context.browser_driver.expects(once()) \
                          .wait_for_page()

    action = PageAmInAction()

    action.execute(context, url="Some Page")
    context.browser_driver.verify()

def test_page_am_in_action_sets_page_if_page_is_supplied():
    class SomePage(Page):
        url = "some"

    context = FakeContext()

    context.browser_driver.expects(once()) \
                          .page_open(eq("some"))
    context.browser_driver.expects(once()) \
                          .wait_for_page()

    action = PageAmInAction()

    action.execute(context, url="Some Page")
    context.browser_driver.verify()
    assert isinstance(context.current_page, SomePage)
    assert context.url == "some"

