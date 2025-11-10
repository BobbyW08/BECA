import * as React from 'react';
import { injectable, postConstruct, inject } from 'inversify';
import { ReactWidget } from '@theia/core/lib/browser/widgets/react-widget';
import { MessageService } from '@theia/core';
import { BECAApiService, BECAMessage } from './beca-api-service';
import { FileService } from '@theia/filesystem/lib/browser/file-service';
import { EditorManager } from '@theia/editor/lib/browser';
import URI from '@theia/core/lib/common/uri';

@injectable()
export class BECAChatWidget extends ReactWidget {
    static readonly ID = 'beca-chat-widget';
    static readonly LABEL = 'BECA Chat';

    @inject(BECAApiService)
    protected readonly becaApi!: BECAApiService;

    @inject(MessageService)
    protected readonly messageService!: MessageService;

    @inject(FileService)
    protected readonly fileService!: FileService;

    @inject(EditorManager)
    protected readonly editorManager!: EditorManager;

    private messages: BECAMessage[] = [];
    private inputValue: string = '';
    private mode: 'plan' | 'act' = 'act';
    private followMode: boolean = true;
    private isLoading: boolean = false;

    @postConstruct()
    protected init(): void {
        this.id = BECAChatWidget.ID;
        this.title.label = BECAChatWidget.LABEL;
        this.title.caption = BECAChatWidget.LABEL;
        this.title.closable = true;
        this.title.iconClass = 'fa fa-comments';
        this.update();
        this.loadChatHistory();
    }

    protected async loadChatHistory(): Promise<void> {
        try {
            const history = await this.becaApi.getChatHistory();
            this.messages = Array.isArray(history) ? history : [];
            this.update();
        } catch (error) {
            console.error('Error loading chat history:', error);
            this.messages = [];
            this.update();
        }
    }

    protected render(): React.ReactNode {
        return (
            <div className="beca-chat-container">
                <div className="beca-chat-header">
                    <h3>BECA Assistant</h3>
                    <div className="beca-chat-controls">
                        <button
                            className={`mode-toggle ${this.mode === 'plan' ? 'active' : ''}`}
                            onClick={() => this.toggleMode()}
                            title="Toggle between Plan and Act mode"
                        >
                            {this.mode === 'plan' ? 'PLAN' : 'ACT'}
                        </button>
                        <button
                            className={`follow-toggle ${this.followMode ? 'active' : ''}`}
                            onClick={() => this.toggleFollow()}
                            title="Auto-open files that BECA modifies"
                        >
                            <i className={`fa fa-eye${this.followMode ? '' : '-slash'}`}></i>
                        </button>
                        <button
                            onClick={() => this.clearChat()}
                            title="Clear chat history"
                        >
                            <i className="fa fa-trash"></i>
                        </button>
                    </div>
                </div>

                <div className="beca-chat-messages">
                    {this.messages.map((msg, idx) => (
                        <div key={idx} className={`message ${msg.role}`}>
                            <div className="message-role">
                                {msg.role === 'user' ? 'You' : 'BECA'}
                            </div>
                            <div className="message-content">
                                {this.formatMessage(msg.content)}
                            </div>
                            {msg.timestamp && (
                                <div className="message-timestamp">
                                    {new Date(msg.timestamp).toLocaleTimeString()}
                                </div>
                            )}
                        </div>
                    ))}
                    {this.isLoading && (
                        <div className="message assistant loading">
                            <div className="message-role">BECA</div>
                            <div className="message-content">
                                <i className="fa fa-spinner fa-spin"></i> Thinking...
                            </div>
                        </div>
                    )}
                </div>

                <div className="beca-chat-input">
                    <textarea
                        value={this.inputValue}
                        onChange={(e) => this.handleInputChange(e)}
                        onKeyPress={(e) => this.handleKeyPress(e)}
                        placeholder={`Ask BECA anything... (${this.mode.toUpperCase()} mode)`}
                        disabled={this.isLoading}
                        rows={3}
                    />
                    <button
                        onClick={() => this.sendMessage()}
                        disabled={this.isLoading || !this.inputValue.trim()}
                        className="send-button"
                    >
                        <i className="fa fa-paper-plane"></i>
                    </button>
                </div>
            </div>
        );
    }

    private formatMessage(content: string): React.ReactNode {
        // Simple markdown-like formatting
        const lines = content.split('\n');
        return lines.map((line, idx) => {
            // Code blocks
            if (line.startsWith('```')) {
                return <pre key={idx}><code>{line.substring(3)}</code></pre>;
            }
            // Bold text
            line = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            // Inline code
            line = line.replace(/`(.*?)`/g, '<code>$1</code>');
            
            return <p key={idx} dangerouslySetInnerHTML={{ __html: line }} />;
        });
    }

    private handleInputChange(e: React.ChangeEvent<HTMLTextAreaElement>): void {
        this.inputValue = e.target.value;
        this.update();
    }

    private handleKeyPress(e: React.KeyboardEvent<HTMLTextAreaElement>): void {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            this.sendMessage();
        }
    }

    private async sendMessage(): Promise<void> {
        if (!this.inputValue.trim() || this.isLoading) {
            return;
        }

        const userMessage = this.inputValue.trim();
        this.inputValue = '';
        this.isLoading = true;

        // Add user message to chat
        this.messages.push({
            role: 'user',
            content: userMessage,
            timestamp: new Date().toISOString()
        });
        this.update();

        try {
            // Send message to BECA
            const response = await this.becaApi.sendMessage(userMessage, this.mode);

            // Add BECA's response to chat
            this.messages.push({
                role: 'assistant',
                content: response.response,
                timestamp: new Date().toISOString()
            });

            // Handle file tracking if enabled and files were modified
            if (this.followMode && Array.isArray(response.files_modified) && response.files_modified.length > 0) {
                await this.openModifiedFiles(response.files_modified);
            }

            if (response.error) {
                this.messageService.error(`BECA Error: ${response.error}`);
            }
        } catch (error: any) {
            this.messages.push({
                role: 'assistant',
                content: `Error: ${error.message}`,
                timestamp: new Date().toISOString()
            });
            this.messageService.error(`Failed to send message: ${error.message}`);
        } finally {
            this.isLoading = false;
            this.update();
            this.scrollToBottom();
        }
    }

    private async openModifiedFiles(files: string[]): Promise<void> {
        if (!Array.isArray(files) || files.length === 0) {
            return;
        }
        
        for (const file of files) {
            try {
                if (file && typeof file === 'string') {
                    const uri = new URI(file);
                    await this.editorManager.open(uri, {
                        mode: 'reveal'
                    });
                }
            } catch (error: any) {
                console.error(`Failed to open file ${file}:`, error);
            }
        }
    }

    private toggleMode(): void {
        this.mode = this.mode === 'plan' ? 'act' : 'plan';
        this.messageService.info(`Switched to ${this.mode.toUpperCase()} mode`);
        this.update();
    }

    private toggleFollow(): void {
        this.followMode = !this.followMode;
        this.messageService.info(
            this.followMode
                ? 'Follow mode enabled - files will auto-open'
                : 'Follow mode disabled'
        );
        this.update();
    }

    private async clearChat(): Promise<void> {
        const confirmed = await this.messageService.info(
            'Clear all chat history?',
            'Cancel',
            'Clear'
        );
        if (confirmed === 'Clear') {
            await this.becaApi.clearHistory();
            this.messages = [];
            this.update();
        }
    }

    private scrollToBottom(): void {
        setTimeout(() => {
            const messagesDiv = document.querySelector('.beca-chat-messages');
            if (messagesDiv) {
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
        }, 100);
    }
}
