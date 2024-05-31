## Adding a New Local Tool for Composio

This document guides you through creating a new local tool for Composi.io.

**Structure:**

Your local tool and its actions should be organized as follows:

```
local_tools/
├── <tool_name>/
│   ├── tool.py
│   ├── __init__.py
│   └── actions/
│       ├── <action_name>.py
│       └── __init__.py
```

**Files and their Contents:**

1. **`composio/local_tools/<tool_name>/tool.py`:** Defines the tool class.

   ```python
   from composio.core.local import Tool, Action
   from .actions.<action_name> import <ActionName>  # Import your action class

   class <ToolName>(Tool):
       """
       Description of your tool.
       """

       def actions(self) -> list[Action]:
           return [<ActionName>]

       def triggers(self) -> list:
           return []  # If applicable, define triggers here
   ```

2. **`composio/local_tools/<tool_name>/__init__.py`:** Exports the tool class.

   ```python
   from .tool import <ToolName>
   ```

3. **`composio/local_tools/<tool_name>/actions/<action_name>.py`:** Defines an action for your tool.

   ```python
   from pydantic import BaseModel, Field
   from composio.core.local import Action

   class <RequestSchema>(BaseModel):
       # Define input schema for your action
       # Example:
       # text: str = Field(..., description="Input text for the action")

   class <ResponseSchema>(BaseModel):
       # Define output schema for your action
       # Example:
       # result: str = Field(..., description="Result of the action")

   class <ActionName>(Action):
       """
       Description of your action.
       """

       _display_name = "Friendly name of your action"
       _request_schema = <RequestSchema>
       _response_schema = <ResponseSchema>
       _tags = ["tag1", "tag2"]  # Optional tags to categorize your action
       _tool_name = "<tool_name>"  # Tool name, same as directory name

       def execute(
           self, request_data: <RequestSchema>, authorisation_data: dict = {}
       ) -> dict:
           # Implement logic to process input and return output
           # Example:
           # response_data = {"result": "Processed text: " + request_data.text}
           return {"execution_details": {"executed": True}, "response_data": response_data}
   ```

4. **`composio/local_tools/<tool_name>/actions/__init__.py`:** Exports the action class.

   ```python
   from .<action_name> import <ActionName>
   ```

5. Register your tool inside `composio/client/local_handler.py` file.

```diff
diff --git a/composio/client/local_handler.py b/composio/client/local_handler.py
index 9a36573..94dfd1b 100644
--- a/composio/client/local_handler.py
+++ b/composio/client/local_handler.py
@@ -16,7 +16,7 @@ from composio.local_tools.ragtool import RagTool
 from composio.local_tools import Mathematical
 from composio.local_tools.webtool import WebTool
 from composio.local_tools.greptile.tool import Greptile
-
+from composio.tools.local_tools.<tool_name> import <ToolName>
 
 class LocalToolHandler:
     def __init__(self):
@@ -46,6 +46,7 @@ class LocalToolHandler:
             RagTool(),
             WebTool(),
             Greptile(),
+            <ToolName>(),
         ]
```

**Example:**

**`composio/local_tools/sentiment/tool.py`**

```python
from composio.core.local import Tool, Action
from .actions.sentiment_analysis import SentimentAnalysis

class SentimentAnalyzer(Tool):
    """
    Analyzes the sentiment of text.
    """

    def actions(self) -> list[Action]:
        return [SentimentAnalysis]

    def triggers(self) -> list:
        return []
```

**`composio/local_tools/sentiment/actions/sentiment_analysis.py`**

```python
from pydantic import BaseModel, Field
from composio.core.local import Action

class SentimentRequest(BaseModel):
    text: str = Field(..., description="Text to analyze sentiment")

class SentimentResponse(BaseModel):
    sentiment: str = Field(..., description="Sentiment (e.g., positive, negative, neutral)")

class SentimentAnalysis(Action):
    """
    Analyzes the sentiment of text.
    """

    _display_name = "Analyze Sentiment"
    _request_schema = SentimentRequest
    _response_schema = SentimentResponse
    _tags = ["sentiment", "analysis"]
    _tool_name = "sentiment"

    def execute(
        self, request_data: SentimentRequest, authorisation_data: dict = {}
    ) -> dict:
        # Implement sentiment analysis logic here
        response_data = {"sentiment": "positive"}  # Placeholder
        return {"execution_details": {"executed": True}, "response_data": response_data}
```

**Integration:**

* Make sure you register your new tool inside `composio/client/local_handler.py` file.
* You can now access your new tool through Composio SdK and use it to power you Agents.

**Key Points:**

* Replace placeholders `<tool_name>`, `<action_name>`, `<ToolName>`, `<ActionName>`, `<RequestSchema>`, `<ResponseSchema>` with your own names and logic.
* Use the Composi.io documentation for further details on defining tools and actions: [https://docs.composio.dev/](https://docs.composio.dev/)
* Install any required dependencies for your tools and actions.

By following these steps, you can easily create custom local tools that enhance your LLM applications within Composi.io. 