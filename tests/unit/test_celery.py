# tests.py
from unittest.mock import patch   # from magic import whoa
from .tasks import task
@pytest.mark.usefixtures('celery_session_app')
@pytest.mark.usefixtures('celery_session_worker')
class MyTest():
    @patch('tasks.some_function')  # See this?
    def test(self, function_mock):  # And that second argument.
        task_handle = task.delay()
        task_handle.get()  # Wait for the task to finish.
        function_mock.assert_called()  # Check that the function was actually called.