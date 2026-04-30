import { App, Modal, Notice, Plugin, PluginSettingTab, Setting, TFile, moment } from "obsidian";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";

interface CallingTheDrSettings {
    mcpUrl: string;
    mcpToken: string;
    userId: string;
    userPass: string;
    egeriaUrl: string;
    viewServer: string;
    defaultDirective: string;
    outboxPath: string;
    inputPath: string;
    verbose: boolean;
}

const DEFAULT_SETTINGS: CallingTheDrSettings = {
    mcpUrl: "http://localhost:8000/sse",
    mcpToken: "egeria-secret-mcp-token",
    userId: "erinoverview",
    userPass: "secret",
    egeriaUrl: "https://host.docker.internal:9443",
    viewServer: "qs-view-server",
    defaultDirective: "process",
    outboxPath: "dr-egeria-outbox",
    inputPath: "",
    verbose: true
};

export default class CallingTheDrPlugin extends Plugin {
    settings: CallingTheDrSettings = DEFAULT_SETTINGS;

    async onload() {
        await this.loadSettings();

        // Ribbon icon: Doctor's Bag
        this.addRibbonIcon("briefcase", "Calling the Dr. (MCP)", async () => {
            await this.runMcpBlock();
        });

        this.addCommand({
            id: "run-mcp-block",
            name: "Run Note via MCP",
            callback: async () => {
                await this.runMcpBlock();
            }
        });

        this.addSettingTab(new CallingTheDrSettingTab(this.app, this));
    }

    async runMcpBlock() {
        const file = this.app.workspace.getActiveFile();
        if (!file) {
            new Notice("No active file.");
            return;
        }

        const content = await this.app.vault.read(file);
        
        // Keep the notice until the results come
        const notice = new Notice("Calling the Dr. via MCP SSE...", 0);

        try {
            const url = new URL(this.settings.mcpUrl);
            url.searchParams.set("token", this.settings.mcpToken);

            const transport = new SSEClientTransport(url);

            const client = new Client({
                name: "Calling the Dr. Obsidian Plugin",
                version: "0.1.0"
            }, {
                capabilities: {}
            });

            await client.connect(transport);
            console.log("MCP Client connected to", this.settings.mcpUrl);

            const result = await client.callTool({
                name: "dr_egeria_run_block",
                arguments: {
                    markdown_block: content,
                    url: this.settings.egeriaUrl,
                    server_name: this.settings.viewServer,
                    user_id: this.settings.userId,
                    user_pass: this.settings.userPass,
                    directive: this.settings.defaultDirective,
                    output_folder: "", // can add this to settings later if needed
                    outbox_path: this.settings.outboxPath,
                    input_file: this.settings.inputPath ? `${this.settings.inputPath}/${file.name}` : file.name
                }
            }) as any;

        const textResult = (result.content as any[])
            .filter((c: any) => c.type === "text")
            .map((c: any) => c.text)
            .join("\n");
        
        console.log("MCP Tool result received:", result);
        console.log("Extracted text result length:", textResult.length);

        const directiveUsed = this.settings.defaultDirective;
        
        let headerStatus = "✅ Success";
        if (textResult.toLowerCase().includes("error:")) {
            headerStatus = "❌ Error";
        } else if (textResult.toLowerCase().includes("warning:")) {
            headerStatus = "⚠️ Warning";
        }

        // V3: Write the result to the vault if it's a "process" directive and we have content
        let fileSavedMessage = "";
        if (directiveUsed === "process" && textResult && !textResult.startsWith("Error:") && !textResult.startsWith("Warning:")) {
            try {
                const outboxFolder = this.settings.outboxPath || "dr-egeria-outbox";
                // Ensure folder exists
                if (!await this.app.vault.adapter.exists(outboxFolder)) {
                    await this.app.vault.createFolder(outboxFolder);
                }

                const ts = (window as any).moment().format("YYYYMMDD-HHmmss");
                const baseName = file.basename;
                const outFileName = `${outboxFolder}/${baseName}-processed-${ts}.md`;
                
                await this.app.vault.create(outFileName, textResult);
                fileSavedMessage = `\n\n✅ **File saved to**: \`${outFileName}\``;
                new Notice(`Output saved to ${outFileName}`);
            } catch (saveErr) {
                console.error("Failed to save output to vault:", saveErr);
                fileSavedMessage = `\n\n❌ **Failed to save file**: ${saveErr instanceof Error ? saveErr.message : String(saveErr)}`;
            }
        }

        const successMessage = textResult 
            ? `### ${headerStatus}: Dr. Egeria Result (${directiveUsed})\n\n${textResult}${fileSavedMessage}`
            : `### ${headerStatus}: Dr. Egeria Result (${directiveUsed})\n\n✅ Command completed with no content returned.`;

        new ResultModal(this.app, successMessage, this.settings.verbose).open();
            
            await client.close();
            notice.hide();
            
        } catch (err) {
            console.error("MCP Error:", err);
            notice.hide();
            let errorMessage = (err instanceof Error ? err.message : String(err));
            if (errorMessage.includes("timeout")) {
                errorMessage = "⌛ Request timed out. The backend might still be processing, please check the outbox in a few moments.";
            }
            new Notice("❌ MCP Error: " + errorMessage);
        }
    }

    async loadSettings() {
        this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
    }

    async saveSettings() {
        await this.saveData(this.settings);
    }
}

class ResultModal extends Modal {
    text: string;
    verbose: boolean;

    constructor(app: App, text: string, verbose: boolean = true) {
        super(app);
        this.text = text;
        this.verbose = verbose;
    }

    onOpen() {
        const { contentEl, modalEl } = this;
        contentEl.createEl("h2", { text: "Dr.Egeria Results (MCP)" });

        modalEl.style.resize = "both";
        modalEl.style.overflow = "auto";
        modalEl.style.minWidth = "400px";
        modalEl.style.minHeight = "300px";
        modalEl.style.width = "80%";
        modalEl.style.height = "70%";

        let displayContent = this.text;
        if (!this.verbose) {
            // Simple heuristic to remove log lines and debug info
            displayContent = this.text.split("\n")
                .filter(line => {
                    const lower = line.toLowerCase();
                    return !lower.includes("| info |") && 
                           !lower.includes("| debug |") && 
                           !lower.includes("captured") && 
                           !lower.includes("executing dr_egeria_run_block");
                })
                .join("\n")
                .replace(/\n\n+/g, "\n\n");
        }

        const pre = contentEl.createEl("pre", { text: displayContent });
        pre.style.whiteSpace = "pre-wrap";
        pre.style.wordBreak = "break-word";
        pre.style.height = "calc(100% - 60px)";
        pre.style.overflowY = "auto";
        pre.style.margin = "0";
        pre.style.padding = "10px";
        pre.style.border = "1px solid var(--background-modifier-border)";
        pre.style.backgroundColor = "var(--background-secondary)";
    }

    onClose() {
        const { contentEl } = this;
        contentEl.empty();
    }
}

class CallingTheDrSettingTab extends PluginSettingTab {
    plugin: CallingTheDrPlugin;

    constructor(app: App, plugin: CallingTheDrPlugin) {
        super(app, plugin);
        this.plugin = plugin;
    }

    display(): void {
        const { containerEl } = this;
        containerEl.empty();

        containerEl.createEl("h2", { text: "Calling the Dr. Settings (MCP)" });

        new Setting(containerEl)
            .setName("MCP Server URL")
            .setDesc("The SSE endpoint of your Dr. Egeria MCP server.")
            .addText(text => text
                .setPlaceholder("http://localhost:8000/sse")
                .setValue(this.plugin.settings.mcpUrl)
                .onChange(async (value) => {
                    this.plugin.settings.mcpUrl = value;
                    await this.plugin.saveSettings();
                }));

        new Setting(containerEl)
            .setName("MCP Access Token")
            .setDesc("Security token for MCP access.")
            .addText(text => text
                .setPlaceholder("Enter token")
                .setValue(this.plugin.settings.mcpToken)
                .onChange(async (value) => {
                    this.plugin.settings.mcpToken = value;
                    await this.plugin.saveSettings();
                }));

        containerEl.createEl("h3", { text: "Egeria Settings" });

        new Setting(containerEl)
            .setName("Egeria User ID")
            .addText(text => text
                .setPlaceholder("erinoverview")
                .setValue(this.plugin.settings.userId)
                .onChange(async (value) => {
                    this.plugin.settings.userId = value;
                    await this.plugin.saveSettings();
                }));

        new Setting(containerEl)
            .setName("Egeria User Password")
            .addText(text => text
                .setPlaceholder("secret")
                .setValue(this.plugin.settings.userPass)
                .onChange(async (value) => {
                    this.plugin.settings.userPass = value;
                    await this.plugin.saveSettings();
                })
                .inputEl.type = "password");

        new Setting(containerEl)
            .setName("Verbose Output")
            .setDesc("If disabled, debug statements and internal logs are hidden from the results popup.")
            .addToggle(toggle => toggle
                .setValue(this.plugin.settings.verbose)
                .onChange(async (value) => {
                    this.plugin.settings.verbose = value;
                    await this.plugin.saveSettings();
                }));

        new Setting(containerEl)
            .setName("Egeria Platform URL")
            .addText(text => text
                .setPlaceholder("https://host.docker.internal:9443")
                .setValue(this.plugin.settings.egeriaUrl)
                .onChange(async (value) => {
                    this.plugin.settings.egeriaUrl = value;
                    await this.plugin.saveSettings();
                }));

        new Setting(containerEl)
            .setName("Egeria View Server")
            .addText(text => text
                .setPlaceholder("qs-view-server")
                .setValue(this.plugin.settings.viewServer)
                .onChange(async (value) => {
                    this.plugin.settings.viewServer = value;
                    await this.plugin.saveSettings();
                }));

        new Setting(containerEl)
            .setName("Default Directive")
            .setDesc("The default action for Dr. Egeria (process, validate, or display).")
            .addDropdown(dropdown => dropdown
                .addOption("process", "Process (Execute)")
                .addOption("validate", "Validate (Check only)")
                .addOption("display", "Display (View)")
                .setValue(this.plugin.settings.defaultDirective)
                .onChange(async (value) => {
                    this.plugin.settings.defaultDirective = value;
                    await this.plugin.saveSettings();
                }));

        new Setting(containerEl)
            .setName("Outbox Path")
            .setDesc("The location where Dr. Egeria should save output files (relative to vault root).")
            .addText(text => text
                .setPlaceholder("dr-egeria-outbox")
                .setValue(this.plugin.settings.outboxPath)
                .onChange(async (value) => {
                    this.plugin.settings.outboxPath = value;
                    await this.plugin.saveSettings();
                }));

        new Setting(containerEl)
            .setName("Input Path")
            .setDesc("The path to the folder containing the current note (relative to vault root). For example: keeping-safe/martyns-law")
            .addText(text => text
                .setPlaceholder("keeping-safe/martyns-law")
                .setValue(this.plugin.settings.inputPath)
                .onChange(async (value) => {
                    this.plugin.settings.inputPath = value;
                    await this.plugin.saveSettings();
                }));

        containerEl.createEl("h3", { text: "Vault Roots" });
        containerEl.createEl("p", { text: "Ensure the path below matches the mount point for your vault in Docker." });

        new Setting(containerEl)
            .setName("Vault Root (Container Side)")
            .setDesc("The absolute path to your vault inside the Docker container.")
            .addText(text => text
                .setPlaceholder("/coco-workbooks")
                .setValue(this.plugin.settings.egeriaUrl.includes("coco") ? "/coco-workbooks" : "/work/Work-Obsidian")
                .setDisabled(true));

        containerEl.createEl("h3", { text: "Maintenance" });

        new Setting(containerEl)
            .setName("Refresh Dr. Egeria Specs")
            .setDesc("Reload command specifications and dispatcher in the backend.")
            .addButton(button => button
                .setButtonText("Refresh Now")
                .onClick(async () => {
                    await this.refreshSpecs();
                }));
    }

    async refreshSpecs() {
        new Notice("Refreshing Dr. Egeria specs...");
        try {
            const url = new URL(this.plugin.settings.mcpUrl);
            url.searchParams.set("token", this.plugin.settings.mcpToken);

            const transport = new SSEClientTransport(url);
            const client = new Client({
                name: "Calling the Dr. Obsidian Plugin",
                version: "0.1.0"
            }, {
                capabilities: {}
            });

            await client.connect(transport);
            await client.callTool({
                name: "egeria_refresh_specs",
                arguments: {}
            });
            await client.close();
            new Notice("✅ Dr. Egeria specs refreshed successfully.");
        } catch (err) {
            console.error("Refresh Error:", err);
            new Notice("❌ Refresh failed: " + (err instanceof Error ? err.message : String(err)));
        }
    }
}
