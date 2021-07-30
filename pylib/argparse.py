"""Docstring for the argparse.py module.

Contains custom functionality using the standard library argparse package.

"""
# Standard Library Imports
import argparse

# Third Party Imports

# Local Application Imports


class CustomHelpFormatter(argparse.HelpFormatter):
    """A subclassed HelpFormatter used by argparse.ArgumentParser objects.

    Changes from the original argparse.HelpFormatter include:
    -   The format of the option string(s) with there argument(s) now differ.
    -   Options are now organized in alphabetical order for their help messages
        but not in the usage string for their parser. This is more so to follow
        POSIX conventions for utilities.

    """

    def _get_first_nonprefix_char(self, action):
        """Retrieve said character from an action's option string.

        This applies to an action's first option string. Regardless
        if it is a long option or a short option.

        Parameters
        ----------
        action : argparse._ArgumentGroup
            The action with its option strings.

        Returns
        -------
        str
            The first nonprefix character found from an option string, or
            in the case the action does not contain an option string, the full
            positional argument label.

        """
        try:
            option_string = action.option_strings[0]
            prefix_char = option_string[0]  # '-h' ==> '-'
            return option_string[
                option_string.rfind(prefix_char) :  # noqa: E203,E501
            ][1]
        except IndexError:
            # Positional args do not contain option_strings, so best
            # to just sort them by their full label.
            return action.dest

    def add_arguments(self, actions):
        """Extend the parent's method in adding actions to help message.

        Actions are now sorted by their first non-prefix character.

        Parameters
        ----------
        actions : argparse._ArgumentGroup
            Contains the actions with their option_strings.

        """
        # credits go to the following:
        # https://stackoverflow.com/questions/12268602/sort-argparse-help-alphabetically

        actions = sorted(actions, key=self._get_first_nonprefix_char)
        super(CustomHelpFormatter, self).add_arguments(actions)

    def _format_action_invocation(self, action):
        """Override the parent's method in formatting option strings.

        Parameters
        ----------
        action : argparse._ArgumentGroup
            The action with its option_strings.

        Returns
        -------
        str
            The action's option strings combined together with a delimiter.

        """
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

            # if the optional takes a value, formats are (assuming '-' is a
            # prefix char):
            #    -s, --long=ARG ==> if both short/long
            #    --long=ARG ==> if just long option
            #    -s ARG ==> if just short option
            else:
                default = self._get_default_metavar_for_optional(action)
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    if option_string == action.option_strings[-1]:
                        if (
                            option_string[0] == option_string[1]
                        ):  # means at least two prefix chars
                            parts.append(f"{option_string}={args_string}")
                        else:
                            parts.append(f"{option_string} {args_string}")
                    else:
                        parts.append(option_string)
            return ", ".join(parts)


class CustomRawDescriptionHelpFormatter(CustomHelpFormatter):
    """A subclassed CustomHelpFormatter used by argparse.ArgumentParser objects.

    Changes from the original pylib.CustomHelpFormatter include:
    -   Does not reformat or line wrap help descriptions.

    """

    def _fill_text(self, text, width, indent):
        """Retain format in the text description.

        Method comes out of the argparse.RawDescriptionHelpFormatter class.

        Parameters
        ----------
        text : str
            The help description text.
        width : int, float
            The text line length.
        indent : str
            String that is prepended to the line.

        Returns
        -------
        str
            The text line with it's format retained.

        """
        return "".join(
            indent + line for line in text.splitlines(keepends=True)
        )
