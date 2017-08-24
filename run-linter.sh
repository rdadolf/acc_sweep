#!/bin/bash
LINT_FLAGS=-rn
die() { echo "ERROR: $@"; exit 1; }
pylint $LINT_FLAGS acc_sweep || die 'Linter check failed for library'
