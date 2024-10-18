import asyncio
import json
import os
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import typer

from diracx.client.aio import DiracClient
from diracx.client.models import DeviceFlowErrorResponse
from diracx.core.extensions import select_from_extension
from diracx.core.preferences import get_diracx_preferences
from diracx.core.utils import write_credentials

from .utils import AsyncTyper

app = AsyncTyper()


async def installation_metadata():
    async with DiracClient() as api:
        return await api.well_known.installation_metadata()


def vo_callback(vo: str | None) -> str:
    metadata = asyncio.run(installation_metadata())
    vos = list(metadata.virtual_organizations)
    if not vo:
        raise typer.BadParameter(
            f"VO must be specified, available options are: {' '.join(vos)}"
        )
    if vo not in vos:
        raise typer.BadParameter(
            f"Unknown VO {vo}, available options are: {' '.join(vos)}"
        )
    return vo


@app.async_command()
async def login(
    vo: Annotated[Optional[str], typer.Argument(callback=vo_callback)] = None,
    group: Optional[str] = None,
    property: Optional[list[str]] = typer.Option(
        None, help="Override the default(s) with one or more properties"
    ),
):
    scopes = [f"vo:{vo}"]
    if group:
        scopes.append(f"group:{group}")
    if property:
        scopes += [f"property:{p}" for p in property]

    print(f"Logging in with scopes: {scopes}")
    async with DiracClient() as api:
        data = await api.auth.initiate_device_flow(
            client_id=api.client_id,
            scope=" ".join(scopes),
        )
        print("Now go to:", data.verification_uri_complete)
        expires = datetime.now(tz=timezone.utc) + timedelta(
            seconds=data.expires_in - 30
        )
        while expires > datetime.now(tz=timezone.utc):
            print(".", end="", flush=True)
            response = await api.auth.token(device_code=data.device_code, client_id=api.client_id)  # type: ignore
            if isinstance(response, DeviceFlowErrorResponse):
                if response.error == "authorization_pending":
                    # TODO: Setting more than 5 seconds results in an error
                    # Related to keep-alive disconnects from uvicon (--timeout-keep-alive)
                    await asyncio.sleep(2)
                    continue
                raise RuntimeError(f"Device flow failed with {response}")
            break
        else:
            raise RuntimeError("Device authorization flow expired")

        # Save credentials
        write_credentials(response)
        credentials_path = get_diracx_preferences().credentials_path
        print(f"Saved credentials to {credentials_path}")
    print("\nLogin successful!")


@app.async_command()
async def whoami():
    async with DiracClient() as api:
        user_info = await api.auth.userinfo()
        # TODO: Add a RICH output format
        print(json.dumps(user_info.as_dict(), indent=2))


@app.async_command()
async def logout():
    async with DiracClient() as api:
        credentials_path = get_diracx_preferences().credentials_path
        if credentials_path.exists():
            credentials = json.loads(credentials_path.read_text())

            # Revoke refresh token
            try:
                await api.auth.revoke_refresh_token(credentials["refresh_token"])
            except Exception as e:
                print(f"Error revoking the refresh token {e!r}")
                pass

            # Remove credentials
            credentials_path.unlink(missing_ok=True)
            print(f"Removed credentials from {credentials_path}")
    print("\nLogout successful!")


@app.callback()
def callback(output_format: Optional[str] = None):
    if output_format is not None:
        os.environ["DIRACX_OUTPUT_FORMAT"] = output_format


# Load all the sub commands

cli_names = set(
    [entry_point.name for entry_point in select_from_extension(group="diracx.cli")]
)
for cli_name in cli_names:
    entry_point = select_from_extension(group="diracx.cli", name=cli_name)[0]
    app.add_typer(entry_point.load(), name=entry_point.name)


cli_hidden_names = set(
    [
        entry_point.name
        for entry_point in select_from_extension(group="diracx.cli.hidden")
    ]
)
for cli_name in cli_hidden_names:
    entry_point = select_from_extension(group="diracx.cli.hidden", name=cli_name)[0]
    app.add_typer(entry_point.load(), name=entry_point.name, hidden=True)


if __name__ == "__main__":
    app()
