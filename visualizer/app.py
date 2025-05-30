import os
import sys
from pathlib import Path

# Add the project root to Python path for Vercel
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Also add the visualizer directory for module imports
visualizer_dir = project_root / "visualizer"
sys.path.insert(0, str(visualizer_dir))

from flask import Flask, render_template, jsonify, request
import json
import glob
import logging
import time
import re
from collections import defaultdict

try:
    # Try relative import first
    from . import node_details_helper
    from . import config
except ImportError:
    # Fallback for Vercel serverless environment
    import sys
    from pathlib import Path
    visualizer_dir = Path(__file__).parent
    sys.path.insert(0, str(visualizer_dir))
    import node_details_helper
    import config

class AIAlignmentVisualizer:
    def __init__(self):
        # For Vercel deployment, static files are served from visualizer/static
        static_folder = os.path.join(os.path.dirname(__file__), 'static')
        template_folder = os.path.join(os.path.dirname(__file__), 'templates')
        
        self.app = Flask(__name__, 
                        static_url_path='/static', 
                        static_folder=static_folder,
                        template_folder=template_folder)
        
        # Simple rate limiting storage (in-memory for Vercel serverless)
        self.request_counts = defaultdict(list)
        self.rate_limit_window = config.RATE_LIMIT_WINDOW
        self.rate_limit_max_requests = config.RATE_LIMIT_MAX_REQUESTS
        
        self.setup_logging()
        self.setup_paths()
        self.setup_routes()
        
    def setup_logging(self):
        # Production logging - only errors and warnings
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s'
        ))
        # Only log warnings and errors in production
        handler.setLevel(logging.WARNING)
        self.app.logger.addHandler(handler)
        self.app.logger.setLevel(logging.WARNING)
        self.app.logger.warning('AI Alignment Visualization startup')
        
    def setup_paths(self):
        self.APP_DIR = os.path.abspath(os.path.dirname(__file__))
        self.PARENT_DIR = os.path.abspath(os.path.join(self.APP_DIR, ".."))
        self.COMPONENTS_DIR = os.path.normpath(os.path.join(self.PARENT_DIR, "components"))
        self.SUBCOMPONENTS_DIR = os.path.normpath(os.path.join(self.PARENT_DIR, "subcomponents"))
        self.ROOT_JSON_FILE = os.path.normpath(os.path.join(self.PARENT_DIR, "ai-alignment.json"))
        
    def check_rate_limit(self):
        """Simple rate limiting check"""
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        if not client_ip:
            return True  # Allow if we can't determine IP
            
        current_time = time.time()
        
        # Clean old requests outside the window
        self.request_counts[client_ip] = [
            req_time for req_time in self.request_counts[client_ip]
            if current_time - req_time < self.rate_limit_window
        ]
        
        # Check if under limit
        if len(self.request_counts[client_ip]) >= self.rate_limit_max_requests:
            return False
            
        # Add current request
        self.request_counts[client_ip].append(current_time)
        return True

    def setup_routes(self):
        self.app.route('/')(self.index)
        self.app.route('/api/graph', methods=['GET'])(self.graph)
        self.app.route('/api/hierarchy-path/<node_id>')(self.hierarchy_path)
        self.app.route('/api/health')(self.health_check)
        self.app.route('/api/root')(self.root_details)
        self.app.route('/api/details/<node_id>')(self.node_details)
        self.app.route('/api/audio-config')(self.audio_config)
        
    def run(self, host='0.0.0.0', port=3000, debug=False):
        self.app.run(host=host, port=port, debug=debug)
        
    def index(self):
        return render_template('index.html')
        
    def graph(self):
        """Return the graph data for visualization."""
        # Check rate limit for API endpoints
        if not self.check_rate_limit():
            return jsonify({"error": "Rate limit exceeded"}), 429
            
        try:
            graph_data = self.build_graph_data()
            return jsonify(graph_data)
        except Exception as e:
            self.app.logger.error(f"Error building graph data")
            return jsonify({
                "error": "Unable to load graph data"
            }), 500
            
    def node_details(self, node_id):
        # Check rate limit for API endpoints
        if not self.check_rate_limit():
            return jsonify({"error": "Rate limit exceeded"}), 429
            
        # Basic input validation - only allow alphanumeric, hyphens, underscores
        if not node_id or not isinstance(node_id, str) or not node_id.replace('-', '').replace('_', '').isalnum():
            return jsonify({
                "error": "Invalid node identifier",
                "id": "invalid",
                "name": "Invalid Node",
                "description": "Node identifier contains invalid characters",
                "type": "error"
            }), 400
            
        try:
            result, status_code = node_details_helper.get_node_details(node_id)
            if status_code == 200:
                return jsonify(result)
            else:
                return jsonify(result), status_code
        except Exception as e:
            self.app.logger.error(f"Error getting node details for {node_id}")
            return jsonify({
                "error": "Could not load node details",
                "id": node_id,
                "name": "Error Loading Node",
                "description": "Could not load node details",
                "type": "error"
            }), 500

    def hierarchy_path(self, node_id):
        """Returns the path from root to the specified node."""
        # Check rate limit for API endpoints
        if not self.check_rate_limit():
            return jsonify({"error": "Rate limit exceeded"}), 429
            
        # Basic input validation - only allow alphanumeric, hyphens, underscores
        if not node_id or not isinstance(node_id, str) or not node_id.replace('-', '').replace('_', '').isalnum():
            return jsonify({"error": "Invalid node identifier"}), 400
            
        graph_data = self.build_graph_data()
        
        # Find the node
        target_node = None
        for node in graph_data["nodes"]:
            if node["id"] == node_id:
                target_node = node
                break
        
        if not target_node:
            return jsonify({"error": "Node not found"}), 404
        
        # Build the path
        path = [{"id": target_node["id"], "name": target_node["name"], "type": target_node["type"]}]
        
        # Traverse up the hierarchy
        current_node = target_node
        while "parent" in current_node:
            parent_id = current_node["parent"]
            parent_node = None
            
            for node in graph_data["nodes"]:
                if node["id"] == parent_id:
                    parent_node = node
                    break
            
            if parent_node:
                path.insert(0, {"id": parent_node["id"], "name": parent_node["name"], "type": parent_node["type"]})
                current_node = parent_node
            else:
                break
        
        return jsonify({"path": path})

    def health_check(self):
        """Check the health of the application and JSON file loading."""
        try:
            health_status = {
                "status": "ok",
                "root_data": False,
                "components": [],
                "subcomponents": [],
                "errors": []
            }
            
            # Check root data
            root_data = self.get_root_data()
            if root_data:
                health_status["root_data"] = True
            else:
                health_status["errors"].append(f"Failed to load root data from {self.ROOT_JSON_FILE}")
                
            # Check components
            if os.path.isdir(self.COMPONENTS_DIR):
                component_files = glob.glob(os.path.join(self.COMPONENTS_DIR, "*.json"))
                for file_path in component_files:
                    component_id = os.path.basename(file_path).replace(".json", "")
                    try:
                        data = self.load_json_file(file_path)
                        if data:
                            health_status["components"].append({
                                "id": component_id,
                                "status": "loaded",
                                "file": file_path
                            })
                        else:
                            health_status["components"].append({
                                "id": component_id,
                                "status": "failed",
                                "file": file_path
                            })
                            health_status["errors"].append(f"Failed to load component: {file_path}")
                    except Exception as e:
                        health_status["components"].append({
                            "id": component_id,
                            "status": "error",
                            "file": file_path,
                            "error": str(e)
                        })
                        health_status["errors"].append(f"Error loading component {file_path}: {str(e)}")
            else:
                health_status["errors"].append(f"Components directory not found: {self.COMPONENTS_DIR}")
                
            # Check subcomponents
            if os.path.isdir(self.SUBCOMPONENTS_DIR):
                subcomponent_files = glob.glob(os.path.join(self.SUBCOMPONENTS_DIR, "*.json"))
                for file_path in subcomponent_files:
                    subcomp_id = os.path.basename(file_path).replace(".json", "")
                    try:
                        data = self.load_json_file(file_path)
                        if data:
                            health_status["subcomponents"].append({
                                "id": subcomp_id,
                                "status": "loaded",
                                "file": file_path
                            })
                        else:
                            health_status["subcomponents"].append({
                                "id": subcomp_id,
                                "status": "failed",
                                "file": file_path
                            })
                            health_status["errors"].append(f"Failed to load subcomponent: {file_path}")
                    except Exception as e:
                        health_status["subcomponents"].append({
                            "id": subcomp_id,
                            "status": "error",
                            "file": file_path,
                            "error": str(e)
                        })
                        health_status["errors"].append(f"Error loading subcomponent {file_path}: {str(e)}")
            else:
                health_status["errors"].append(f"Subcomponents directory not found: {self.SUBCOMPONENTS_DIR}")
                
            if health_status["errors"]:
                health_status["status"] = "error"
                return jsonify(health_status), 500
                
            return jsonify(health_status)
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "error": str(e)
            }), 500

    def get_root_data(self):
        """Get the root AI Alignment data."""
        root_data = node_details_helper.load_json_file(self.ROOT_JSON_FILE)
        if not root_data:
            self.app.logger.warning(f"Using default root data since {self.ROOT_JSON_FILE} was not found")
            return node_details_helper.DEFAULT_ROOT_DATA
        return root_data

    def get_components(self):
        """Get all component data."""
        components = {}
        
        # Check if components directory exists
        if not os.path.isdir(self.COMPONENTS_DIR):
            self.app.logger.warning(f"Components directory not found: {self.COMPONENTS_DIR}")
            # Use components from the default data
            for component in node_details_helper.DEFAULT_ROOT_DATA["components"]:
                components[component["id"]] = component
            return components
        
        # Load components
        component_files = glob.glob(os.path.join(self.COMPONENTS_DIR, "*.json"))
        self.app.logger.info(f"Found {len(component_files)} component files")
        
        # If no component files found, use default components
        if not component_files:
            self.app.logger.warning("No component files found, using default components")
            for component in node_details_helper.DEFAULT_ROOT_DATA["components"]:
                components[component["id"]] = component
            return components
        
        for file_path in component_files:
            self.app.logger.debug(f"Loading component file: {file_path}")
            component_data = node_details_helper.load_json_file(file_path)
            if component_data:
                component_id = os.path.basename(file_path).replace(".json", "")
                components[component_id] = component_data
                self.app.logger.debug(f"Successfully loaded component: {component_id}")
            else:
                self.app.logger.error(f"Failed to load component file: {file_path}")
        
        # If no components were successfully loaded, use default components
        if not components:
            self.app.logger.warning("No components were successfully loaded, using default components")
            for component in node_details_helper.DEFAULT_ROOT_DATA["components"]:
                components[component["id"]] = component
        
        return components

    def get_subcomponents(self):
        """Get all subcomponent data."""
        subcomponents = {}
        
        if not os.path.isdir(self.SUBCOMPONENTS_DIR):
            self.app.logger.warning(f"Subcomponents directory not found: {self.SUBCOMPONENTS_DIR}")
            return subcomponents
        
        # Load subcomponents
        subcomponent_files = glob.glob(os.path.join(self.SUBCOMPONENTS_DIR, "*.json"))
        self.app.logger.info(f"Found {len(subcomponent_files)} subcomponent files")
        
        for file_path in subcomponent_files:
            self.app.logger.debug(f"Loading subcomponent file: {file_path}")
            data = node_details_helper.load_json_file(file_path)
            if data:
                subcomponent_id = os.path.basename(file_path).replace(".json", "")
                if "id" not in data:
                    data["id"] = subcomponent_id
                subcomponents[subcomponent_id] = data
                self.app.logger.debug(f"Successfully loaded subcomponent: {subcomponent_id}")
            else:
                self.app.logger.error(f"Failed to load subcomponent file: {file_path}")
        
        return subcomponents

    def load_json_file(self, file_path):
        """Load and parse a JSON file with robust error handling."""
        try:
            self.app.logger.info(f"Attempting to load file: {file_path}")
            data = node_details_helper.load_json_file(file_path)
            if data:
                self.app.logger.info(f"Successfully loaded {file_path}")
                return data
            else:
                self.app.logger.error(f"Failed to load {file_path}")
                return None
        except Exception as e:
            self.app.logger.error(f"Error loading {file_path}: {str(e)}")
            return None

    def root_details(self):
        # Check rate limit for API endpoints
        if not self.check_rate_limit():
            return jsonify({"error": "Rate limit exceeded"}), 429
            
        try:
            node_data, status_code = node_details_helper.get_node_details("ai-alignment")
            return jsonify(node_data), status_code
        except Exception as e:
            self.app.logger.error("Error in root_details")
            return jsonify({
                "error": "Server error processing root node"
            }), 500

    def audio_config(self):
        """Return audio configuration for the frontend."""
        # Check rate limit for API endpoints
        if not self.check_rate_limit():
            return jsonify({"error": "Rate limit exceeded"}), 429
            
        try:
            return jsonify(config.AUDIO_CONFIG)
        except Exception as e:
            self.app.logger.error("Error getting audio config")
            return jsonify({
                "error": "Unable to load audio configuration",
                "fallback_to_generated": True
            }), 500

    def build_graph_data(self):
        """Build visualization graph data with nodes and links."""
        try:
            # Get data sources
            root_data = self.get_root_data()
            if not isinstance(root_data, dict):
                self.app.logger.error(f"Root data is not a dictionary: {type(root_data)}")
                return {"nodes": [], "links": [], "error": "Root data is not valid"}
                
            components = self.get_components()
            subcomponents = self.get_subcomponents()
            
            # Create nodes and links with optimized data structures
            nodes = []
            links = []
            node_map = {}  # For faster lookups
            
            # Add root node
            root_node = {
                "id": root_data.get("id", "ai-alignment"),
                "name": root_data.get("name", "AI Alignment"),
                "type": "component_group",
                "description": root_data.get("description", "AI Alignment"),
                "level": 0,
                "expandable": True,
                "has_children": bool(components)  # Faster than len() check
            }
            nodes.append(root_node)
            node_map[root_node["id"]] = root_node
            
            # Add component nodes with batch processing
            for component_id, component in components.items():
                if not isinstance(component, dict):
                    self.app.logger.warning(f"Component {component_id} is not a dictionary, skipping")
                    continue
                    
                # Check if this component has any subcomponents - use set for faster lookup
                component_subcomponents = {s_id: s for s_id, s in subcomponents.items() 
                                        if isinstance(s, dict) and "parent" in s and s["parent"] == component_id}
                has_children = bool(component_subcomponents)
                
                component_node = {
                    "id": component_id,
                    "name": component.get("name", component_id),
                    "type": "component",
                    "description": component.get("description", ""),
                    "parent": root_node["id"],
                    "level": 1,
                    "expandable": has_children,
                    "has_children": has_children
                }
                nodes.append(component_node)
                node_map[component_id] = component_node
                
                # Add link from root to component
                links.append({
                    "source": root_node["id"],
                    "target": component_id,
                    "type": "contains"
                })
                
                # Process subcomponents in batches
                for subcomp_id, subcomp in component_subcomponents.items():
                    capabilities = []
                    if "capabilities" in subcomp:
                        cap_obj = subcomp["capabilities"]
                        if isinstance(cap_obj, list):
                            capabilities = cap_obj
                        elif isinstance(cap_obj, dict) and "items" in cap_obj:
                            capabilities = cap_obj["items"]
                        else:
                            self.app.logger.warning(f"Unexpected capabilities format in {subcomp_id}: {type(cap_obj)}")
                    
                    has_children = bool(capabilities)
                    
                    subcomp_node = {
                        "id": subcomp_id,
                        "name": subcomp.get("name", subcomp_id),
                        "type": "subcomponent",
                        "description": subcomp.get("description", ""),
                        "parent": component_id,
                        "level": 2,
                        "expandable": has_children,
                        "has_children": has_children
                    }
                    nodes.append(subcomp_node)
                    node_map[subcomp_id] = subcomp_node
                    
                    links.append({
                        "source": component_id,
                        "target": subcomp_id,
                        "type": "contains"
                    })
                    
                    # Now add capabilities and their deeper descendants
                    for capability in capabilities:
                        if not isinstance(capability, dict):
                            self.app.logger.warning(f"Capability in {subcomp_id} is not a dictionary, skipping")
                            continue
                            
                        capability_id = capability.get("id", f"{subcomp_id}-capability-{len(nodes)}")
                        functions = capability.get("functions", [])
                        has_capability_children = bool(functions)
                        
                        capability_node = {
                            "id": capability_id,
                            "name": capability.get("name", "Capability"),
                            "type": "capability",
                            "description": capability.get("description", ""),
                            "parent": subcomp_id,
                            "level": 3,
                            "expandable": has_capability_children,
                            "has_children": has_capability_children
                        }
                        
                        nodes.append(capability_node)
                        node_map[capability_id] = capability_node
                        
                        links.append({
                            "source": subcomp_id,
                            "target": capability_id,
                            "type": "has_capability"
                        })
                        
                        # Add functions
                        for function in functions:
                            if not isinstance(function, dict):
                                self.app.logger.warning(f"Function in {capability_id} is not a dictionary, skipping")
                                continue
                                
                            function_id = function.get("id", f"{capability_id}-function-{len(nodes)}")
                            specifications = function.get("specifications", [])
                            has_function_children = bool(specifications)
                            
                            function_node = {
                                "id": function_id,
                                "name": function.get("name", "Function"),
                                "type": "function",
                                "description": function.get("description", ""),
                                "parent": capability_id,
                                "level": 4,
                                "expandable": has_function_children,
                                "has_children": has_function_children
                            }
                            
                            nodes.append(function_node)
                            node_map[function_id] = function_node
                            
                            links.append({
                                "source": capability_id,
                                "target": function_id,
                                "type": "has_function"
                            })
                            
                            # Add specifications
                            for spec in specifications:
                                if not isinstance(spec, dict):
                                    self.app.logger.warning(f"Specification in {function_id} is not a dictionary, skipping")
                                    continue
                                    
                                spec_id = spec.get("id", f"{function_id}-spec-{len(nodes)}")
                                integration = spec.get("integration")
                                has_spec_children = bool(integration)
                                
                                spec_node = {
                                    "id": spec_id,
                                    "name": spec.get("name", "Specification"),
                                    "type": "specification",
                                    "description": spec.get("description", ""),
                                    "parent": function_id,
                                    "level": 5,
                                    "expandable": has_spec_children,
                                    "has_children": has_spec_children
                                }
                                
                                nodes.append(spec_node)
                                node_map[spec_id] = spec_node
                                
                                links.append({
                                    "source": function_id,
                                    "target": spec_id,
                                    "type": "has_specification"
                                })
                                
                                # Add integration if present
                                if integration and isinstance(integration, dict):
                                    integration_id = integration.get("id", f"{spec_id}-integration-{len(nodes)}")
                                    techniques = integration.get("techniques", [])
                                    has_integration_children = bool(techniques)
                                    
                                    integration_node = {
                                        "id": integration_id,
                                        "name": integration.get("name", "Integration"),
                                        "type": "integration",
                                        "description": integration.get("description", ""),
                                        "parent": spec_id,
                                        "level": 6,
                                        "expandable": has_integration_children,
                                        "has_children": has_integration_children
                                    }
                                    
                                    nodes.append(integration_node)
                                    node_map[integration_id] = integration_node
                                    
                                    links.append({
                                        "source": spec_id,
                                        "target": integration_id,
                                        "type": "has_integration"
                                    })
                                    
                                    # Add techniques 
                                    for technique in techniques:
                                        if not isinstance(technique, dict):
                                            self.app.logger.warning(f"Technique in {integration_id} is not a dictionary, skipping")
                                            continue
                                            
                                        technique_id = technique.get("id", f"{integration_id}-technique-{len(nodes)}")
                                        applications = technique.get("applications", [])
                                        has_technique_children = bool(applications)
                                        
                                        technique_node = {
                                            "id": technique_id,
                                            "name": technique.get("name", "Technique"),
                                            "type": "technique",
                                            "description": technique.get("description", ""),
                                            "parent": integration_id,
                                            "level": 7,
                                            "expandable": has_technique_children,
                                            "has_children": has_technique_children
                                        }
                                        
                                        nodes.append(technique_node)
                                        node_map[technique_id] = technique_node
                                        
                                        links.append({
                                            "source": integration_id,
                                            "target": technique_id,
                                            "type": "has_technique"
                                        })
                                        
                                        # Add applications (deeper level)
                                        for app in applications:
                                            if not isinstance(app, dict):
                                                self.app.logger.warning(f"Application in {technique_id} is not a dictionary, skipping")
                                                continue
                                                
                                            app_id = app.get("id", f"{technique_id}-app-{len(nodes)}")
                                            
                                            # Get inputs and directly extract outputs
                                            inputs = app.get("inputs", [])
                                            standalone_outputs = app.get("outputs", [])  # Some apps have direct outputs
                                            nested_outputs = []  # Outputs from inputs
                                            
                                            # Extract all outputs from inputs
                                            for input_item in inputs:
                                                if isinstance(input_item, dict) and "outputs" in input_item:
                                                    input_outputs = input_item.get("outputs", [])
                                                    if isinstance(input_outputs, list):
                                                        nested_outputs.extend(input_outputs)
                                                    elif isinstance(input_outputs, dict):
                                                        nested_outputs.append(input_outputs)
                                            
                                            # Combine all outputs
                                            outputs = standalone_outputs + nested_outputs
                                            
                                            # Ensure uniqueness by ID
                                            unique_outputs = []
                                            output_ids = set()
                                            for output in outputs:
                                                if not isinstance(output, dict):
                                                    continue
                                                output_id = output.get("id")
                                                if output_id and output_id not in output_ids:
                                                    output_ids.add(output_id)
                                                    unique_outputs.append(output)
                                                elif not output_id:  # If no ID, include anyway
                                                    unique_outputs.append(output)
                                            
                                            outputs = unique_outputs
                                            has_app_children = bool(inputs) or bool(outputs)
                                            
                                            app_node = {
                                                "id": app_id,
                                                "name": app.get("name", "Application"),
                                                "type": "application",
                                                "description": app.get("description", ""),
                                                "parent": technique_id,
                                                "level": 8,
                                                "expandable": has_app_children,
                                                "has_children": has_app_children
                                            }
                                            
                                            nodes.append(app_node)
                                            node_map[app_id] = app_node
                                            
                                            links.append({
                                                "source": technique_id,
                                                "target": app_id,
                                                "type": "has_application"
                                            })
                                            
                                            # Add inputs as direct children of application
                                            for input_item in inputs:
                                                if not isinstance(input_item, dict):
                                                    continue
                                                    
                                                input_id = input_item.get("id", f"{app_id}-input-{len(nodes)}")
                                                
                                                input_node = {
                                                    "id": input_id,
                                                    "name": input_item.get("name", "Input"),
                                                    "type": "input",
                                                    "description": input_item.get("description", ""),
                                                    "parent": app_id,
                                                    "level": 9,
                                                    "expandable": False,
                                                    "has_children": False
                                                }
                                                
                                                nodes.append(input_node)
                                                node_map[input_id] = input_node
                                                
                                                links.append({
                                                    "source": app_id,
                                                    "target": input_id,
                                                    "type": "has_input"
                                                })
                                            
                                            # Add outputs as direct children of application (siblings to inputs)
                                            for output_idx, output_item in enumerate(outputs):
                                                if not isinstance(output_item, dict):
                                                    continue
                                                    
                                                # Ensure output has a good ID to avoid clashes
                                                if "id" in output_item and output_item["id"]:
                                                    output_id = output_item["id"]
                                                else:
                                                    output_id = f"{app_id}-output-{output_idx}"
                                                    
                                                output_node = {
                                                    "id": output_id,
                                                    "name": output_item.get("name", f"Output {output_idx+1}"),
                                                    "type": "output",
                                                    "description": output_item.get("description", ""),
                                                    "parent": app_id,  # Direct child of application
                                                    "level": 9,        # Same level as inputs
                                                    "expandable": False,
                                                    "has_children": False
                                                }
                                                
                                                # Only add if not already in nodes
                                                if output_id not in node_map:
                                                    nodes.append(output_node)
                                                    node_map[output_id] = output_node
                                                    
                                                    links.append({
                                                        "source": app_id,
                                                        "target": output_id,
                                                        "type": "has_output"
                                                    })
            
            # Process cross-connections and additional relationships
            for component_id, component in components.items():
                if not isinstance(component, dict):
                    continue
                    
                # Handle component relationships
                if "relationships" in component:
                    relationships = component["relationships"]
                    if isinstance(relationships, list):
                        for rel in relationships:
                            if not isinstance(rel, dict):
                                continue
                                
                            rel_id = rel.get("id")
                            rel_type = rel.get("relationship_type")
                            if rel_id and rel_type:
                                links.append({
                                    "source": component_id,
                                    "target": rel_id,
                                    "type": rel_type,
                                    "description": rel.get("description", "")
                                })
                                
                                # Add integration points if they exist
                                if "integration_points" in rel:
                                    for point in rel["integration_points"]:
                                        if isinstance(point, dict) and "this_component_function" in point and "other_component_function" in point:
                                            links.append({
                                                "source": point["this_component_function"],
                                                "target": point["other_component_function"],
                                                "type": "integration_point",
                                                "description": point.get("description", "")
                                            })
                    else:
                        self.app.logger.warning(f"Relationships in {component_id} is not a list: {type(relationships)}")

            # Process subcomponent cross-connections
            for subcomp_id, subcomp in subcomponents.items():
                if not isinstance(subcomp, dict):
                    continue
                    
                if "cross_connections" in subcomp:
                    connections = subcomp["cross_connections"]
                    if isinstance(connections, list):
                        for conn in connections:
                            if not isinstance(conn, dict):
                                continue
                                
                            source_id = conn.get("source_id")
                            target_id = conn.get("target_id")
                            conn_type = conn.get("type")
                            if source_id and target_id and conn_type:
                                links.append({
                                    "source": source_id,
                                    "target": target_id,
                                    "type": conn_type,
                                    "description": conn.get("description", "")
                                })
                    else:
                        self.app.logger.warning(f"Cross connections in {subcomp_id} is not a list: {type(connections)}")

            # Process capability implementations
            for subcomp_id, subcomp in subcomponents.items():
                if not isinstance(subcomp, dict):
                    continue
                    
                if "capabilities" in subcomp:
                    capabilities = subcomp["capabilities"]
                    if isinstance(capabilities, list):
                        for cap in capabilities:
                            if not isinstance(cap, dict):
                                continue
                                
                            if "implements_component_capabilities" in cap:
                                impls = cap["implements_component_capabilities"]
                                if isinstance(impls, list):
                                    for impl_cap in impls:
                                        links.append({
                                            "source": cap.get("id", ""),
                                            "target": impl_cap,
                                            "type": "implements",
                                            "description": "Implements component capability"
                                        })
                                else:
                                    self.app.logger.warning(f"Implements component capabilities in {cap.get('id', '')} is not a list: {type(impls)}")
                    else:
                        self.app.logger.warning(f"Capabilities in {subcomp_id} is not a list: {type(capabilities)}")

            # Process function implementations
            for subcomp_id, subcomp in subcomponents.items():
                if not isinstance(subcomp, dict):
                    continue
                    
                if "functions" in subcomp:
                    functions = subcomp["functions"]
                    if isinstance(functions, list):
                        for func in functions:
                            if not isinstance(func, dict):
                                continue
                                
                            if "implements_component_functions" in func:
                                impls = func["implements_component_functions"]
                                if isinstance(impls, list):
                                    for impl_func in impls:
                                        links.append({
                                            "source": func.get("id", ""),
                                            "target": impl_func,
                                            "type": "implements",
                                            "description": "Implements component function"
                                        })
                                else:
                                    self.app.logger.warning(f"Implements component functions in {func.get('id', '')} is not a list: {type(impls)}")
                    else:
                        self.app.logger.warning(f"Functions in {subcomp_id} is not a list: {type(functions)}")

            self.app.logger.info(f"Built comprehensive graph with {len(nodes)} nodes and {len(links)} links")
            return {"nodes": nodes, "links": links}
        except Exception as e:
            self.app.logger.error(f"Error in build_graph_data: {str(e)}", exc_info=True)
            # Return an empty graph rather than failing completely
            return {"nodes": [], "links": [], "error": str(e)}

# Create and run the application
def create_app():
    visualizer = AIAlignmentVisualizer()
    app = visualizer.app

    # Add routes that need to use the app instance directly
    @app.route('/api/details/<node_id>')
    def node_details_route(node_id):
        # Check rate limit for API endpoints
        if not visualizer.check_rate_limit():
            return jsonify({"error": "Rate limit exceeded"}), 429
            
        # Basic input validation - only allow alphanumeric, hyphens, underscores
        if not node_id or not isinstance(node_id, str) or not node_id.replace('-', '').replace('_', '').isalnum():
            return jsonify({
                "error": "Invalid node identifier",
                "id": "invalid",
                "name": "Invalid Node",
                "description": "Node identifier contains invalid characters",
                "type": "error"
            }), 400
            
        try:
            # Use the new helper module for all node requests
            node_data, status_code = node_details_helper.get_node_details(node_id)
            return jsonify(node_data), status_code
        except Exception as e:
            app.logger.error(f"Error in node_details_route for {node_id}")
            return jsonify({
                "error": "Server error processing node",
                "id": node_id,
                "name": "Error Loading Node",
                "description": "Could not load node details",
                "type": "error"
            }), 500
    
    # Add a specific route for the root node
    @app.route('/api/root')
    def root_node():
        # Check rate limit for API endpoints
        if not visualizer.check_rate_limit():
            return jsonify({"error": "Rate limit exceeded"}), 429
            
        try:
            node_data, status_code = node_details_helper.get_node_details("ai-alignment")
            return jsonify(node_data), status_code
        except Exception as e:
            app.logger.error("Error in root_node")
            return jsonify({
                "error": "Server error processing root node"
            }), 500

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def server_error(error):
        app.logger.error(f"Server error: {error}")
        return jsonify({"error": "Internal server error"}), 500

    # Security headers and CORS configuration
    @app.after_request
    def after_request(response):
        # Basic security headers
        for header, value in config.SECURITY_HEADERS.items():
            response.headers[header] = value
        
        # Content Security Policy
        response.headers['Content-Security-Policy'] = config.CSP_POLICY
        
        # CORS - only allow your domain and Vercel preview URLs
        if request.path.startswith('/api/'):
            origin = request.headers.get('Origin')
            
            # Check if origin is in allowed list
            origin_allowed = False
            
            if origin in config.ALLOWED_ORIGINS:
                origin_allowed = True
            elif origin and hasattr(config, 'VERCEL_PREVIEW_PATTERN'):
                # Check if origin matches Vercel preview pattern
                if re.match(config.VERCEL_PREVIEW_PATTERN, origin):
                    origin_allowed = True
            
            if origin_allowed:
                response.headers['Access-Control-Allow-Origin'] = origin
            else:
                # For direct API access (no origin header), allow it for now
                # This is common for direct API calls and testing
                if not origin:
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            response.headers['Access-Control-Allow-Methods'] = 'GET'
        return response

    return app

app = create_app()

# Define absolute paths correctly for Windows environment
APP_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.abspath(os.path.join(APP_DIR, ".."))
COMPONENTS_DIR = os.path.normpath(os.path.join(PARENT_DIR, "components"))
SUBCOMPONENTS_DIR = os.path.normpath(os.path.join(PARENT_DIR, "subcomponents"))
ROOT_JSON_FILE = os.path.normpath(os.path.join(PARENT_DIR, "ai-alignment.json"))

# Print paths to verify
app.logger.info(f"APP_DIR: {APP_DIR}")
app.logger.info(f"PARENT_DIR: {PARENT_DIR}")
app.logger.info(f"COMPONENTS_DIR: {COMPONENTS_DIR}")
app.logger.info(f"SUBCOMPONENTS_DIR: {SUBCOMPONENTS_DIR}")
app.logger.info(f"ROOT_JSON_FILE: {ROOT_JSON_FILE}")

# Default data to use if files aren't found
DEFAULT_ROOT_DATA = {
    "id": "ai-alignment",
    "name": "AI Alignment",
    "description": "Methods to ensure AI systems remain aligned with human values and intentions.",
    "type": "component_group",
    "components": [
        {
            "id": "technical-safeguards",
            "name": "Technical Safeguards",
            "description": "Engineering approaches to ensure AI systems behave as intended"
        },
        {
            "id": "value-learning",
            "name": "Value Learning",
            "description": "Systems that enable AI to learn and internalize human values"
        },
        {
            "id": "interpretability-tools",
            "name": "Interpretability Tools",
            "description": "Methods to understand AI reasoning and decision-making"
        },
        {
            "id": "oversight-mechanisms",
            "name": "Oversight Mechanisms",
            "description": "Systems for monitoring and evaluating AI behavior"
        }
    ]
}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    print(f"Starting AI Alignment Visualization on http://localhost:{port}/")
    visualizer = AIAlignmentVisualizer()
    visualizer.run(port=port) 