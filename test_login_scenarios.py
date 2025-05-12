import pytest
import asyncio
import pytest_asyncio

from core_agent import execute


@pytest.mark.asyncio
async def test_successful_login():

    test_scenario = """
    Go to https://news.ycombinator.com/news
    click on the login button
    enter "dnivra26" for username
    enter "arvindxxxx" for password
    click on the login button
    return "Success" if you are able to see the dashboard
    """


    result = await execute(test_scenario)
    assert "Success" in result

@pytest.mark.asyncio
async def test_invaid_password():

    test_scenario = """
    Go to https://news.ycombinator.com/news
    click on the login button
    enter "dnivra26" for username
    enter "arvindnotxxxx" for password
    click on the login button
    return "Success" if you are able to see "Bad login" message
    """


    result = await execute(test_scenario)
    assert "Success" in result

@pytest.mark.asyncio
async def test_invalid_username():

    test_scenario = """
    Go to https://news.ycombinator.com/news
    click on the login button
    enter "dnivra2626arvind" for username
    enter "arvindxxxx" for password
    click on the login button
    return "Success" if you are able to see "Bad login" message
    """


    result = await execute(test_scenario)
    assert "Success" in result