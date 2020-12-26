import os
from datetime import datetime
from pathlib import Path
from uuid import UUID

import httpx
from typing import Dict, Union, Optional

from pydantic import BaseModel

from factionpy.logger import log, error_out
from factionpy.config import FILES_ENDPOINT, VERIFY_SSL

http = httpx.AsyncClient(verify=VERIFY_SSL)


class FileProperties(BaseModel):
    id: Optional[UUID]
    description: Optional[str]
    type: str
    agent_id: Optional[UUID]
    user_id: Optional[UUID]
    file_path: Optional[str]
    source_file_path: Optional[str]
    created: Optional[datetime]
    last_downloaded: Optional[datetime]
    hash: Optional[str]
    enabled: bool
    url: Optional[str]
    metadata: Optional[str]


async def upload_file(api_key: str, file_path: Path, file_properties: FileProperties) -> Dict[str, Union[str, bool]]:
    """
    Uploads a file to Faction.
    :param file_path:
    :param api_key:
    :param file_properties:
    :return: {"success": bool, "message": str}
    """
    if os.path.exists(file_path):
        log(f"Got upload request for {file_path}", "debug")
        try:
            file = {'file': open(file_path, 'rb')}
            headers = {
                        "Authorization": f"Bearer {api_key}"
                    }
            file_info = {
                'type': file_properties.type,
                'description': file_properties.description,
                'agent_id': file_properties.agent_id,
                'source_file_path': file_properties.source_file_path,
                'metadata': file_properties.metadata
            }
            log(f"Sending the following to {FILES_ENDPOINT}: {file_info}", "debug")
            resp = await http.post(FILES_ENDPOINT, headers=headers, files=file, data=file_info)
        except Exception as e:
            return error_out(f"Error uploading file {file_path}. Error: {e}")

        if resp.status_code == 200:
            log(f"Successfully uploaded file {file_path}", "info")
            return {
                'success': True,
                'message': f"File {file_path} uploaded successfully"
            }
        else:
            return error_out(f"File {file_path} could not be uploaded. Response from server: {resp.content}")
