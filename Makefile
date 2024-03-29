include base.mk

# include other generic makefiles
include python.mk

# simply expanded variables
executables := \
	${python_executables}

_check_executables := $(foreach exec,${executables},$(if $(shell command -v ${exec}),pass,$(error "No ${exec} in PATH")))

.PHONY: ${HELP}
${HELP}:
	# inspired by the makefiles of the Linux kernel and Mercurial
>	@echo 'Common make targets:'
>	@echo '  ${SETUP}        - installs the distro-independent dependencies for this'
>	@echo '                 project'

.PHONY: ${SETUP}
${SETUP}: ${PYENV_POETRY_SETUP}
