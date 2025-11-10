import { injectable } from 'inversify';
import axios, { AxiosInstance } from 'axios';

export interface BECAMessage {
    role: 'user' | 'assistant';
    content: string;
    timestamp?: string;
}

export interface BECAResponse {
    response: string;
    files_modified?: string[];
    error?: string;
}

export interface BECAStatus {
    status: string;
    model?: string;
    mode?: string;
    error?: string;
}

@injectable()
export class BECAApiService {
    private apiClient: AxiosInstance;
    private apiUrl: string;

    constructor() {
        // Dynamically determine API URL based on current host
        // This allows the frontend to work with any external IP
        const protocol = window.location.protocol; // http: or https:
        const hostname = window.location.hostname; // e.g., 34.134.149.22 or localhost
        
        // Use the same host as frontend but port 8000
        // Note: process.env is not available in browser context
        this.apiUrl = `${protocol}//${hostname}:8000`;
        
        console.log(`BECA API URL: ${this.apiUrl}`);
        
        this.apiClient = axios.create({
            baseURL: this.apiUrl,
            timeout: 300000, // 5 minutes for long-running tasks
            headers: {
                'Content-Type': 'application/json',
            }
        });
    }
    setApiUrl(url: string): void {
        this.apiUrl = url;
        console.log(`BECA API URL updated to: ${this.apiUrl}`);
        this.apiClient = axios.create({
            baseURL: this.apiUrl,
            timeout: 300000,
            headers: {
                'Content-Type': 'application/json',
            }
        });
    }

    /**
     * Send a message to BECA and get a response
     */
    async sendMessage(message: string, mode: 'plan' | 'act' = 'act'): Promise<BECAResponse> {
        try {
            const response = await this.apiClient.post('/api/chat', {
                message,
                mode,
                history: []
            });
            return {
                response: response.data.response,
                files_modified: response.data.files_changed || [],
                error: undefined
            };
        } catch (error: any) {
            console.error('Error sending message to BECA:', error);
            return {
                response: `Error: ${error.response?.data?.detail || error.message}`,
                error: error.message
            };
        }
    }

    /**
     * Get BECA's current status
     */
    async getStatus(): Promise<BECAStatus> {
        try {
            const response = await this.apiClient.get('/api/status');
            return {
                status: response.data.agent_available ? 'online' : 'offline',
                model: 'ollama',
                mode: 'ready'
            };
        } catch (error: any) {
            console.error('Error getting BECA status:', error);
            return {
                status: 'error',
                error: error.message
            };
        }
    }

    /**
     * Get chat history - stored locally in browser
     */
    async getChatHistory(): Promise<BECAMessage[]> {
        // Chat history is now managed client-side
        return [];
    }

    /**
     * Clear chat history - managed locally in browser
     */
    async clearHistory(): Promise<void> {
        // Chat history clearing is now managed client-side
    }

    /**
     * Get file tree
     */
    async getFileTree(): Promise<any> {
        try {
            const response = await this.apiClient.get('/api/files/tree');
            return response.data;
        } catch (error: any) {
            console.error('Error getting file tree:', error);
            return null;
        }
    }

    /**
     * Read file contents
     */
    async readFile(path: string): Promise<string> {
        try {
            const response = await this.apiClient.post('/api/files/read', { path });
            return response.data.content || '';
        } catch (error: any) {
            console.error('Error reading file:', error);
            throw error;
        }
    }

    /**
     * Get current API URL
     */
    getApiUrl(): string {
        return this.apiUrl;
    }
}
