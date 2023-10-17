#!/bin/bash

case "$OSTYPE" in
    msys*)    python=python ;;
    cygwin*)  python=python ;;
    *)        python=python3 ;;
esac

PATH_TO_MANAGE_PY=$(find ../ -name "manage.py" -not -path "*/env" -not -path "*/venv");
BASE_DIR="$(dirname "${PATH_TO_MANAGE_PY}")";
cd $BASE_DIR
status=$?;
if [ $status -ne 0 ]; then
    echo "Please make sure that there is only one file manage.py";
    exit $status;
fi

echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
     usernames_list = ['vasya.pupkin', 'second-user', 'third-user-username', 'NoEmail', 'NoFirstName', 'NoLastName', 'NoPassword', 'TooLongEmail', \
     'the-username-that-is-150-characters-long-and-should-not-pass-validation-if-the-serializer-is-configured-correctly-otherwise-the-current-test-will-fail-', \
     'TooLongFirstName', 'TooLongLastName', 'InvalidU$ername', 'EmailInUse']; \
     delete_num, _ = User.objects.filter(username__in=['vasya.pupkin', 'second-user', 'third-user-username']).delete(); \
     exit(1) if not delete_num else exit(0);" | $python manage.py shell
status=$?;
if [ $status -ne 0 ]; then
    echo "Error during cleaning DB after last postman collection launch: there are no objects or general failure.";
    exit $status;
fi
echo "The DB is cleaned."
