from pydantic import BaseModel,Field

class Profile(BaseModel):
    name: str
class Contact(BaseModel):
    profile: Profile
    wa_id: str
class Text(BaseModel):
    body: str
class Message(BaseModel):
    from_: str = Field(alias="from")
    id: str
    timestamp: str
    text: Text | None = None
    type: str
class Metadata(BaseModel):
    display_phone_number: str
    phone_number_id: str
class Value(BaseModel):
    messaging_product: str
    metadata: Metadata
    contacts: list[Contact] | None = None
    messages: list[Message] | None = None
class Change(BaseModel):
    field: str
    value: Value
class Entry(BaseModel):
    id: str
    changes: list[Change]
class WebhookPayload(BaseModel):
    entry: list[Entry]
    object: str