# -*- coding: utf-8 -*-

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
from pyccuracy.errors import ActionFailedError, LanguageDoesNotResolveError
from pyccuracy.languages import LanguageItem, AVAILABLE_GETTERS, LanguageGetter

ACTIONS = []

class ActionRegistry(object):
    @classmethod
    def suitable_for(cls, line, language, getter=None):
        getter = getter or AVAILABLE_GETTERS[language]

        for Action in ACTIONS:
            regex = Action.regex
            if isinstance(Action.regex, LanguageItem):
                regex = getter.get(Action.regex)
                if regex is None:
                    raise LanguageDoesNotResolveError('The language "%s" does not resolve the string "%s"' % (language, Action.regex))

            matches = re.match(regex, line)
            if matches:
                return Action, matches.groups(), matches.groupdict()

        return None, None, None

class MetaActionBase(type):
    def __init__(cls, name, bases, attrs):
        if name not in ('ActionBase', ):
            if 'execute' not in attrs:
                raise NotImplementedError("The action %s does not implements the method execute()", name)
            if 'regex' not in attrs:
                raise NotImplementedError("The action %s does not implements the attribute regex", name)

            if not isinstance(attrs['regex'], basestring):
                regex = attrs['regex']
                raise TypeError("%s.regex attribute must be a string, got %r(%r)." % (regex.__class__, regex))

            # registering
            ACTIONS.append(cls)

        super(MetaActionBase, cls).__init__(name, bases, attrs)

class ActionBase(object):
    __metaclass__ = MetaActionBase
    ActionFailedError = ActionFailedError

    @classmethod
    def can_resolve(cls, string):
        return re.match(cls.regex, string)

    def execute_action(self, line, context, getter=None):
        # the getter is here for unit testing reasons
        Action, args, kwargs = ActionRegistry.suitable_for(line, context.get_language(), getter=getter)
        if isinstance(self, Action):
            raise RuntimeError('A action can not execute itself for infinite recursion reasons :)')
