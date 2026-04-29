import os
import sys
import asyncio
import re
from datetime import datetime
from typing import Type, Callable, List, Dict, Any, Optional
from loguru import logger
from rich.console import Console
from pyegeria import EgeriaTech, PyegeriaException, print_basic_exception

# Use local md_processing
from md_processing.md_processing_utils.md_processing_constants import (
    load_commands, get_command_spec, build_command_variants, 
    PROJECT_SUBTYPES, COLLECTION_SUBTYPES, COMMAND_DEFINITIONS
)
from md_processing.v2 import (
    UniversalExtractor, V2Dispatcher, AsyncBaseCommandProcessor,
    TermProcessor, TermRelationshipProcessor,
    DataCollectionProcessor, DataStructureProcessor, DataFieldProcessor, DataClassProcessor,
    BlueprintProcessor, ComponentProcessor, SupplyChainProcessor, SolutionLinkProcessor,
    SolutionArchitectProcessor,
    ProjectProcessor, ProjectLinkProcessor,
    CollectionManagerProcessor, CSVElementProcessor, CollectionLinkProcessor,
    GovernanceProcessor, GovernanceLinkProcessor, GovernanceContextProcessor,
    FeedbackProcessor, TagProcessor, ExternalReferenceProcessor, FeedbackLinkProcessor,
    ViewProcessor
)

# Configuration from environment
EGERIA_WIDTH = os.environ.get("EGERIA_WIDTH", "100")
EGERIA_ROOT_PATH = os.environ.get("EGERIA_ROOT_PATH", "/")
EGERIA_INBOX_PATH = os.environ.get("EGERIA_INBOX_PATH", "dr-egeria-inbox")
EGERIA_OUTBOX_PATH = os.environ.get("EGERIA_OUTBOX_PATH", "dr-egeria-outbox")

# Initial load
load_commands()

# Data Designer
try:
    from md_processing.v2.data_designer import (
        DataValueSpecificationProcessor, LinkDataFieldProcessor, LinkFieldToStructureProcessor,
        LinkDataValueDefinitionProcessor, LinkDataValueCompositionProcessor,
        LinkDataClassCompositionProcessor, LinkCertificationTypeToStructureProcessor,
        AttachDataDescriptionProcessor, AssignDataValueSpecificationProcessor,
        AttachDataValueSpecificationProcessor
    )
except ImportError as e:
    logger.warning(f"Some Data Designer processors could not be imported: {e}")
    # Initialize with None to allow conditional registration
    DataValueSpecificationProcessor = globals().get('DataValueSpecificationProcessor')
    LinkDataFieldProcessor = globals().get('LinkDataFieldProcessor')
    LinkFieldToStructureProcessor = globals().get('LinkFieldToStructureProcessor')
    LinkDataValueDefinitionProcessor = globals().get('LinkDataValueDefinitionProcessor')
    LinkDataValueCompositionProcessor = globals().get('LinkDataValueCompositionProcessor')
    LinkDataClassCompositionProcessor = globals().get('LinkDataClassCompositionProcessor')
    LinkCertificationTypeToStructureProcessor = globals().get('LinkCertificationTypeToStructureProcessor')
    AttachDataDescriptionProcessor = globals().get('AttachDataDescriptionProcessor')
    AssignDataValueSpecificationProcessor = globals().get('AssignDataValueSpecificationProcessor')
    AttachDataValueSpecificationProcessor = globals().get('AttachDataValueSpecificationProcessor')

def register_solution_architect_processors(register_processor_fn: Callable):
    specs = COMMAND_DEFINITIONS.get("Command Specifications", {})
    link_verbs = {"Link", "Attach", "Add", "Detach", "Unlink", "Remove"}
    for base_name, spec in specs.items():
        if not isinstance(spec, dict) or spec.get("family") != "Solution Architect":
            continue
        
        # Determine processor class
        if base_name.split(" ", 1)[0] in link_verbs:
            processor_cls = SolutionLinkProcessor
        elif "Blueprint" in base_name:
            processor_cls = BlueprintProcessor
        elif "Component" in base_name and "Link" not in base_name:
            processor_cls = ComponentProcessor
        elif "Information Supply Chain" in base_name and "Link" not in base_name:
            processor_cls = SupplyChainProcessor
        else:
            processor_cls = SolutionArchitectProcessor
        register_processor_fn(base_name, processor_cls)

def register_governance_processors(register_processor_fn: Callable):
    specs = COMMAND_DEFINITIONS.get("Command Specifications", {})
    for base_name, spec in specs.items():
        if not isinstance(spec, dict) or spec.get("family") != "Governance":
            continue
        if "Context" in base_name:
            processor_cls = GovernanceContextProcessor
        elif "Link" in base_name or "Attach" in base_name or "Add" in base_name:
            processor_cls = GovernanceLinkProcessor
        else:
            processor_cls = GovernanceProcessor
        register_processor_fn(base_name, processor_cls)

def setup_dispatcher(client: EgeriaTech) -> V2Dispatcher:
    dispatcher = V2Dispatcher(client)
    
    def normalize_command_key(key: str) -> str:
        return re.sub(r'\s+', ' ', key).strip() if key else key

    def register_processor(base_command: str, processor_cls: Type[AsyncBaseCommandProcessor]):
        spec = get_command_spec(base_command)
        registered = set()
        if spec:
            alternate_names = spec.get('alternate_names', [])
            if isinstance(alternate_names, str):
                alternate_names = [alternate_names]
            for name in [base_command, spec.get('display_name', '')] + alternate_names:
                key = normalize_command_key(name)
                if key and key not in registered:
                    dispatcher.register(key, processor_cls)
                    registered.add(key)
            variants = build_command_variants(base_command, spec)
            for variant in variants:
                vkey = normalize_command_key(variant)
                if vkey and vkey not in registered:
                    dispatcher.register(vkey, processor_cls)
                    registered.add(vkey)
        else:
            dispatcher.register(normalize_command_key(base_command), processor_cls)

    # Core Processors
    register_processor("Create Glossary Term", TermProcessor)
    register_processor("Link Term-Term Relationship", TermRelationshipProcessor)
    register_processor("Unlink Term-Term Relationship", TermRelationshipProcessor)
    register_processor("Remove Term-Term Relationship", TermRelationshipProcessor)
    register_processor("Detach Term-Term Relationship", TermRelationshipProcessor)
    
    register_processor("Create Data Specification", DataCollectionProcessor)
    register_processor("Create Data Dictionary", DataCollectionProcessor)
    register_processor("Create Data Structure", DataStructureProcessor)
    register_processor("Create Data Field", DataFieldProcessor)
    register_processor("Create Data Class", DataClassProcessor)
    if DataValueSpecificationProcessor:
        register_processor("Create Data Value Specification", DataValueSpecificationProcessor)
        register_processor("Update Data Value Specification", DataValueSpecificationProcessor)
    if LinkDataFieldProcessor:
        register_processor("Link Data Field", LinkDataFieldProcessor)
    if LinkFieldToStructureProcessor:
        register_processor("Link Field to Structure", LinkFieldToStructureProcessor)
    if LinkDataValueDefinitionProcessor:
        register_processor("Link Data Value Definition", LinkDataValueDefinitionProcessor)
    if LinkDataValueCompositionProcessor:
        register_processor("Link Data Value Composition", LinkDataValueCompositionProcessor)
    if LinkDataClassCompositionProcessor:
        register_processor("Link Data Class Composition", LinkDataClassCompositionProcessor)
    if LinkCertificationTypeToStructureProcessor:
        register_processor("Link Certification Type to Data Structure", LinkCertificationTypeToStructureProcessor)
    if AttachDataDescriptionProcessor:
        register_processor("Attach Data Description to Element", AttachDataDescriptionProcessor)
    if AssignDataValueSpecificationProcessor:
        register_processor("Assign Data Value Specification", AssignDataValueSpecificationProcessor)
    if AttachDataValueSpecificationProcessor:
        register_processor("Attach Data Value Specification to Element", AttachDataValueSpecificationProcessor)

    # Families
    register_solution_architect_processors(register_processor)
    register_governance_processors(register_processor)

    # Project
    register_processor("Create Project", ProjectProcessor)
    register_processor("Link Project Dependency", ProjectLinkProcessor)
    register_processor("Link Project Hierarchy", ProjectLinkProcessor)
    for proj_type in PROJECT_SUBTYPES:
        register_processor(f"Create {proj_type}", ProjectProcessor)
        register_processor(f"Update {proj_type}", ProjectProcessor)

    # Collection Manager
    for coll_type in COLLECTION_SUBTYPES:
        register_processor(f"Create {coll_type}", CollectionManagerProcessor)
        register_processor(f"Update {coll_type}", CollectionManagerProcessor)
    register_processor("Create CSV Element", CSVElementProcessor)
    register_processor("Add Member to Collection", CollectionLinkProcessor)
    register_processor("Link Agreement Item", CollectionLinkProcessor)
    register_processor("Link Agreement Actor", CollectionLinkProcessor)
    register_processor("Link Product Dependency", CollectionLinkProcessor)
    register_processor("Link Product-Product", CollectionLinkProcessor)
    register_processor("Attach Collection to Resource", CollectionLinkProcessor)
    register_processor("Link Digital Subscriber", CollectionLinkProcessor)

    # Feedback & Reporting
    register_processor("View Report", ViewProcessor)
    register_processor("Add Comment", FeedbackProcessor)
    register_processor("Update Comment", FeedbackProcessor)
    register_processor("Create Journal Entry", FeedbackProcessor)
    register_processor("Create Informal Tag", TagProcessor)
    register_processor("Link Tag", FeedbackLinkProcessor)
    register_processor("Attach Tag to Element", FeedbackLinkProcessor)
    register_processor("Create External Reference", ExternalReferenceProcessor)
    register_processor("Update External Reference", ExternalReferenceProcessor)
    register_processor("Link External Reference", FeedbackLinkProcessor)
    register_processor("Attach External Reference to Element", FeedbackLinkProcessor)

    return dispatcher

async def process_md_file_async(input_file: str, output_folder: str, directive: str, 
                                server: str, url: str, userid: str, user_pass: str,
                                outbox_path: Optional[str] = None) -> None:
    console = Console(width=int(EGERIA_WIDTH))
    client = EgeriaTech(server, url, user_id=userid)
    client.create_egeria_bearer_token(userid, user_pass)
    
    dispatcher = setup_dispatcher(client)
    
    # Construct the full file path. 
    # Use os.path.normpath to avoid issues like /./filename
    if os.path.isabs(input_file):
        full_file_path = os.path.normpath(input_file)
    else:
        full_file_path = os.path.normpath(os.path.join(EGERIA_ROOT_PATH, EGERIA_INBOX_PATH, input_file))
    
    # Fallback search if not found at primary path
    if not os.path.exists(full_file_path):
        mount_points = ["/work", "/coco-workbooks", "/work/Work-Obsidian"]
        for mp in mount_points:
            fallback = os.path.normpath(os.path.join(mp, input_file.lstrip("/")))
            if os.path.exists(fallback):
                full_file_path = fallback
                break
                
    if not os.path.exists(full_file_path):
        console.print(f"[bold red]Error:[/bold red] File not found at {full_file_path}")
        return

    try:
        with open(full_file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] Failed to read {full_file_path}: {e}")
        return

    extractor = UniversalExtractor(content)
    commands = extractor.extract_commands()
    
    if not commands:
        console.print(f"[bold yellow]Warning:[/bold yellow] No valid Egeria commands found in {input_file}")
        return

    results = await dispatcher.dispatch_batch(commands, context={"directive": directive})
    
    # Aggregate output and write to file
    final_output = ""
    for res in results:
        if res.get("output"):
            final_output += res["output"] + "\n\n"
    
    # Determine output filename: <input_file_name>-processed-<date-time>.md
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_file_name = f"{base_name}-processed-{ts}.md"
    
    effective_outbox = outbox_path if outbox_path else EGERIA_OUTBOX_PATH
    
    # Handle absolute vs relative paths for outbox
    # If it starts with 'work/', we assume it's relative to / (since /work is mounted)
    if os.path.isabs(effective_outbox):
        full_output_dir = os.path.join(effective_outbox, output_folder)
    elif effective_outbox.startswith("work/") or effective_outbox.startswith("coco-workbooks/"):
        full_output_dir = os.path.join("/", effective_outbox, output_folder)
    else:
        full_output_dir = os.path.join(EGERIA_ROOT_PATH, effective_outbox, output_folder)
        
    # Standardize path: remove redundant slashes and resolve any .. segments
    full_output_dir = os.path.normpath(full_output_dir)
    os.makedirs(full_output_dir, exist_ok=True)
    full_output_path = os.path.join(full_output_dir, out_file_name)
    
    try:
        with open(full_output_path, 'w') as f:
            f.write(final_output)
        console.print(f"\n[bold green]Success:[/bold green] Output written to {full_output_path}")
        console.print(f"Output file: {out_file_name}")
        console.print(f"Output path: {full_output_path}")
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] Failed to write output file: {e}")

    # Print results back to console (which is captured by the web handler)
    for res in results:
        if res.get("output"):
            console.print(res["output"])
    
    # Final success/failure summary
    has_errors = any(res.get("status") == "failure" for res in results)
    if has_errors:
        console.print(f"\n[bold red]Status:[/bold red] Processing finished with errors.")
    else:
        console.print(f"\n[bold green]Status:[/bold green] Processing finished successfully.")

def process_markdown_file(input_file: str, output_folder: str, directive: str, 
                        server: str, url: str, userid: str, user_pass: str,
                        outbox_path: Optional[str] = None) -> None:
    """Synchronous wrapper for backward compatibility with existing pyegeria_handler.py and mcp_server.py"""
    try:
        asyncio.run(process_md_file_async(input_file, output_folder, directive, server, url, userid, user_pass, outbox_path))
    except Exception as e:
        print(f"Async processing failed: {e}")

# Alias for backward compatibility
process_md_file = process_markdown_file
