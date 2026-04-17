import { App, Notice, Plugin, PluginSettingTab, Setting, normalizePath, requestUrl, Modal } from "obsidian";

interface SendNoteSettings {
    apiUrl: string;
    platformUrl: string;
    serverName: string;
    directive: "process" | "validate" | "display";
    userId: string;
    userPass: string;
    outputFolder: string;
    inputFolder?: string; // optional folder to prepend to input_file
}

const DEFAULT_SETTINGS: SendNoteSettings = {
    apiUrl: "http://localhost:8085/dr-egeria/process",
    platformUrl: "https://host.docker.internal:9443",
    serverName: "qs-view-server",
    directive: "process",
    userId: "erinoverview",
    userPass: "secret",
    outputFolder: "Monday",
    inputFolder: "" // default empty (not used)
};

export default class SendNotePlugin extends Plugin {
    settings: SendNoteSettings = DEFAULT_SETTINGS;

    async onload() {
        await this.loadSettings();

        // Ribbon icon
        this.addRibbonIcon("phone", "Call Dr.Egeria", async () => {
            await this.sendCurrentNote();
        });

        // Command palette
        this.addCommand({
            id: "send-current-note",
            name: "Send Current Note via REST",
            callback: async () => {
                await this.sendCurrentNote();
            }
        });

        // Settings tab
        this.addSettingTab(new SendNoteSettingTab(this.app, this));
    }

    async sendCurrentNote() {
        const file = this.app.workspace.getActiveFile();
        if (!file) {
            new Notice("No active file.");
            return;
        }

        // Use vault-relative path so subfolders are preserved and filenames do not collide.
        const baseName = normalizePath(file.name);
        const inputFile = (this.settings.inputFolder && this.settings.inputFolder.trim().length > 0)
            ? `${this.settings.inputFolder.replace(/\\+$/g, "").replace(/\/+$/g, "")}/${baseName}`
            : baseName;

        const payload = {
            input_file: inputFile,
            output_folder: this.settings.outputFolder,
            directive: this.settings.directive,
            url: this.settings.platformUrl,
            server: this.settings.serverName,
            user_id: this.settings.userId,
            user_pass: this.settings.userPass
        };

        console.log("📤 Sending note with payload:", payload);

        try {
            const response = await requestUrl({
                url: this.settings.apiUrl,
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "text/plain, application/json"
                },
                body: JSON.stringify(payload),
                throw: false,
            });


            const contentType = (response.headers?.["content-type"] ?? "").toLowerCase();
            const rawBody: string = response.text ?? "";
            let parsed: any = undefined;
            if (contentType.includes("application/json")) {
                try {
                    parsed = JSON.parse(rawBody);
                } catch {
                    // leave parsed undefined if JSON is malformed
                }
            }

            console.log("📥 Response status:", response.status);
            console.log("📥 Response body:", parsed ?? rawBody);

            if (response.status < 200 || response.status >= 300) {
                const detail =
                    (parsed && (parsed.message || parsed.error || parsed.detail)) ||
                    rawBody ||
                    "Request failed";
                throw new Error(`HTTP ${response.status} - ${detail}`);
            }

            if (rawBody.trim().length > 0) {
                if (rawBody.length > 200) {
                    new ResultModal(this.app, rawBody).open();
                    new Notice(`✅ Dr.Egeria processed the note. See results in modal.`);
                } else {
                    new Notice(`✅ Dr.Egeria response: ${rawBody}`);
                }
            } else {
                new Notice("✅ Note sent successfully!");
            }

        } catch (err: unknown) {
            let message = "Unknown error";
            if (err instanceof Error) {
                message = err.message;
            } else if (typeof err === "string") {
                message = err;
            } else {
                try { message = JSON.stringify(err); } catch {}
            }
            new Notice("❌ Failed to send note: " + message);
            console.error("SendNotePlugin error:", err);
        }

    }

    async loadSettings() {
        this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
    }

    async saveSettings() {
        await this.saveData(this.settings);
    }
}

class SendNoteSettingTab extends PluginSettingTab {
    plugin: SendNotePlugin;

    constructor(app: App, plugin: SendNotePlugin) {
        super(app, plugin);
        this.plugin = plugin;
    }

    display(): void {
        const { containerEl } = this;
        containerEl.empty();

        containerEl.createEl("h2", { text: "Send Note Plugin Settings" });

        new Setting(containerEl)
            .setName("API URL")
            .setDesc("FastAPI endpoint that accepts process requests")
            .addText(text => text
                .setPlaceholder("https://localhost:8085/dr-egeria/process")
                .setValue(this.plugin.settings.apiUrl)
                .onChange(async (value) => {
                    this.plugin.settings.apiUrl = value;
                    await this.plugin.saveSettings();
                }));

        new Setting(containerEl)
            .setName("Platform URL")
            .setDesc("Egeria platform URL passed in the request payload")
            .addText(text => text
                .setPlaceholder("https://host.docker.internal:9443")
                .setValue(this.plugin.settings.platformUrl)
                .onChange(async (value) => {
                    this.plugin.settings.platformUrl = value;
                    await this.plugin.saveSettings();
                }));

        new Setting(containerEl)
            .setName("View Server")
            .setDesc("Egeria view server passed in the request payload")
            .addText(text => text
                .setPlaceholder("qs-view-server")
                .setValue(this.plugin.settings.serverName)
                .onChange(async (value) => {
                    this.plugin.settings.serverName = value;
                    await this.plugin.saveSettings();
                }));

        new Setting(containerEl)
            .setName("Directive")
            .setDesc("How Dr.Egeria should handle the file")
            .addDropdown(dropdown => dropdown
                .addOption("process", "process")
                .addOption("validate", "validate")
                .addOption("display", "display")
                .setValue(this.plugin.settings.directive)
                .onChange(async (value) => {
                    if (value === "process" || value === "validate" || value === "display") {
                        this.plugin.settings.directive = value;
                    }
                    await this.plugin.saveSettings();
                }));

        new Setting(containerEl)
            .setName("User ID")
            .setDesc("User name for authentication")
            .addText(text => text
                .setPlaceholder("erinoverview")
                .setValue(this.plugin.settings.userId)
                .onChange(async (value) => {
                    this.plugin.settings.userId = value;
                    await this.plugin.saveSettings();
                }));

        new Setting(containerEl)
            .setName("Password")
            .setDesc("Password for authentication")
            .addText(text => {
                text.setPlaceholder("secret")
                    .setValue(this.plugin.settings.userPass)
                    .onChange(async (value) => {
                        this.plugin.settings.userPass = value;
                        await this.plugin.saveSettings();
                    });
                text.inputEl.type = "password";
                return text;
            });

        new Setting(containerEl)
            .setName("Output Folder")
            .setDesc("Name of the output folder")
            .addText(text => text
                .setPlaceholder("Monday")
                .setValue(this.plugin.settings.outputFolder)
                .onChange(async (value) => {
                    this.plugin.settings.outputFolder = value;
                    await this.plugin.saveSettings();
                }));

        new Setting(containerEl)
            .setName("Input Folder (optional)")
            .setDesc("If set, prepended to vault-relative file path as 'input_folder/path/to/file.md'")
            .addText(text => text
                .setPlaceholder("inbox")
                .setValue(this.plugin.settings.inputFolder || "")
                .onChange(async (value) => {
                    this.plugin.settings.inputFolder = value;
                    await this.plugin.saveSettings();
                }));

        containerEl.createEl("h3", { text: "Maintenance" });

        new Setting(containerEl)
            .setName("Refresh Command Specs")
            .setDesc("Reload Dr. Egeria command definitions from JSON files on the server")
            .addButton(button => button
                .setButtonText("Refresh Now")
                .onClick(async () => {
                    const refreshUrl = this.plugin.settings.apiUrl.replace("/process", "/refresh");
                    try {
                        const response = await requestUrl({
                            url: refreshUrl,
                            method: "POST",
                        });
                        if (response.status === 200) {
                            new Notice("✅ Command specs refreshed!");
                        } else {
                            new Notice(`❌ Refresh failed (Status ${response.status}): ${response.text}`);
                        }
                    } catch (err) {
                        new Notice(`❌ Error: ${err}`);
                    }
                }));
    }
}

class ResultModal extends Modal {
    text: string;
    constructor(app: App, text: string) {
        super(app);
        this.text = text;
    }

    onOpen() {
        const { contentEl } = this;
        contentEl.createEl("h2", { text: "Dr.Egeria Results" });
        const pre = contentEl.createEl("pre", { text: this.text });
        pre.style.whiteSpace = "pre-wrap";
        pre.style.wordBreak = "break-all";
        pre.style.maxHeight = "400px";
        pre.style.overflowY = "auto";
    }

    onClose() {
        const { contentEl } = this;
        contentEl.empty();
    }
}
