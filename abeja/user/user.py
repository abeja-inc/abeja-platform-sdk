from typing import Optional, NamedTuple, Dict, Any


__ProfileIcon = NamedTuple('ProfileIcon', [
    ('original_icon_url', Optional[str]),
    ('thumbnail_icon_url', Optional[str]),
    ('mini_icon_url', Optional[str]),
])


class ProfileIcon(__ProfileIcon):

    @classmethod
    def from_response(
            klass, response: Optional[Dict[str, Any]]) -> Optional['ProfileIcon']:
        if response is None:
            return None

        return klass(
            original_icon_url=response.get('original_icon_url'),
            thumbnail_icon_url=response.get('thumbnail_icon_url'),
            mini_icon_url=response.get('mini_icon_url'))


__User = NamedTuple('User', [
    ('id', str),
    ('display_name', str),
    ('email', str),
    ('preferred_language', str),
    ('created_at', str),
    ('updated_at', str),
    ('profile_icon', Optional[ProfileIcon]),
])


class User(__User):

    @classmethod
    def from_response(
            klass, response: Optional[Dict[str, Any]]) -> Optional['User']:
        if response is None:
            return None

        profile_icon = ProfileIcon.from_response(response.get('profile_icon'))

        return klass(
            id=response.get('id', ''),
            display_name=response.get('display_name', ''),
            email=response.get('email', ''),
            preferred_language=response.get('preferred_language', ''),
            created_at=response.get('created_at', ''),
            updated_at=response.get('updated_at', ''),
            profile_icon=profile_icon)

    @property
    def user_id(self) -> str:
        return self.id
