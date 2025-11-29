# Import ObjectId type used for MongoDB document IDs
from bson import ObjectId

# Import the async MongoDB collection class from Motor
from motor.motor_asyncio import AsyncIOMotorCollection

# Import ReturnDocument to control what find_one_and_update returns
from pymongo import ReturnDocument

# Import BaseModel from Pydantic for data validation and serialization
from pydantic import BaseModel

# Import uuid4 to generate unique IDs for list items
from uuid import uuid4


# Pydantic model representing a lightweight summary of a ToDo list
class ListSummary(BaseModel):
    id: str  # List ID
    name: str  # List name
    item_count: int  # Number of items in the list

    @staticmethod
    def from_doc(doc) -> "ListSummary":
        # Convert MongoDB document into ListSummary model
        return ListSummary(
            id=str(doc["_id"]),  # Convert ObjectId to string
            name=doc["name"],  # Extract name
            item_count=doc["item_count"],  # Extract computed item count
        )


# Pydantic model for a single item in a to-do list
class ToDoListItem(BaseModel):
    id: str  # Unique item ID
    label: str  # Item text
    checked: bool  # Boolean status of item

    @staticmethod
    def from_doc(item) -> "ToDoListItem":
        # Convert item document into ToDoListItem model
        return ToDoListItem(
            id=item["id"],
            label=item["label"],
            checked=item["checked"],
        )


# Pydantic model for the entire to-do list including items
class ToDoList(BaseModel):
    id: str  # List ID
    name: str  # List name
    items: list[ToDoListItem]  # All items inside the list

    @staticmethod
    def from_doc(doc) -> "ToDoList":
        # Convert MongoDB document into ToDoList model
        return ToDoList(
            id=str(doc["_id"]),  # Convert ObjectId to string
            name=doc["name"],  # Extract name
            items=[ToDoListItem.from_doc(item) for item in doc["items"]],  # Map items
        )


# Data Access Layer (DAL) for interacting with MongoDB
class ToDoDAL:
    def __init__(self, todo_collection: AsyncIOMotorCollection):
        # Store the MongoDB collection
        self._todo_collection = todo_collection

    async def list_todo_lists(self, session=None):
        # Iterate all lists and return summary information
        async for doc in self._todo_collection.find(
            {},  # No filter → return all documents
            projection={
                "name": 1,  # Include name
                "item_count": {"$size": "$items"},  # Compute number of items
            },
            sort={"name": 1},  # Sort alphabetically by name
            session=session,
        ):
            yield ListSummary.from_doc(doc)  # Yield one summary at a time

    async def create_todo_list(self, name: str, session=None) -> str:
        # Insert a new todo list with empty items array
        response = await self._todo_collection.insert_one(
            {"name": name, "items": []},
            session=session,
        )
        return str(response.inserted_id)  # Return ID as string

    async def get_todo_list(self, id: str | ObjectId, session=None) -> ToDoList:
        # Find a single list by ID
        doc = await self._todo_collection.find_one(
            {"_id": ObjectId(id)},
            session=session,
        )
        return ToDoList.from_doc(doc)  # Convert and return model

    async def delete_todo_list(self, id: str | ObjectId, session=None) -> bool:
        # Delete a list by ID
        response = await self._todo_collection.delete_one(
            {"_id": ObjectId(id)},
            session=session,
        )
        return response.deleted_count == 1  # Return success status

    async def create_item(
        self,
        id: str | ObjectId,
        label: str,
        session=None,
    ) -> ToDoList | None:
        # Add a new item to the list
        result = await self._todo_collection.find_one_and_update(
            {"_id": ObjectId(id)},  # Target list
            {
                "$push": {  # Push new item into the items array
                    "items": {
                        "id": uuid4().hex,  # Generate unique item ID
                        "label": label,  # Item name
                        "checked": False,  # Initial state
                    }
                }
            },
            session=session,
            return_document=ReturnDocument.AFTER,  # Return updated list
        )
        if result:
            return ToDoList.from_doc(result)  # Convert and return updated list

    async def set_checked_state(
        self,
        doc_id: str | ObjectId,
        item_id: str,
        checked_state: bool,
        session=None,
    ) -> ToDoList | None:
        # Update the "checked" field of one item
        result = await self._todo_collection.find_one_and_update(
            {"_id": ObjectId(doc_id), "items.id": item_id},  # Match list + item
            {
                "$set": {"items.$.checked": checked_state}
            },  # Update item using positional operator
            session=session,
            return_document=ReturnDocument.AFTER,
        )
        if result:
            return ToDoList.from_doc(result)

    async def delete_item(
        self,
        doc_id: str | ObjectId,
        item_id: str,
        session=None,
    ) -> ToDoList | None:
        # Remove an item from the list
        result = await self._todo_collection.find_one_and_update(
            {"_id": ObjectId(doc_id)},  # Match list
            {"$pull": {"items": {"id": item_id}}},  # Remove matching item
            session=session,
            return_document=ReturnDocument.AFTER,
        )
        if result:
            return ToDoList.from_doc(result)
