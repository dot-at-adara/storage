import pytest

FIRST_ATTEMPT = True


@pytest.fixture()
def reset_attempts():
    global FIRST_ATTEMPT
    FIRST_ATTEMPT = True


def always_fail():
    assert False


def fail_once():
    global FIRST_ATTEMPT
    print(FIRST_ATTEMPT)
    if FIRST_ATTEMPT:
        FIRST_ATTEMPT = False
        assert False
    else:
        FIRST_ATTEMPT = True
        return True


def test_fails_on_first_atttempt(reset_attempts):
    from framework.storage.utilities import manage_retries
    from functools import partial
    partial_function = partial(fail_once)
    with pytest.raises(AssertionError):
        manage_retries(partial_function=partial_function, handled_exceptions=(AssertionError,),
                       propagate_exceptions=True, retries=1, backoff=False)


def test_retry_automatically(reset_attempts, caplog):
    from framework.storage.utilities import manage_retries
    from functools import partial
    partial_function = partial(fail_once)
    results = manage_retries(partial_function=partial_function, handled_exceptions=(AssertionError,),
                             propagate_exceptions=True, retries=3, backoff=False)
    assert results


def test_raise_errors_with_propagation(reset_attempts):
    from framework.storage.utilities import manage_retries
    from functools import partial
    partial_function = partial(always_fail)
    with pytest.raises(AssertionError):
        manage_retries(partial_function=partial_function, handled_exceptions=(AssertionError,),
                       propagate_exceptions=True, retries=3, backoff=False)


def test_no_errors_without_propagation(reset_attempts):
    from datetime import datetime
    from framework.storage.utilities import manage_retries
    from functools import partial
    partial_function = partial(always_fail)
    start = int(datetime.utcnow().timestamp())
    results = manage_retries(partial_function=partial_function, handled_exceptions=(AssertionError,),
                             propagate_exceptions=False, retries=3, backoff=False)
    end = int(datetime.utcnow().timestamp())
    assert results is None
    assert (end - start) < 1


def test_backoff(reset_attempts):
    from datetime import datetime
    from framework.storage.utilities import manage_retries
    from functools import partial
    start = int(datetime.utcnow().timestamp())
    partial_function = partial(always_fail)
    manage_retries(partial_function=partial_function, handled_exceptions=(AssertionError,), propagate_exceptions=False,
                   retries=3, backoff=True)
    end = int(datetime.utcnow().timestamp())
    assert (end - start) >= 7
