import os
import requests
from typing import Dict, Union

from factionpy.logger import log, error_out
from factionpy.config import FILES_ENDPOINT


def upload_file(upload_type: str, file_path: str, api_key: str, description: str = None, agent_id: str = None,
                source_file_path: str = None, metadata: str = None) -> Dict[str, Union[str, bool]]:
    """
    Uploads a file to Faction.
    :param upload_type: what type of file is being uploaded (payload, agent_upload, user_upload, etc)
    :param file_path: path to the file being uploaded
    :param api_key: faction api key
    :param description: description of the file
    :param agent_id: ID of the agent uploading the file (if agent_upload)
    :param source_file_path: Path where the file was found (if agent_upload)
    :param metadata: JSON string of metadata to be associated with the upload
    :return: {"success": bool, "message": str}
    """
    if os.path.exists(file_path):
        log(f"Got upload request for {file_path}", "debug")
        try:
            file = {'file': open(file_path, 'rb')}
            headers = {
                        "Content-type": "application/json",
                        "Authorization": f"Bearer {api_key}"
                    }
            file_info = {
                'upload_type': upload_type,
                'description': description,
                'agent_id': agent_id,
                'source_file_path': source_file_path,
                'metadata': metadata
            }
            log(f"Sending the following to {FILES_ENDPOINT}: {file_info}", "debug")
            resp = requests.post(FILES_ENDPOINT, headers=headers, files=file, data=file_info)
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
