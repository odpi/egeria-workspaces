import { App, Editor, MarkdownView, Modal, Plugin, Notice, PluginSettingTab, Setting, requestUrl } from "obsidian";

interface SendNoteSettings {
    apiUrl: string;
    userId: string;
    userPass: string;
    outputFolder: string;
}

const DEFAULT_SETTINGS: SendNoteSettings = {
    apiUrl: "http://localhost:8085/dr-egeria/process",
    userId: "erinoverview",
    userPass: "secret",
    outputFolder: "Monday"
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

        const content = await this.app.vault.read(file);

        const payload = {
            input_file: file.basename+".md",
            output_folder: this.settings.outputFolder,
            directive: "process",
            url: "https://host.docker.internal:9443",
            server: "qs-view-server",
            user_id: this.settings.userId,
            user_pass: this.settings.userPass
           // content: content
        };

        console.log("📤 Sending note with payload:", payload);

        try {
            const response = await requestUrl({
                url: this.settings.apiUrl,
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify(payload),
                // timeout: 30000, // optional
                 throw: true,   // set to false if you prefer not to throw on non-2xx
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

            new Notice("✅ Note sent successfully!");

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
            .setDesc("Endpoint to send notes to")
            .addText(text => text
                .setPlaceholder("https://localhost:8085/dr-egeria/process")
                .setValue(this.plugin.settings.apiUrl)
                .onChange(async (value) => {
                    this.plugin.settings.apiUrl = value;
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
            .addText(text => text
                .setPlaceholder("secret")
                .setValue(this.plugin.settings.userPass)
                .onChange(async (value) => {
                    this.plugin.settings.userPass = value;
                    await this.plugin.saveSettings();
                }));

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
    }
}
