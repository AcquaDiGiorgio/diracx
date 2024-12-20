from __future__ import annotations

from typing import AsyncGenerator

import pytest

from gubbins.db.sql import GubbinsJobDB


@pytest.fixture
async def gubbins_db() -> AsyncGenerator[GubbinsJobDB, None]:
    gubbins_db = GubbinsJobDB("sqlite+aiosqlite:///:memory:")
    async with gubbins_db.engine_context():
        async with gubbins_db.engine.begin() as conn:
            # set PRAGMA foreign_keys=ON if sqlite
            if gubbins_db._db_url.startswith("sqlite"):
                await conn.exec_driver_sql("PRAGMA foreign_keys=ON")
            await conn.run_sync(gubbins_db.metadata.create_all)
        yield gubbins_db


async def test_gubbins_info(gubbins_db):
    """
    This test makes sure that we can:
    * use a method from the parent db (insert)
    * use a method from a child db (insert_gubbins_info)
    * use a method modified in the child db (getJobJDL)
    """
    async with gubbins_db as gubbins_db:
        result = await gubbins_db.insert(
            "JDL",
            "owner_toto",
            "owner_group1",
            "New",
            "dfdfds",
            "lhcb",
        )

        job_id = result["JobID"]

        await gubbins_db.insert_gubbins_info(job_id, "info")

        result = await gubbins_db.getJobJDL(job_id, original=True)
        assert result == "[JDL]"

        result = await gubbins_db.getJobJDL(job_id, with_info=True)
        assert "JDL" in result
        assert result["Info"] == "info"
