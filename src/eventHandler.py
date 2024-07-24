from typing_extensions import override
from openai import AssistantEventHandler
from .openai import client

class EventHandler(AssistantEventHandler):
  @override
  def on_event(self, event):
    # Retrieve events that are denoted with 'requires_action'
    # since these will have our tool_calls
    if event.event == 'thread.run.requires_action':
      run_id = event.data.id  # Retrieve the run ID from the event data
      self.handle_requires_action(event.data, run_id)

  def handle_requires_action(self, data, run_id):
    tool_outputs = []
      
    for tool in data.required_action.submit_tool_outputs.tool_calls:
      if tool.function.name == "get_spendings":
        tool_outputs.append({"tool_call_id": tool.id, "output": '{ "data": [{ "id": 1, "name": "Lunch at midpoint", "amount": "450 TL", "date": "10-07-2024 10:34 GMT+3" }] }'})
      elif tool.function.name == "store_spending":
        tool_outputs.append({"tool_call_id": tool.id, "output": "0.06"})
      
    # Submit all tool_outputs at the same time
    self.submit_tool_outputs(tool_outputs, run_id)

  def submit_tool_outputs(self, tool_outputs, run_id):
    # Use the submit_tool_outputs_stream helper
    client.beta.threads.runs.submit_tool_outputs(
      thread_id=self.current_run.thread_id,
      run_id=self.current_run.id,
      tool_outputs=tool_outputs,
    )
