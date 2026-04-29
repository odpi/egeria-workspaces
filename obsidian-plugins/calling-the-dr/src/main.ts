import { App, Modal, Notice, Plugin, PluginSettingTab, Setting, requestUrl } from "obsidian";
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
}

const DEFAULT_SETTINGS: CallingTheDrSettings = {
    mcpUrl: "http://localhost:8000/sse",
    mcpToken: "egeria-secret-mcp-token",
    userId: "erinoverview",
    userPass: "secret",
    egeriaUrl: "https://host.docker.internal:9443",
    viewServer: "qs-view-server",
    defaultDirective: "process",
    outboxPath: "dr-egeria-outbox"
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
        
        new Notice("Calling the Dr. via MCP SSE...");

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
                    outbox_path: this.settings.outboxPath,
                    output_folder: file.parent?.path || "",
                    input_file: file.name
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

        const successMessage = textResult 
            ? `### ${headerStatus}: Dr. Egeria Result (${directiveUsed})\n\n${textResult}`
            : `### ${headerStatus}: Dr. Egeria Result (${directiveUsed})\n\n✅ Command completed with no console output.`;

        new ResultModal(this.app, successMessage).open();
            
            await client.close();
            
        } catch (err) {
            console.error("MCP Error:", err);
            new Notice("❌ MCP Error: " + (err instanceof Error ? err.message : String(err)));
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

    constructor(app: App, text: string) {
        super(app);
        this.text = text;
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

        const pre = contentEl.createEl("pre", { text: this.text });
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
            .setDesc("The location where Dr. Egeria should save output files (relative to workspace root).")
            .addText(text => text
                .setPlaceholder("dr-egeria-outbox")
                .setValue(this.plugin.settings.outboxPath)
                .onChange(async (value) => {
                    this.plugin.settings.outboxPath = value;
                    await this.plugin.saveSettings();
                }));

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
