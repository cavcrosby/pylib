#!/usr/bin/env python3
# Standard Library Imports
import argparse

# Third Party Imports

# Local Application Imports


class CustomHelpFormatter(argparse.HelpFormatter):
    """A custom HelpFormatter subclass used by argparse.ArgumentParser objects.

    Changes from the original argparse.HelpFormatter are: the format of the
    option string(s) with there argument(s), see '_format_action_invocation'.
    Options are now organized in alphabetical order for their help messages
    but not in the usage str for their parser. This is more so to follow POSIX
    conventions for utilities.

    """

    def add_arguments(self, actions):
        # credits go to the following:
        # https://stackoverflow.com/questions/12268602/sort-argparse-help-alphabetically
        def _parse_short_option(action):
            # This assumes all options have a short/long version,
            # will sort based on the short option ([0]).
            if action.option_strings:
                return action.option_strings[0]

        actions = sorted(actions, key=_parse_short_option)
        super(CustomHelpFormatter, self).add_arguments(actions)

    def _format_action_invocation(self, action):
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            (metavar,) = self._metavar_formatter(action, default)(1)
            return metavar

        else:
            parts = []

            # if the optional doesn't take a value, format is:
            #    -s, --long
            if action.nargs == 0:
                parts.extend(action.option_strings)

            # if the optional takes a value, formats are:
            #    -s, --long=ARG ==> if both short/long
            #    --long=ARG ==> if just long
            #    -s=ARG ==> if just short
            else:
                default = self._get_default_metavar_for_optional(action)
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    if option_string == action.option_strings[-1]:
                        parts.append(f"{option_string}={args_string}")
                    else:
                        parts.append(option_string)

            return ", ".join(parts)
