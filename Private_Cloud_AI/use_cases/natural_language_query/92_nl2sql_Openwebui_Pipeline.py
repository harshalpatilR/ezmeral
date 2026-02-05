### Openwebui - disable any caching of models and enable pipeline under models tab also
"""
title: NL2SQL Database Pipeline
author: YourName
version: 1.0.3
description: All queries routed to Langflow NL2SQL pipeline - Non-async version
"""

import requests
import json
import urllib3
from typing import List, Union, Generator, Iterator
from pydantic import BaseModel

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Pipeline:
    class Valves(BaseModel):
        """Pipeline configuration"""
        LANGFLOW_URL: str = "https://langflow.app.pcai.sgctc.net/api/v1/run/f97143ca-830e-49b8-9be3-0ca707703050?stream=false"
        QUERY_TIMEOUT: int = 60
        DEBUG_MODE: bool = False
        SHOW_SQL: bool = False

    def __init__(self):
        self.name = "Natural Language Query"
        self.valves = self.Valves()

    async def on_startup(self):
        """Called when the pipeline starts"""
        print(f"NL2SQL Pipeline starting up...")
        print(f"Langflow URL: {self.valves.LANGFLOW_URL}")

    async def on_shutdown(self):
        """Called when the pipeline shuts down"""
        print("NL2SQL Pipeline shutting down...")

    def query_langflow(self, question: str) -> str:
        """Query Langflow API"""
        
        payload = {
            "input_value": question.strip(),
            "tweaks": {}
        }
        
        headers = {"Content-Type": "application/json"}
        
        try:
            if self.valves.DEBUG_MODE:
                print(f"🔄 Sending to Langflow: {question[:50]}...")
                
            response = requests.post(
                self.valves.LANGFLOW_URL,
                json=payload,
                headers=headers,
                timeout=self.valves.QUERY_TIMEOUT,
                verify=False
            )
            
            if self.valves.DEBUG_MODE:
                print(f"📊 Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                if self.valves.DEBUG_MODE:
                    print(f"✅ Got response from Langflow")
                
                # Extract the response
                try:
                    
                    if(self.valves.SHOW_SQL):
                        answer = "SQL: /n"+ result["outputs"][0]["outputs"][1]["results"]["message"]["text"] + "/n Result: /n" + result["outputs"][0]["outputs"][0]["results"]["message"]["text"]
                    else:
                        answer = result["outputs"][0]["outputs"][0]["results"]["message"]["text"]

                    if self.valves.DEBUG_MODE:
                        print(f"📝 Extracted answer: {answer[:100]}...")
                    return answer

                except (KeyError, IndexError, TypeError) as e:
                    if self.valves.DEBUG_MODE:
                        print(f"❌ Parse error: {e}")
                    return "Sorry, I couldn't process that query. Please try again."
            else:
                error_msg = f"❌ Query failed with status {response.status_code}"
                print(error_msg)
                return error_msg
                        
        except requests.exceptions.Timeout:
            error_msg = f"⏱️ Query timed out after {self.valves.QUERY_TIMEOUT} seconds"
            print(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            print(error_msg)
            return error_msg

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        """Main pipeline processing function - NOT ASYNC"""
        
        if self.valves.DEBUG_MODE:
            print(f"🚀 Pipeline received: '{user_message}'")
        
        try:
            result = self.query_langflow(user_message)
            
            if self.valves.DEBUG_MODE:
                print(f"📤 Returning result: {result[:100]}...")
                
            return result
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            print(f"❌ Pipeline error: {error_msg}")
            return error_msg

    def pipe_stream(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        """Streaming version - NOT ASYNC"""
        
        if self.valves.DEBUG_MODE:
            print(f"🌊 Streaming pipeline received: '{user_message}'")
        
        try:
            result = self.query_langflow(user_message)
            
            if self.valves.DEBUG_MODE:
                print(f"🌊 Streaming result: {result[:100]}...")
            
            # Return as generator for streaming
            yield result
                
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            print(f"❌ Streaming pipeline error: {error_msg}")
            yield error_msg
