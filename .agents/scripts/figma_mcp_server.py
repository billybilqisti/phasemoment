#!/usr/bin/env python3
"""
Figma Model Context Protocol (MCP) Server
Zero-dependency, standalone stdio server for Figma API.
"""

import sys
import os
import json
import re
import urllib.request
import urllib.parse
import urllib.error

FIGMA_API_BASE = "https://api.figma.com/v1"
TOKEN = os.environ.get("FIGMA_ACCESS_TOKEN") or os.environ.get("FIGMA_API_KEY") or "figd_WoiBSrfV4ybXMfYJq-J2ggTTHG2KkGOE7VeBbENG"

def log(msg):
    sys.stderr.write(f"[Figma MCP] {msg}\n")
    sys.stderr.flush()

def extract_file_key(key_or_url: str) -> str:
    if not key_or_url:
        return ""
    # Check if URL
    match = re.search(r"figma\.com/(?:file|design)/([a-zA-Z0-9]+)", key_or_url)
    if match:
        return match.group(1)
    # Check if direct key
    return key_or_url.strip().split("?")[0].split("/")[0]

def extract_node_id(node_id_or_url: str) -> str:
    if not node_id_or_url:
        return ""
    if "node-id=" in node_id_or_url:
        match = re.search(r"node-id=([^&]+)", node_id_or_url)
        if match:
            val = urllib.parse.unquote(match.group(1))
            return val.replace("-", ":")
    return node_id_or_url.strip().replace("-", ":")

def figma_request(endpoint: str, method: str = "GET", data: dict = None, query: dict = None) -> dict:
    url = f"{FIGMA_API_BASE}/{endpoint.lstrip('/')}"
    if query:
        clean_query = {k: v for k, v in query.items() if v is not None}
        if clean_query:
            url += ("?" if "?" not in url else "&") + urllib.parse.urlencode(clean_query)
    
    headers = {
        "X-Figma-Token": TOKEN,
        "User-Agent": "Antigravity-Figma-MCP/1.0"
    }
    
    req_body = None
    if data is not None:
        headers["Content-Type"] = "application/json"
        req_body = json.dumps(data).encode("utf-8")
        
    req = urllib.request.Request(url, data=req_body, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            content = resp.read().decode("utf-8")
            return json.loads(content)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(error_body)
            err_msg = parsed.get("err") or parsed.get("message") or error_body
        except Exception:
            err_msg = error_body
        raise RuntimeError(f"Figma API HTTP {e.code}: {err_msg}")
    except Exception as e:
        raise RuntimeError(f"Figma API Request Failed: {str(e)}")

# Define Tools
TOOLS = [
    {
        "name": "figma_get_me",
        "description": "Get current authenticated Figma user information to verify credentials and connection.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "figma_get_file",
        "description": "Fetch the document JSON for a Figma file. You can pass a file key or full Figma file/design URL.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_key": {
                    "type": "string",
                    "description": "Figma file key or full URL (e.g., https://www.figma.com/design/KEY/...)"
                },
                "depth": {
                    "type": "integer",
                    "description": "Traverse depth of the component tree (optional)"
                },
                "ids": {
                    "type": "string",
                    "description": "Comma-separated list of node IDs to filter by (optional)"
                }
            },
            "required": ["file_key"]
        }
    },
    {
        "name": "figma_get_file_nodes",
        "description": "Fetch specific nodes (frames, components) by ID from a Figma file. Faster and more focused than downloading the whole file.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_key": {
                    "type": "string",
                    "description": "Figma file key or full URL"
                },
                "ids": {
                    "type": "string",
                    "description": "Comma-separated node IDs (e.g. '0:1' or '123-456' or URL with node-id)"
                },
                "depth": {
                    "type": "integer",
                    "description": "Traverse depth of the node tree (optional)"
                }
            },
            "required": ["file_key", "ids"]
        }
    },
    {
        "name": "figma_get_image",
        "description": "Render frames, components, or layers as images (PNG, SVG, JPG, PDF) and get their download URLs.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_key": {
                    "type": "string",
                    "description": "Figma file key or full URL"
                },
                "ids": {
                    "type": "string",
                    "description": "Comma-separated node IDs to render as images"
                },
                "scale": {
                    "type": "number",
                    "description": "Image scaling factor between 0.01 and 4 (default: 2)"
                },
                "format": {
                    "type": "string",
                    "enum": ["png", "jpg", "svg", "pdf"],
                    "description": "Image export format (default: png)"
                }
            },
            "required": ["file_key", "ids"]
        }
    },
    {
        "name": "figma_get_image_fills",
        "description": "Get download URLs for images that are used as fills in a Figma file.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_key": {
                    "type": "string",
                    "description": "Figma file key or full URL"
                }
            },
            "required": ["file_key"]
        }
    },
    {
        "name": "figma_get_comments",
        "description": "Get comments on a Figma file.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_key": {
                    "type": "string",
                    "description": "Figma file key or full URL"
                }
            },
            "required": ["file_key"]
        }
    },
    {
        "name": "figma_post_comment",
        "description": "Post a new comment to a Figma file or reply to a thread.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_key": {
                    "type": "string",
                    "description": "Figma file key or full URL"
                },
                "message": {
                    "type": "string",
                    "description": "Comment text"
                },
                "comment_id": {
                    "type": "string",
                    "description": "Optional parent comment ID if replying to a thread"
                }
            },
            "required": ["file_key", "message"]
        }
    },
    {
        "name": "figma_get_team_projects",
        "description": "List all projects in a Figma team.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "team_id": {
                    "type": "string",
                    "description": "Figma Team ID"
                }
            },
            "required": ["team_id"]
        }
    },
    {
        "name": "figma_get_project_files",
        "description": "List all files in a specific Figma project.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "string",
                    "description": "Figma Project ID"
                }
            },
            "required": ["project_id"]
        }
    }
]

def handle_tool_call(name: str, args: dict) -> dict:
    if name == "figma_get_me":
        return figma_request("me")
        
    elif name == "figma_get_file":
        file_key = extract_file_key(args.get("file_key", ""))
        if not file_key:
            raise ValueError("Invalid file_key or Figma URL provided.")
        query = {}
        if "depth" in args:
            query["depth"] = args["depth"]
        if "ids" in args and args["ids"]:
            query["ids"] = ",".join(extract_node_id(i) for i in args["ids"].split(","))
        return figma_request(f"files/{file_key}", query=query)
        
    elif name == "figma_get_file_nodes":
        file_key = extract_file_key(args.get("file_key", ""))
        ids_raw = args.get("ids", "")
        if not ids_raw and "node-id=" in args.get("file_key", ""):
            ids_raw = extract_node_id(args.get("file_key", ""))
        clean_ids = ",".join(extract_node_id(i) for i in ids_raw.split(","))
        query = {"ids": clean_ids}
        if "depth" in args:
            query["depth"] = args["depth"]
        return figma_request(f"files/{file_key}/nodes", query=query)
        
    elif name == "figma_get_image":
        file_key = extract_file_key(args.get("file_key", ""))
        ids_raw = args.get("ids", "")
        clean_ids = ",".join(extract_node_id(i) for i in ids_raw.split(","))
        query = {
            "ids": clean_ids,
            "scale": args.get("scale", 2),
            "format": args.get("format", "png")
        }
        return figma_request(f"images/{file_key}", query=query)
        
    elif name == "figma_get_image_fills":
        file_key = extract_file_key(args.get("file_key", ""))
        return figma_request(f"files/{file_key}/images")
        
    elif name == "figma_get_comments":
        file_key = extract_file_key(args.get("file_key", ""))
        return figma_request(f"files/{file_key}/comments")
        
    elif name == "figma_post_comment":
        file_key = extract_file_key(args.get("file_key", ""))
        payload = {"message": args.get("message", "")}
        if "comment_id" in args:
            payload["comment_id"] = args["comment_id"]
        return figma_request(f"files/{file_key}/comments", method="POST", data=payload)
        
    elif name == "figma_get_team_projects":
        team_id = args.get("team_id", "").strip()
        return figma_request(f"teams/{team_id}/projects")
        
    elif name == "figma_get_project_files":
        project_id = args.get("project_id", "").strip()
        return figma_request(f"projects/{project_id}/files")
        
    else:
        raise ValueError(f"Unknown tool: {name}")

def send_response(resp: dict):
    line = json.dumps(resp, ensure_ascii=False)
    sys.stdout.write(line + "\n")
    sys.stdout.flush()

def main():
    log("Starting Figma MCP Server (stdio transport)...")
    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception as e:
            log(f"Failed to parse JSON: {e}")
            continue
            
        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        # Handle notifications (no id)
        if req_id is None:
            if method == "notifications/initialized":
                log("Client initialized connection.")
            continue
            
        if method == "initialize":
            send_response({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "figma-mcp",
                        "version": "1.0.0"
                    }
                }
            })
        elif method == "ping":
            send_response({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {}
            })
        elif method == "tools/list":
            send_response({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": TOOLS
                }
            })
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            try:
                data = handle_tool_call(tool_name, tool_args)
                text_content = json.dumps(data, indent=2, ensure_ascii=False)
                send_response({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": text_content
                            }
                        ],
                        "isError": False
                    }
                })
            except Exception as e:
                log(f"Error calling {tool_name}: {e}")
                send_response({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Error: {str(e)}"
                            }
                        ],
                        "isError": True
                    }
                })
        else:
            send_response({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            })

if __name__ == "__main__":
    main()
