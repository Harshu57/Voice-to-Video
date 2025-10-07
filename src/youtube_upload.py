from __future__ import annotations

from typing import List, Optional


def upload_to_youtube(
    video_path: str,
    title: str,
    description: str,
    tags: List[str],
    privacy_status: str = "public",
) -> Optional[str]:
    """
    Placeholder for YouTube upload via YouTube Data API v3.

    Instructions:
    - Create OAuth 2.0 client credentials (Desktop) in Google Cloud Console.
    - Save JSON to a path referenced by YOUTUBE_CLIENT_SECRET_FILE.
    - Implement OAuth flow (e.g., using google-auth and google-api-python-client) and upload video.

    This placeholder returns None to signal not implemented by default.
    """
    return None
