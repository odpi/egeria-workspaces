import { App, FileSystemAdapter, Modal, Notice, Plugin, PluginSettingTab, Setting } from "obsidian";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";

interface CallDrEgeriaSettings {
    mcpUrl: string;
    mcpToken: string;
    userId: string;
    userPass: string;
    egeriaUrl: string;
    viewServer: string;
    defaultDirective: string;
    outboxPath: string;
    inputPath: string;
    vaultRoot: string;
    verbose: boolean;
}

const DEFAULT_SETTINGS: CallDrEgeriaSettings = {
    mcpUrl: "http://localhost:8000/sse",
    mcpToken: "egeria-secret-mcp-token",
    userId: "erinoverview",
    userPass: "secret",
    egeriaUrl: "https://host.docker.internal:9443",
    viewServer: "qs-view-server",
    defaultDirective: "process",
    outboxPath: "dr-egeria-outbox",
    inputPath: "",
    vaultRoot: "/work/Work-Obsidian",
    verbose: true
};

export default class CallDrEgeriaPlugin extends Plugin {
    settings: CallDrEgeriaSettings = DEFAULT_SETTINGS;
    private lastInternalSave = 0;

    async onload() {
        await this.loadSettings();
        this.registerExternalConfigWatcher();

        this.addRibbonIcon("briefcase", "Call Dr. Egeria (MCP)", async () => {
            await this.runMcpBlock();
        });

        this.addCommand({
            id: "run-mcp-block",
            name: "Run Note via MCP",
            callback: async () => {
                await this.runMcpBlock();
            }
        });

        this.addSettingTab(new CallDrEgeriaSettingTab(this.app, this));
    }

    async runMcpBlock() {
        const file = this.app.workspace.getActiveFile();
        if (!file) {
            new Notice("No active file.");
            return;
        }

        const content = await this.app.vault.read(file);
        const notice = new Notice("Calling Dr. Egeria via MCP SSE...", 0);

        try {
            const url = new URL(this.settings.mcpUrl);
            url.searchParams.set("token", this.settings.mcpToken);

            const transport = new SSEClientTransport(url);

            const client = new Client({
                name: "Call Dr. Egeria Obsidian Plugin",
                version: "0.2.0"
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
                    output_folder: "",
                    outbox_path: this.settings.outboxPath,
                    input_file: this.settings.inputPath
                        ? `${this.settings.vaultRoot}/${this.settings.inputPath}/${file.name}`.replace(/\/+/g, '/')
                        : `${this.settings.vaultRoot}/${file.name}`.replace(/\/+/g, '/')
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

            let fileSavedMessage = "";
            if (directiveUsed === "process" && textResult && !textResult.startsWith("Error:") && !textResult.startsWith("Warning:")) {
                try {
                    const outboxFolder = this.settings.outboxPath || "dr-egeria-outbox";
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
        if (!this.settings.vaultRoot) {
            this.settings.vaultRoot = this.settings.egeriaUrl.includes("coco") ? "/coco-workbooks" : "/work/Work-Obsidian";
        }
    }

    async saveSettings() {
        this.lastInternalSave = Date.now();
        await this.saveData(this.settings);
    }

    private registerExternalConfigWatcher() {
        const adapter = this.app.vault.adapter;
        if (!(adapter instanceof FileSystemAdapter)) return;

        // eslint-disable-next-line @typescript-eslint/no-var-requires
        const fs = require("fs") as typeof import("fs");
        const path = require("path") as typeof import("path");

        const dataJsonPath = path.join(
            adapter.getBasePath(),
            this.app.vault.configDir,
            "plugins",
            this.manifest.id,
            "data.json"
        );

        let watcher: ReturnType<typeof fs.watch> | null = null;
        try {
            watcher = fs.watch(dataJsonPath, async (eventType: string) => {
                if (eventType !== "change") return;
                // Ignore changes that we triggered ourselves
                if (Date.now() - this.lastInternalSave < 1500) return;

                await this.loadSettings();
                new Notice(`Dr. Egeria: session updated — persona is now "${this.settings.userId}"`);
            });
        } catch {
            // data.json may not exist yet on first install
            console.log("call-dr-egeria: data.json not found, config watcher not started");
        }

        this.register(() => {
            if (watcher) watcher.close();
        });
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
        contentEl.createEl("h2", { text: "Dr. Egeria Results (MCP)" });

        modalEl.style.resize = "both";
        modalEl.style.overflow = "auto";
        modalEl.style.minWidth = "400px";
        modalEl.style.minHeight = "300px";
        modalEl.style.width = "80%";
        modalEl.style.height = "70%";

        let displayContent = this.text;
        if (!this.verbose) {
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

class CallDrEgeriaSettingTab extends PluginSettingTab {
    plugin: CallDrEgeriaPlugin;

    constructor(app: App, plugin: CallDrEgeriaPlugin) {
        super(app, plugin);
        this.plugin = plugin;
    }

    display(): void {
        const { containerEl } = this;
        containerEl.empty();

        containerEl.createEl("h2", { text: "Call Dr. Egeria Settings (MCP)" });

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
            .setDesc("The path to the folder containing the current note (relative to vault root).")
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
                .setValue(this.plugin.settings.vaultRoot)
                .onChange(async (value) => {
                    this.plugin.settings.vaultRoot = value;
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
                name: "Call Dr. Egeria Obsidian Plugin",
                version: "0.2.0"
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
